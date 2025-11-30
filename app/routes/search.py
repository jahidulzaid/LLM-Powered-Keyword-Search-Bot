from fastapi import APIRouter, HTTPException
from app.models import SearchRequest, SearchResponse
from app.data_loader import data_loader
from app.llm_service import llm_service

router = APIRouter()

@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    try:
        # Extract search terms from natural language query
        search_terms = llm_service.extract_search_terms(request.query)
        
        # Search using extracted terms
        results_df = data_loader.search(request.query, search_terms)
        
        if results_df.empty:
            return SearchResponse(
                query=request.query,
                results=[],
                summary=f"No results found. Searched for: {', '.join(search_terms)}"
            )
        
        results = results_df.head(50).to_dict('records')
        summary = llm_service.generate_summary(request.query, results)
        
        return SearchResponse(
            query=request.query,
            results=results,
            summary=summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
