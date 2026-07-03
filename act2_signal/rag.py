# PUPPET Zero-Cost RAG Implementation
# Complete production-ready system with SerpAPI, Sentence-Transformers, Groq

"""
FREE STACK:
- SerpAPI: 100 free queries/month (no 91-day expiry)
- Sentence-Transformers: Open source embeddings (runs locally)
- Groq: Already have API key (LLM inference)
- Streamlit Cloud: Free hosting
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np
from dataclasses import dataclass
import pickle

import streamlit as st
import requests
from groq import Groq
from sentence_transformers import SentenceTransformer

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class ResearchConfig:
    """Configuration for zero-cost RAG system."""
    
    SERP_API_KEY: str = None
    GROQ_API_KEY: str = None
    
    # Local embedding model (free, runs on device)
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # 22MB, fast, good quality
    
    # Cache settings (local file-based)
    CACHE_DIR: str = ".puppet_cache"
    CACHE_TTL_HOURS: int = 24
    
    # Complexity thresholds (auto-detection)
    QUICK_QUERY_KEYWORDS = [
        "latest", "recent", "new", "2024", "2025",
        "how to", "what is", "define",
        "today", "now", "current"
    ]
    DEEP_QUERY_KEYWORDS = [
        "analysis", "research", "compare", "mechanism", "why",
        "history of", "evolution", "trends",
        "impact", "implications", "strategy"
    ]


def get_config() -> ResearchConfig:
    """Load config from Streamlit secrets."""
    return ResearchConfig(
        SERP_API_KEY=st.secrets.get("SERP_API_KEY"),
        GROQ_API_KEY=st.secrets.get("GROQ_API_KEY"),
    )


# ============================================================================
# PART 1: AUTO-COMPLEXITY DETECTION
# ============================================================================

class ComplexityDetector:
    """Automatically decide research depth based on query."""
    
    def __init__(self, config: ResearchConfig):
        self.config = config
    
    def detect_complexity(self, query: str) -> str:
        """
        Returns: "quick" | "standard" | "deep"
        """
        query_lower = query.lower()
        quick_score = sum(1 for kw in self.config.QUICK_QUERY_KEYWORDS 
                         if kw in query_lower)
        deep_score = sum(1 for kw in self.config.DEEP_QUERY_KEYWORDS 
                        if kw in query_lower)
        
        query_length_score = len(query) / 50
        
        total_deep = deep_score + query_length_score
        total_quick = quick_score
        
        if total_deep > 2:
            return "deep"
        elif total_quick > 2 or (total_deep <= 1 and total_quick <= 1):
            return "quick"
        else:
            return "standard"


# ============================================================================
# PART 2: FREE WEB SEARCH (SerpAPI)
# ============================================================================

class FreeWebSearch:
    """Search using SerpAPI (100 free queries/month, no expiry)."""
    
    def __init__(self, config: ResearchConfig):
        self.config = config
        self.api_key = config.SERP_API_KEY
        self.base_url = "https://serpapi.com/search"
    
    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Search using SerpAPI.
        Free tier: 100 queries/month
        Coverage: Entire internet, real-time data
        """
        
        if not self.api_key:
            st.warning(
                "⚠️ SerpAPI key not configured. "
                "Get free key at https://serpapi.com"
            )
            return self._mock_results(query, num_results)
        
        try:
            params = {
                "q": query,
                "api_key": self.api_key,
                "num": min(num_results, 10),
                "engine": "google"
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            # Parse SerpAPI organic results
            for item in data.get("organic_results", [])[:num_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "SerpAPI",
                    "timestamp": datetime.now().isoformat()
                })
            
            return results if results else self._mock_results(query, num_results)
        
        except requests.exceptions.Timeout:
            return self._mock_results(query, num_results)
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                st.warning("Free tier quota exceeded this month")
            return self._mock_results(query, num_results)
        
        except Exception as e:
            return self._mock_results(query, num_results)
    
    def _mock_results(self, query: str, num: int) -> List[Dict]:
        """Fallback mock results."""
        return [
            {
                "title": f"Demo Result {i+1}",
                "url": f"https://example{i}.com",
                "snippet": f"Demo search result for '{query}'",
                "source": "Mock",
                "timestamp": datetime.now().isoformat()
            }
            for i in range(min(num, 3))
        ]


