## Importing libraries and files
import os
import re
from dotenv import load_dotenv
load_dotenv()

# from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader


search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))

# ---debug no three import toll and aign the api key to ork with you environ ment
## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool:
    @staticmethod
    async def read_data_tool(path='data/sample.pdf'):
        """
        Extracts and cleans text from a PDF file.

        Args:
            path (str, optional): Path to the PDF file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Extracted and cleaned financial document text.
        """
        loader = PyPDFLoader(path)
        docs = loader.load()

        # Join all page content
        full_report = "\n".join([doc.page_content.strip() for doc in docs])

        # Clean text (normalize spaces/newlines)
        cleaned_report = re.sub(r"\s+", " ", full_report).strip()

        return cleaned_report


## Creating Investment Analysis Tool
class InvestmentTool:
    @staticmethod
    async def analyze_investment_tool(financial_document_data: str):
        """
        Prepares financial document data for the agent to analyze investments.
        """
        processed_data = re.sub(r"\s+", " ", financial_document_data).strip()
        return processed_data

## Creating Risk Assessment Tool
class RiskTool:
    @staticmethod
    async def create_risk_assessment_tool(financial_document_data: str):
        """
        Prepares financial document data for the agent to analyze risks.
        """
        processed_data = re.sub(r"\s+", " ", financial_document_data).strip()
        return processed_data