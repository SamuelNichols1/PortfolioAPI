# RAG Implementation Guide

## Overview
This Portfolio API now includes **RAG (Retrieval-Augmented Generation)** to provide intelligent, context-aware responses about your career, skills, and experience.

## How It Works

1. **User asks a question** about your portfolio (e.g., "What programming languages do you know?")
2. **System searches** the database for relevant portfolio information using semantic similarity
3. **Top 3 most relevant chunks** are retrieved and combined as context
4. **Context + question** are sent to OpenAI
5. **AI responds** with accurate, personalized information based on your actual portfolio data

## Setup Instructions

### 1. Install Dependencies
```bash
pip install sentence-transformers numpy
pip freeze > requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Load Your Portfolio Data

**Option A: Use Sample Data**
```bash
python manage.py load_portfolio
```

**Option B: Load from a Text File**
```bash
python manage.py load_portfolio --file path/to/your/portfolio.txt
```

**Option C: Clear and Reload**
```bash
python manage.py load_portfolio --clear
```

### 4. Customize Your Portfolio Data

Edit `api/management/commands/load_portfolio.py` and replace the sample data with your actual:
- Work experience
- Technical skills
- Education
- Projects
- Work preferences
- Achievements

## API Usage

### Endpoint
`POST /api/chat/`

### Request
```json
{
  "prompt": "What programming languages do you know?"
}
```

### Response
```json
{
  "prompt": "What programming languages do you know?",
  "response": "Based on my experience, I'm proficient in Python, JavaScript, TypeScript...",
  "created_at": "2025-11-03T12:34:56.789012Z",
  "context_used": true,
  "relevant_chunks": 3
}
```

## Example Questions to Ask

- "What is your work experience?"
- "What programming languages do you know?"
- "Tell me about your projects"
- "What are your strongest skills?"
- "Where did you go to school?"
- "What kind of work are you looking for?"
- "What are your biggest achievements?"

## Architecture

### Components

1. **`models.py`**
   - `PortfolioData`: Stores text chunks with embeddings and categories

2. **`rag_utils.py`**
   - `chunk_text()`: Splits text into overlapping chunks
   - `generate_embedding()`: Converts text to vector embeddings
   - `cosine_similarity()`: Measures similarity between vectors
   - `retrieve_relevant_context()`: Finds most relevant chunks for a query
   - `load_portfolio_text()`: Loads text into database with embeddings

3. **`views.py`**
   - Enhanced `chat_with_openai()`: Now includes RAG retrieval before OpenAI call

4. **`management/commands/load_portfolio.py`**
   - Django command to load portfolio data

### RAG Workflow

```
User Question
    ↓
Convert to Embedding (384-dim vector)
    ↓
Search Database (Cosine Similarity)
    ↓
Retrieve Top 3 Chunks
    ↓
Build Context String
    ↓
Send to OpenAI (System Prompt + Context + User Question)
    ↓
AI Response (Context-Aware)
    ↓
Return to User
```

## Configuration

### Embedding Model
Current: `all-MiniLM-L6-v2` (384 dimensions, fast, accurate)

To change the model, edit `rag_utils.py`:
```python
_model = SentenceTransformer('your-model-name')
```

### Number of Retrieved Chunks
Default: Top 3 chunks

To change, edit `views.py`:
```python
context, relevant_chunks = retrieve_relevant_context(prompt, top_k=5)  # Change to 5
```

### Chunk Size
Default: 500 characters with 50-character overlap

To change, edit `rag_utils.py`:
```python
chunks = chunk_text(text, chunk_size=1000, overlap=100)
```

## Admin Panel

View and manage your portfolio data at `/admin/`:
- **Portfolio Data**: View/edit all chunks, filter by category
- **Chat History**: Review all conversations

## Updating Portfolio Data

### Add New Data
```python
from api.rag_utils import load_portfolio_text

text = "Your new portfolio information..."
load_portfolio_text(text, category='experience')
```

### Clear All Data
```bash
python manage.py shell
>>> from api.models import PortfolioData
>>> PortfolioData.objects.all().delete()
```

### Reload from File
```bash
python manage.py load_portfolio --clear --file portfolio.txt
```

## Performance Tips

1. **First request is slow**: The embedding model loads on first use (~2-3 seconds)
2. **Subsequent requests are fast**: Model stays in memory
3. **Database optimization**: Create index on category field for faster filtering
4. **Chunking strategy**: Adjust chunk size based on your content length

## Troubleshooting

### "No relevant context found"
- Make sure portfolio data is loaded: `python manage.py load_portfolio`
- Check data exists: Visit `/admin/` → Portfolio Data

### Slow response times
- First request initializes the embedding model (normal)
- Consider using a smaller embedding model for faster performance

### Out of memory
- Reduce chunk size in `rag_utils.py`
- Use a smaller embedding model

## Next Steps

1. **Customize** the sample portfolio data with your actual information
2. **Test** with various questions to see how well RAG retrieves context
3. **Refine** chunk sizes and categories based on your needs
4. **Deploy** with your updated portfolio data

## Files Modified/Created

- ✅ `api/models.py` - Added `PortfolioData` model
- ✅ `api/rag_utils.py` - RAG utility functions (NEW)
- ✅ `api/views.py` - Enhanced with RAG retrieval
- ✅ `api/admin.py` - Added `PortfolioData` admin
- ✅ `api/management/commands/load_portfolio.py` - Data loading command (NEW)
- ✅ `RAG_GUIDE.md` - This documentation (NEW)

Happy coding! 🚀