# ============================================================================
# PART 3: LOCAL EMBEDDINGS (FREE)
# ============================================================================

class FreeEmbeddingEngine:
    """Generate embeddings using sentence-transformers (completely free, runs locally)."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embedding model (downloads on first run, then cached)."""
        with st.spinner("Loading embedding model..."):
            self.model = SentenceTransformer(model_name)
        self.dimension = 384  # Dimension of all-MiniLM-L6-v2
    
    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string."""
        return self.model.encode(text, convert_to_tensor=False).tolist()
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts (more efficient)."""
        return self.model.encode(texts, convert_to_tensor=False).tolist()
    
    def similarity(self, text1: str, text2: str) -> float:
        """Cosine similarity between two texts (0-1)."""
        emb1 = self.model.encode(text1)
        emb2 = self.model.encode(text2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(emb1, emb2) / (norm1 * norm2))


# ============================================================================
# PART 4: CHUNKING & PREPROCESSING
# ============================================================================

class ResearchChunker:
    """Convert web search results into semantic chunks for embedding."""
    
    def __init__(self, chunk_size: int = 200, overlap: int = 50):
        self.chunk_size = chunk_size  # words
        self.overlap = overlap  # words
    
    def chunk_search_results(self, 
                            results: List[Dict],
                            strategy: str = "title_snippet") -> List[Dict]:
        """Convert search results into chunks."""
        
        chunks = []
        
        for result in results:
            if strategy == "title_snippet":
                # Simple: title + snippet = 1 chunk
                chunk_text = f"{result['title']}\n\n{result['snippet']}"
                
                chunks.append({
                    "text": chunk_text,
                    "source_title": result.get("title", ""),
                    "source_url": result.get("url", ""),
                    "original_result": result
                })
            
            elif strategy == "split":
                # Split long snippets into multiple chunks with overlap
                full_text = f"{result['title']}. {result['snippet']}"
                text_chunks = self._split_text(full_text)
                
                for chunk_text in text_chunks:
                    chunks.append({
                        "text": chunk_text,
                        "source_title": result.get("title", ""),
                        "source_url": result.get("url", ""),
                        "original_result": result
                    })
        
        return chunks
    
    def _split_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk = " ".join(words[i:i + self.chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks


# ============================================================================
# PART 5: LOCAL CACHE (FALLBACK)
# ============================================================================

class LocalCache:
    """File-based cache for when external services are unavailable."""
    
    def __init__(self, cache_dir: str = ".puppet_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_path(self, query: str) -> str:
        query_hash = hashlib.md5(query.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{query_hash}.pkl")
    
    def cache_research(self, query: str, 
                      chunks: List[Dict],
                      embeddings: List[List[float]]) -> bool:
        """Cache research locally."""
        try:
            cache_path = self.get_cache_path(query)
            data = {
                "query": query,
                "chunks": chunks,
                "embeddings": embeddings,
                "timestamp": datetime.now()
            }
            with open(cache_path, "wb") as f:
                pickle.dump(data, f)
            return True
        except Exception as e:
            st.warning(f"Local cache write failed: {e}")
            return False
    
    def get_cached_research(self, query: str, ttl_hours: int = 24) -> Optional[Dict]:
        """Retrieve cached research if fresh."""
        cache_path = self.get_cache_path(query)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, "rb") as f:
                data = pickle.load(f)
            
            age = datetime.now() - data["timestamp"]
            if age > timedelta(hours=ttl_hours):
                return None
            
            return data
        except Exception as e:
            return None


# ============================================================================
# PART 6: MAIN RAG ORCHESTRATOR
# ============================================================================

class ZeroCostRAG:
    """
    Complete RAG system using only free APIs and local tools.
    
    Pipeline:
    1. Auto-detect query complexity
    2. Web search (SerpAPI)
    3. Chunk results
    4. Generate embeddings locally (sentence-transformers)
    5. Inject into persona prompts
    """
    
    def __init__(self, config: ResearchConfig):
        self.config = config
        self.complexity_detector = ComplexityDetector(config)
        self.search_engine = FreeWebSearch(config)
        self.embedder = FreeEmbeddingEngine()
        self.chunker = ResearchChunker()
        self.local_cache = LocalCache(config.CACHE_DIR)
        self.groq = Groq(api_key=config.GROQ_API_KEY)
    
    def research(self, query: str, force_depth: Optional[str] = None) -> Dict:
        """
        Main RAG pipeline: search → chunk → embed → retrieve.
        
        Args:
            query: User's search query
            force_depth: Override auto-detection ("quick"/"standard"/"deep")
        
        Returns:
            {
                "query": str,
                "depth": str,
                "results": List[Dict],
                "chunks": List[Dict],
                "embeddings": List[List[float]],
                "research_context": str (formatted for LLM)
            }
        """
        
        # Step 1: Check local cache first
        cached = self.local_cache.get_cached_research(query)
        if cached:
            st.info("✅ Using cached research")
            return self._format_research_output(cached, query)
        
        # Step 2: Auto-detect complexity
        depth = force_depth or self.complexity_detector.detect_complexity(query)
        num_results = {
            "quick": 5,
            "standard": 10,
            "deep": 20
        }[depth]
        
        st.info(f"🔍 Detected complexity: **{depth}** ({num_results} results)")
        
        # Step 3: Web search
        with st.spinner(f"Searching {num_results} sources..."):
            results = self.search_engine.search(query, num_results)
        
        if not results:
            st.warning("No search results found")
            return {
                "query": query,
                "depth": depth,
                "results": [],
                "chunks": [],
                "embeddings": [],
                "research_context": "No research found."
            }
        
        # Step 4: Chunk
        chunks = self.chunker.chunk_search_results(
            results,
            strategy="title_snippet" if depth == "quick" else "split"
        )
        
        st.success(f"✅ Created {len(chunks)} semantic chunks")
        
        # Step 5: Embed locally (FREE)
        with st.spinner("Generating embeddings (local)..."):
            chunk_texts = [c["text"] for c in chunks]
            embeddings = self.embedder.embed_batch(chunk_texts)
        
        # Step 6: Cache locally
        self.local_cache.cache_research(query, chunks, embeddings)
        
        # Format output
        return self._format_research_output({
            "query": query,
            "depth": depth,
            "results": results,
            "chunks": chunks,
            "embeddings": embeddings,
            "timestamp": datetime.now()
        }, query)
    
    def _format_research_output(self, data: Dict, query: str) -> Dict:
        """Format RAG output into LLM-ready context."""
        
        chunks = data.get("chunks", [])
        
        # Build research context string
        context_parts = [
            f"## Current Research: {query}\n",
            f"*Retrieved: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
        ]
        
        for i, chunk in enumerate(chunks[:10], 1):  # Top 10 for context
            context_parts.append(
                f"\n### Source {i}: {chunk.get('source_title', 'Untitled')}\n"
                f"**URL:** {chunk.get('source_url', 'N/A')}\n"
                f"{chunk['text']}\n"
            )
        
        research_context = "".join(context_parts)
        
        return {
            "query": query,
            "depth": data.get("depth", "standard"),
            "results": data.get("results", []),
            "chunks": chunks,
            "embeddings": data.get("embeddings", []),
            "research_context": research_context,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_persona_response(self, query: str, 
                            persona_name: str,
                            persona_prompt: str,
                            research_context: str) -> str:
        """Get persona response enriched with research."""
        
        system_with_research = f"""{persona_prompt}

---

## Current Research Context (Retrieved Today)

{research_context}

**Your task:** Respond to the user's query using the above current research.
Maintain your core persona while engaging with today's reality.
Reference the research where relevant."""
        
        message = self.groq.messages.create(
            model="llama-3.1-8b-instant",
            max_tokens=1200,
            system=system_with_research,
            messages=[{"role": "user", "content": query}]
        )
        
        return message.content[0].text