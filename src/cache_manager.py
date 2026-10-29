import os

# Safe import for set_llm_cache across different LangChain versions
try:
    from langchain_core.globals import set_llm_cache
except ImportError:
    from langchain.globals import set_llm_cache

# Safe import for cache classes
try:
    from langchain_community.cache import InMemoryCache, SQLiteCache
except ImportError:
    from langchain.cache import InMemoryCache, SQLiteCache


def configure_cache(cache_type: str = "InMemory"):
    """
    Configures LangChain global LLM caching based on user selection.
    - InMemoryCache: Stored in RAM, fastest, clears on restart.
    - SQLiteCache: Stored in a local file (.langchain.db), persists across sessions.
    """
    if cache_type == "InMemory":
        # Stored in RAM (memory)
        set_llm_cache(InMemoryCache())
        print("Cache configured: InMemoryCache")
        
    elif cache_type == "SQLite":
        # Stored in a local file on disk
        cache_dir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(cache_dir, ".langchain.db")
        set_llm_cache(SQLiteCache(database_path=db_path))
        print(f"Cache configured: SQLiteCache at {db_path}")
        
    else:
        # Default fallback to InMemory
        set_llm_cache(InMemoryCache())