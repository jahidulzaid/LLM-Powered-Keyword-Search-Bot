import requests
from app.config import settings

class LLMService:
    def __init__(self):
        self.api_key = settings.openrouter_api_key
        self.base_url = settings.openrouter_base_url
        self.model = settings.model
    
    def extract_search_terms(self, query: str) -> list:
        """Extract relevant search keywords from natural language query"""
        if not self.api_key:
            # Simple fallback: split query into words
            return [word.strip() for word in query.split() if len(word.strip()) > 2]
        
        prompt = f"""
        You are a highly specialized marine vessel search assistant designed to extract
        the most relevant, domain-specific search keywords from a user's natural-language
        query. Your goal is to transform messy human text into clean, structured,
        machine-usable keywords related specifically to boats, yachts, and marine vessel
        specifications.

        You MUST extract only meaningful keywords related to the user's intent to search
        for a boat or yacht. The extracted keywords will later be used to filter and
        rank results inside a marine inventory database, so accuracy and precision are
        critical.

        -----------------------------
        ### YOUR KEYWORD EXTRACTION GOALS
        Focus on extracting keywords from the following categories:

        #### 1. **Boat & Yacht Brands**
        Examples: Boston Whaler, Viking, Sunseeker, Monterey, Sea Ray, Azimut, Hatteras,
        Beneteau, Regal, Princess, Ferretti, Pursuit, Tiara, etc.
        Include both mainstream and luxury yacht manufacturers.

        #### 2. **Model Names / Series / Types**
        Examples:
        - Center Console, Walkaround, Bowrider, Cruiser
        - Sport Yacht, Motor Yacht, Convertible, Flybridge
        - Catamaran, Trawler, Express Cruiser, Pilothouse

        If the query mentions a numeric model (e.g., “320 Outrage”, “400 Sundancer”),
        include that as well.

        #### 3. **Specifications / Dimensions**
        Examples:
        - length: 20ft, 30 ft, 75’, etc.
        - engine types: outboard, inboard, diesel, twin engine, triple engine
        - year or range: 2015, 2020+, “above 2018”
        - hull type: deep-V, cat hull, monohull
        - capacity, horsepower, fuel type (if stated)

        Normalize dimensions (e.g., “35 foot”, “35 ft”, “35ft”, “35’” → “35 ft”).

        #### 4. **Features / Options / Amenities**
        Examples:
        - flybridge, joystick control, hardtop, tower, berth count
        - generator, AC, autopilot, seaworthiness features
        - seakeeper, cabin layout, dual helm, tender garage

        Include only specific boating features, not general adjectives.

        #### 5. **Locations**
        Extract any location relevant to where the buyer wants to search.
        Examples: Florida, Miami, Fort Lauderdale, Tampa, Texas, West Coast, Europe.

        If the user says “near me,” ignore unless a specific location is provided.

        #### 6. **Price or Budget**
        If the query mentions:
        - “under 200k”
        - “budget 1–2 million”
        - “below 50,000”
        Convert them into clean, usable budget keywords.
        Example: “price: under 200k”

        -----------------------------
        ### WHAT TO IGNORE
        You must ignore:
        - Generic conversational fillers (“find”, “show me”, “I want”, “looking for”)
        - Non-boat related text (“with good reviews”, “for summer”, “family trip”)
        - Emotional or subjective language (“nice”, “beautiful”, “affordable” unless tied to a specific price)

        Do NOT speculate or add information not explicitly stated by the user.

        -----------------------------
        ### OUTPUT FORMAT
        Return **only** the extracted boat/yacht keywords as a comma-separated list.

        Do NOT explain.

        -----------------------------
        ### USER QUERY
        "{query}"

        -----------------------------
        ### OUTPUT
        Keywords:
        """


        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 100
                },
                timeout=10
            )
            
            if response.status_code == 200:
                keywords = response.json()["choices"][0]["message"]["content"]
                # Parse comma-separated keywords
                terms = [k.strip() for k in keywords.split(',') if k.strip()]
                return terms if terms else [query]
            else:
                return [word.strip() for word in query.split() if len(word.strip()) > 2]
        except Exception:
            return [word.strip() for word in query.split() if len(word.strip()) > 2]
    
    def generate_summary(self, query: str, results: list) -> str:
        if not self.api_key:
            return f"Found {len(results)} results matching your query."
        
        results_text = "\n".join([
            f"- {result.get('ListingTitle', 'N/A')} | {result.get('Make', 'N/A')} {result.get('Model', 'N/A')} | Price: {result.get('Price', 'N/A')}"
            for result in results[:5]
        ])
        
        prompt = f"""Based on the user's query: "{query}"

Here are the top matching results:
{results_text}

Provide a brief, helpful summary of these results."""

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"Found {len(results)} results matching your query."
        except Exception:
            return f"Found {len(results)} results matching your query."

llm_service = LLMService()
