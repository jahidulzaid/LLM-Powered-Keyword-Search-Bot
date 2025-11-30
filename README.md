# AI Search Bot

A simple FastAPI-based search bot that searches through a boat listing CSV dataset using OpenRouter AI.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure API key:**
Create a `.env` file in the root directory:
```bash
OPENROUTER_API_KEY=your_openrouter_api_key
```

3. **Run the application:**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### `GET /`
Health check endpoint

### `POST /api/search`
Search the dataset with a query

**Request Body:**
```json
{
  "query": "boston whaler"
}
```

**Response:**
```json
{
  "query": "boston whaler",
  "results": [...],
  "summary": "AI-generated summary of results"
}
```

## Testing

Visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

```
.
├── main.py                 # Application entry point
├── app/
│   ├── config.py          # Configuration settings
│   ├── models.py          # Pydantic models
│   ├── data_loader.py     # CSV data loading and search
│   ├── llm_service.py     # OpenRouter AI integration
│   └── routes/
│       └── search.py      # Search endpoint
├── sources.csv            # Dataset
├── requirements.txt       # Dependencies
└── .env                   # Environment variables (create this)
```
