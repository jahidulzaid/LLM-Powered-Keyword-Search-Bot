import pandas as pd
from app.config import settings

class DataLoader:
    def __init__(self):
        self.df = None
        self.load_data()
    
    def load_data(self):
        try:
            self.df = pd.read_csv(settings.csv_file_path)
        except Exception as e:
            raise Exception(f"Failed to load CSV: {str(e)}")
    
    def search(self, query: str, search_terms: list = None) -> pd.DataFrame:
        if self.df is None:
            return pd.DataFrame()
        
        # Use provided search terms or fallback to original query
        terms = search_terms if search_terms else [query]
        
        # Search for ALL terms (AND logic) - each result must contain all search terms
        masks = []
        for term in terms:
            term_lower = term.lower().strip()
            if term_lower:
                mask = self.df.astype(str).apply(
                    lambda row: any(term_lower in str(cell).lower() for cell in row), 
                    axis=1
                )
                masks.append(mask)
        
        # Combine masks with AND logic - all terms must be present
        if masks:
            combined_mask = masks[0]
            for mask in masks[1:]:
                combined_mask = combined_mask & mask
            return self.df[combined_mask]
        
        return pd.DataFrame()

data_loader = DataLoader()
