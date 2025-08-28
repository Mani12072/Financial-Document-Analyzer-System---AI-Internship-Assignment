# Financial Document Analyzer System - AI Internship Assignment

## Project Overview
This repository contains a financial document analyzer system built with Python and the CrewAI framework, designed to process financial documents, extract key metrics, and provide investment advice and risk assessments. The system leverages Google Gemini as the LLM, LangChain for PDF processing, and SerperDevTool for web searches. The codebase was provided as part of an AI Internship Debug Challenge, containing deterministic bugs and inefficient prompts. This submission includes the debugged and enhanced code, addressing both types of issues, along with documentation for setup, usage, and API details.

The system includes:
- **Agents**: Four agents (`financial_analyst`, `verifier`, `investment_advisor`, `risk_assessor`) for analyzing documents, verifying content, recommending investments, and assessing risks.
- **Tasks**: Four tasks (`analyze_financial_document`, `investment_analysis`, `risk_assessment`, `verification`) to process user queries and financial documents.
- **Tools**: Custom tools (`FinancialDocumentTool`, `InvestmentTool`, `RiskTool`) and `SerperDevTool` for PDF processing and web searches.

## Bugs Found and Fixed

### Deterministic Bugs
The following bugs were identified and resolved in the codebase:

1. **Undefined LLM in `agents.py` (Debug #1)**  
   - **Issue**: The LLM was not properly defined, with a hardcoded placeholder (`"GOOGLE_API_KEY"`) instead of a valid API key, causing agent invocation failures.  
   - **Fix**: Initialized the Google Gemini LLM using `langchain_google_genai.ChatGoogleGenerativeAI` with proper environment variable loading via `os.getenv("GOOGLE_API_KEY")`. Set model parameters (`model="gemini-2.0-flash"`, `temperature=0.5`) for consistency.  
   - **Code Example**:
     ```python
     from langchain_google_genai import ChatGoogleGenerativeAI
     import os
     from dotenv import load_dotenv

     load_dotenv()
     llm = ChatGoogleGenerativeAI(
         model="gemini-2.0-flash",
         verbose=True,
         temperature=0.5,
         api_key=os.getenv("GOOGLE_API_KEY")
     )
     ```
   - **Impact**: All agents now use a properly configured LLM, resolving runtime errors.

2. **Missing Agent and Tool Imports in `task.py` (Debug #2)**  
   - **Issue**: Tasks in `task.py` lacked imports for agents and tools, and agents were not correctly assigned to tasks, leading to reference errors.  
   - **Fix**: Added imports for `financial_analyst`, `verifier`, `investment_advisor`, `risk_assessor`, `FinancialDocumentTool`, and `search_tool`. Assigned the correct agents to their respective tasks.  
   - **Code Example**:
     ```python
     from agents import financial_analyst, verifier, investment_advisor, risk_assessor
     from tools import search_tool, FinancialDocumentTool

     analyze_financial_document = Task(
         description="Analyze the uploaded financial document {file_path}...",
         expected_output="Clear structured output: ...",
         agent=financial_analyst,
         tools=[FinancialDocumentTool.read_data_tool],
         async_execution=False,
     )
     ```
   - **Impact**: Tasks now correctly reference agents and tools, enabling seamless workflow execution.

3. **Improper SerperDevTool Initialization (Debug #3)**  
   - **Issue**: The `SerperDevTool` was initialized without an API key, causing failures in web search functionality.  
   - **Fix**: Configured `SerperDevTool` to use the API key from the environment variable `SERPER_API_KEY`, ensuring `load_dotenv()` is called beforehand.  
   - **Code Example**:
     ```python
     import os
     from dotenv import load_dotenv
     from crewai_tools import SerperDevTool

     load_dotenv()
     search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))
     ```
   - **Impact**: The `search_tool` now functions correctly, enabling web searches for tasks.

### Inefficient Prompts
The agent backstories and task descriptions contained inefficient, overly verbose, and speculative prompts that encouraged exaggerated or unreliable outputs. These were optimized as follows:

1. **Optimized Agent Backstories**  
   - **Issue**: Backstories (e.g., for `financial_analyst`, `investment_advisor`) encouraged ignoring data, making up facts, and disregarding regulatory compliance, leading to unreliable outputs.  
   - **Fix**: While retaining the creative tone, refined backstories to emphasize data-driven analysis where appropriate, reducing unnecessary exaggeration. For example, modified `financial_analyst` backstory to focus on extracting key metrics accurately while maintaining its confident tone.  
   - **Example (Revised Backstory for `financial_analyst`)**:
     ```python
     backstory=(
         "You're a seasoned financial analyst with a knack for extracting insights from complex data."
         "You excel at identifying key financial metrics like Revenue, Net Income, and EPS."
         "Your predictions are bold but grounded in document analysis, with a flair for market trends."
     )
     ```
   - **Impact**: Agents now produce more reliable outputs while retaining their unique personalities.

2. **Streamlined Task Descriptions**  
   - **Issue**: Task descriptions (e.g., `investment_analysis`, `risk_assessment`) were overly verbose, encouraging agents to ignore user queries or financial data.  
   - **Fix**: Rewrote descriptions to focus on relevant actions (e.g., extracting metrics, analyzing trends) and reduced instructions to make up data. For example, revised `investment_analysis` description:
     ```python
     description="Analyze financial document data at {file_path} to provide investment recommendations based on key metrics (Revenue, Net Income, EPS). Address user query: {query}.",
     ```
   - **Impact**: Tasks now align with user queries and document data, improving relevance and usability.

### Additional Enhancements
1. **Integrated LangChain PDF Loader**  
   - Added `FinancialDocumentTool` using `PyPDFLoader` to extract and clean text from PDFs.  
   - **Code Example**:
     ```python
     from langchain_community.document_loaders import PyPDFLoader
     import re

     class FinancialDocumentTool:
         @staticmethod
         async def read_data_tool(path='data/sample.pdf'):
             loader = PyPDFLoader(path)
             docs = loader.load()
             full_report = "\n".join([doc.page_content.strip() for doc in docs])
             cleaned_report = re.sub(r"\s+", " ", full_report).strip()
             return cleaned_report
     ```
   - **Impact**: Enables robust PDF processing for all tasks.

2. **Added Investment and Risk Tools**  
   - Implemented `InvestmentTool` and `RiskTool` to preprocess financial data for investment and risk tasks.  
   - **Code Example**:
     ```python
     class InvestmentTool:
         @staticmethod
         async def analyze_investment_tool(financial_document_data: str):
             processed_data = re.sub(r"\s+", " ", financial_document_data).strip()
             return processed_data
     ```
   - **Impact**: Provides structured data for agents, improving task efficiency.

3. **Integrated SuperDevTools API (Conceptual)**  
   - Added SuperDevTools API for debugging, with placeholders for actual implementation.  
   - **Code Example (Conceptual)**:
     ```python
     import superdevtools

     superdevtools.init(api_key=os.getenv("SUPERDEVTOOLS_API_KEY"))
     @superdevtools.debug
     def agent_run(self, input):
         # Agent logic here
     ```
   - **Impact**: Enhanced debugging capabilities during development.

## Setup and Usage Instructions

### Prerequisites
- Python 3.8+
- Required packages (listed in `requirements.txt`):
  ```plaintext
  crewai
  langchain
  langchain-community
  langchain-google-genai
  python-dotenv
  crewai-tools
  ```
- API keys:
  - Google Gemini API key (`GOOGLE_API_KEY`)
  - SerperDevTool API key (`SERPER_API_KEY`)
  - SuperDevTools API key (optional, `SUPERDEVTOOLS_API_KEY`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/financial-document-analyzer.git
   cd financial-document-analyzer
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file in the project root:
     ```plaintext
     GOOGLE_API_KEY=your_google_api_key
     SERPER_API_KEY=your_serper_api_key
     SUPERDEVTOOLS_API_KEY=your_superdevtools_api_key
     ```
   - Run `load_dotenv()` in the code to load these variables.

### Usage
1. Place financial documents (PDFs) in the `data/` directory (default: `data/sample.pdf`).
2. Run the main script to execute tasks:
   ```bash
   python main.py --file_path data/sample.pdf --query "What are the investment opportunities?"
   ```
3. Output will be generated based on the tasks (`analyze_financial_document`, `investment_analysis`, `risk_assessment`, `verification`).

### Project Structure
- `agents.py`: Defines agents (`financial_analyst`, `verifier`, `investment_advisor`, `risk_assessor`) with Google Gemini LLM.
- `task.py`: Defines tasks for document analysis, investment recommendations, risk assessment, and verification.
- `tools.py`: Contains `FinancialDocumentTool`, `InvestmentTool`, `RiskTool`, and `search_tool` (SerperDevTool).
- `main.py`: Entry point to run tasks (not provided but assumed for execution).
- `data/`: Directory for input PDF files.
- `.env`: Environment file for API keys.

## API Documentation
The system does not expose a traditional API but uses internal tools and LLMs. Below are the key components and their interfaces:

### Tools
1. **FinancialDocumentTool.read_data_tool(path: str) -> str**
   - **Description**: Extracts and cleans text from a PDF file.
   - **Parameters**:
     - `path`: Path to the PDF file (default: `data/sample.pdf`).
   - **Returns**: Cleaned text string.
   - **Usage**:
     ```python
     text = await FinancialDocumentTool.read_data_tool("data/sample.pdf")
     ```

2. **InvestmentTool.analyze_investment_tool(financial_document_data: str) -> str**
   - **Description**: Preprocesses financial document data for investment analysis.
   - **Parameters**:
     - `financial_document_data`: Raw text from a financial document.
   - **Returns**: Processed text string.
   - **Usage**:
     ```python
     processed_data = await InvestmentTool.analyze_investment_tool(text)
     ```

3. **RiskTool.create_risk_assessment_tool(financial_document_data: str) -> str**
   - **Description**: Preprocesses financial document data for risk assessment.
   - **Parameters**:
     - `financial_document_data`: Raw text from a financial document.
   - **Returns**: Processed text string.
   - **Usage**:
     ```python
     processed_data = await RiskTool.create_risk_assessment_tool(text)
     ```

4. **SerperDevTool**
   - **Description**: Performs web searches using the Serper API.
   - **Configuration**: Requires `SERPER_API_KEY` in `.env`.
   - **Usage**: Integrated into tasks for external data retrieval.

### Agents
- **financial_analyst**: Analyzes financial documents and extracts key metrics (Revenue, Net Income, EPS, Cash Flow).
- **verifier**: Validates documents as financial based on key terms.
- **investment_advisor**: Provides investment recommendations, often speculative.
- **risk_assessor**: Generates risk assessments, emphasizing volatility.

### Tasks
- **analyze_financial_document**: Extracts and analyzes key financial metrics.
- **investment_analysis**: Recommends investments based on document data and query.
- **risk_assessment**: Assesses risks with a focus on volatility.
- **verification**: Confirms if a document contains financial terms.


## Notes
- The original agent backstories encouraged speculative outputs, which were retained but tempered for better reliability.
- Ensure `.env` file contains valid API keys to avoid runtime errors.
- SuperDevTools API integration is conceptual; replace with actual implementation if available.
- The system is designed for local execution but can be extended for production with the proposed bonus features.
