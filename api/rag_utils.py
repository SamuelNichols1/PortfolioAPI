"""
RAG (Retrieval-Augmented Generation) Utilities

This module provides functions for implementing RAG in the portfolio API:
1. Text chunking: Breaking large text into smaller, meaningful pieces using LangChain
2. Embedding generation: Converting text to vector representations
3. Similarity search: Finding the most relevant chunks for a query

The RAG workflow:
- User asks a question about your portfolio
- System converts question to embedding
- Finds most similar portfolio chunks using cosine similarity
- Sends relevant context + question to OpenAI
- OpenAI responds with accurate, context-aware answers

Now using LangChain for intelligent text splitting that respects:
- Sentence boundaries
- Paragraph structure
- Natural semantic breaks
"""
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .models import PortfolioData


# Initialize the embedding model (all-MiniLM-L6-v2 is fast and effective)
# This model converts text into 384-dimensional vectors
_model = None

def get_embedding_model():
    """
    Lazy load the sentence transformer model.
    Only loads when first needed to avoid slow startup times.
    """
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
    """
    Split text into intelligent, semantically-aware chunks using LangChain.
    
    LangChain's RecursiveCharacterTextSplitter is much smarter than simple character splitting:
    - Tries to keep paragraphs together first
    - Then splits on sentences
    - Then splits on words
    - Only splits on characters as a last resort
    - Respects natural language boundaries
    
    This leads to MUCH better retrieval because chunks are semantically coherent.
    
    Args:
        text: The text to chunk
        chunk_size: Target size for each chunk (characters)
        overlap: Number of characters to overlap between chunks
    
    Returns:
        List of intelligently split text chunks
    
    Example:
        >>> text = "I worked at Google for 5 years...\\n\\nMy main projects included..."
        >>> chunks = chunk_text(text)
        >>> # Returns chunks that respect paragraph/sentence boundaries
    """
    # RecursiveCharacterTextSplitter tries these separators in order:
    # 1. "\n\n" (double newline - paragraph breaks)
    # 2. "\n" (single newline)
    # 3. " " (spaces - word boundaries)
    # 4. "" (character by character as last resort)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", "\n", ". ", " ", ""]  # Try in this order
    )
    
    chunks = text_splitter.split_text(text)
    
    # Filter out any empty chunks
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def generate_embedding(text: str) -> List[float]:
    """
    Convert text to a vector embedding using sentence-transformers.
    
    The embedding is a dense vector representation that captures
    the semantic meaning of the text. Similar texts have similar embeddings.
    
    Args:
        text: Text to convert to embedding
    
    Returns:
        List of floats representing the embedding vector (384 dimensions)
    
    Example:
        >>> embedding = generate_embedding("Python developer with 5 years experience")
        >>> len(embedding)  # 384
    """
    model = get_embedding_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Cosine similarity measures how similar two vectors are:
    - 1.0: Identical direction (very similar)
    - 0.0: Orthogonal (no similarity)
    - -1.0: Opposite direction (very dissimilar)
    
    Args:
        vec1: First embedding vector
        vec2: Second embedding vector
    
    Returns:
        Similarity score between -1 and 1
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return float(dot_product / (norm1 * norm2))


def retrieve_relevant_context(
    query: str, 
    top_k: int = 3, 
    min_similarity: float = 0.3
) -> Tuple[str, List[dict]]:
    """
    Retrieve the most relevant portfolio chunks for a given query with improved matching.
    
    This enhanced retrieval function:
    1. Converts the query to an embedding
    2. Calculates similarity with all portfolio chunks
    3. Filters out chunks below the similarity threshold
    4. Returns the top_k most relevant chunks with metadata
    
    Args:
        query: The user's question/prompt
        top_k: Number of top relevant chunks to retrieve (default: 3)
        min_similarity: Minimum similarity score to include (0-1, default: 0.3)
                       Higher = more strict matching, Lower = more permissive
    
    Returns:
        Tuple of (combined_context_string, list_of_matched_chunks)
        Each chunk includes: item, similarity, content, category
        
    Example:
        >>> context, chunks = retrieve_relevant_context("What programming languages do you know?", top_k=3)
        >>> # Returns top 3 relevant chunks about programming languages
        >>> for chunk in chunks:
        >>>     print(f"Similarity: {chunk['similarity']:.2f}, Category: {chunk['category']}")
    """
    # Generate embedding for the user's query
    query_embedding = generate_embedding(query)
    
    # Get all portfolio data from database
    portfolio_items = PortfolioData.objects.all()
    
    if not portfolio_items.exists():
        return "", []
    
    # Calculate similarity scores for each portfolio chunk
    similarities = []
    for item in portfolio_items:
        similarity = cosine_similarity(query_embedding, item.embedding)
        
        # Only include chunks above the minimum similarity threshold
        if similarity >= min_similarity:
            similarities.append({
                'item': item,
                'similarity': similarity,
                'content': item.content,
                'category': item.category
            })
    
    # If no chunks meet the threshold, return empty
    if not similarities:
        return "", []
    
    # Sort by similarity (highest first) and get top_k
    similarities.sort(key=lambda x: x['similarity'], reverse=True)
    top_chunks = similarities[:top_k]
    
    # Combine the top chunks into a single context string
    # Include similarity scores for debugging/transparency
    context_parts = []
    for i, chunk in enumerate(top_chunks, 1):
        context_parts.append(
            f"[CONTEXT {i} - {chunk['category'].upper()} - Relevance: {chunk['similarity']:.2f}]\n"
            f"{chunk['content']}"
        )
    
    combined_context = "\n\n".join(context_parts)
    
    return combined_context, top_chunks


def load_portfolio_text(text: str, category: str = 'other') -> int:
    """
    Load portfolio text into the database with embeddings.
    
    This function:
    1. Chunks the text into manageable pieces
    2. Generates embeddings for each chunk
    3. Saves to database for later retrieval
    
    Args:
        text: The portfolio text to load
        category: Category of the text (experience, skills, etc.)
    
    Returns:
        Number of chunks created
    
    Example:
        >>> text = "I have 5 years of experience as a Python developer..."
        >>> count = load_portfolio_text(text, category='experience')
        >>> print(f"Created {count} chunks")
    """
    # Split text into chunks
    chunks = chunk_text(text)
    
    created_count = 0
    for chunk in chunks:
        # Generate embedding for this chunk
        embedding = generate_embedding(chunk)
        
        # Save to database
        PortfolioData.objects.create(
            content=chunk,
            embedding=embedding,
            category=category
        )
        created_count += 1
    
    return created_count
