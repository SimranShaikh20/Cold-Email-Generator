import streamlit as st
import pandas as pd
import uuid
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from utils import clean_text


class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.portfolio_data = []

    def load_portfolio(self):
        # Loading portfolio data from CSV into a list of dictionaries
        for _, row in self.data.iterrows():
            self.portfolio_data.append({
                "techstack": row["Techstack"],
                "links": row["Links"],
                "id": str(uuid.uuid4())
            })

    def query_links(self, skills):
        # Basic text-based matching for skills
        results = []
        for entry in self.portfolio_data:
            if skills.lower() in entry["techstack"].lower():
                results.append(entry["links"])
                if len(results) == 2:
                    break
        return results


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-43832")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Load and clean the content from the provided URL
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            
            # Load portfolio data if not already loaded
            portfolio.load_portfolio()
            
            # Extract job information and generate email
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                
                # Join skills into a single string for text-based querying
                skills_str = ' '.join(skills)
                links = portfolio.query_links(skills_str)
                
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
