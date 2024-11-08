import pandas as pd
import uuid

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.portfolio_data = []

    def load_portfolio(self):
        for _, row in self.data.iterrows():
            self.portfolio_data.append({
                "techstack": row["Techstack"],
                "links": row["Links"],
                "id": str(uuid.uuid4())
            })

    def query_links(self, skills):
        # Replace the vector-based query with a basic text-based matching
        results = []
        for entry in self.portfolio_data:
            if skills.lower() in entry["techstack"].lower():
                results.append(entry["links"])
                if len(results) == 2:  # Limit results as per original function
                    break
        return results
