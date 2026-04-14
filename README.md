
# AI Test Case Generator

An AI-powered tool that generates structured software test cases from natural language requirements using Large Language Models (LLMs).

Now enhanced with Retrieval-Augmented Generation (RAG), enabling more context-aware, relevant, and realistic test case generation.

The project provides both a CLI interface and a web-based UI built with Streamlit, allowing testers and developers to quickly generate functional and non-functional test cases and export them in a structured format.

---

## 📈 Evolution

- V1: Basic LLM-based test case generation  
- V2: Introduced RAG for context-aware generation  
- V3: Improved retrieval precision and refactored architecture 
- V4: Retrieval Evaluation, Query Rewriting, and Alignment Improvements for Reliable RAG Systems

---

## Features

- Generate test cases from plain English requirements
- Structured output using Pydantic models
- CLI interface for quick generation
- Streamlit web UI for interactive usage
- Export generated test cases to CSV
- Modular architecture for easy extension
- RAG-based retrieval using FAISS for context-aware generation
- Semantic search over existing test cases

---

## 📂 Sample Dataset

A sample dataset is included in the `data/` directory to demonstrate RAG-based retrieval.

- File: `data/sample_testcases.csv`
- Contains structured test cases used for semantic search
- You can replace this file with your own test case repository

Note: Larger or private datasets can be excluded using `.gitignore`.

---

## 🚀 Update (V2 - RAG Integration)

This version introduces Retrieval-Augmented Generation (RAG) to improve the quality and relevance of generated test cases.

### How it works

Requirement  
→ Retrieve similar test cases using FAISS  
→ Inject them into the prompt  
→ Generate context-aware test cases  

### Improvements

- More realistic and domain-specific scenarios  
- Better coverage of edge cases (e.g., invalid payment, cancellation)  
- Reduced generic outputs  

### Example

Input:  
User pays using PayPal  

Before (V1):  
- Generic payment-related test cases  

After (V2):  
- PayPal-specific scenarios such as valid payment, cancellation, insufficient funds  

### Notes

- A sample CSV dataset is provided in `/data` for quick testing
- ~300 test cases are used for retrieval  
- Embeddings are generated using sentence-transformers  
- FAISS index is currently built at runtime  
- Future improvement: persist index to disk for faster startup  

---

## 🚀 Update (V3 - Retrieval Improvements & Architecture Refactor)

Enhanced retrieval accuracy and improved system design and modularity.

### Retrieval Enhancements

- Implemented embedding normalization to enable cosine similarity with FAISS
- Added similarity threshold filtering to improve relevance
- Improved retrieval consistency and reduced noisy results

### Architecture Improvements

- Refactored RAG pipeline into `RAGEngine` class
- Introduced `TestCaseGenerator` for orchestration
- Improved modularity for CLI and UI reuse

---

## 🚀 Update (V4 - Retrieval Alignment, Evaluation & Query Rewriting)

This version focuses on improving retrieval reliability and alignment between user queries and the knowledge base.

### 🔍 Evaluation Framework

Introduced a retrieval evaluation pipeline to measure system performance and identify failure patterns.

- Built a ground-truth dataset mapping queries → expected test cases
- Measured retrieval using:
  - Hit@K (whether correct document is retrieved)
  - Recall@K (coverage for multi-document queries)
- Logged retrieval outputs (indices, scores, distances) for analysis

This helped uncover hidden issues where outputs looked correct but retrieval was incorrect.

---

### 🔄 Query Rewriting (Alignment Layer)

Added a query rewriting layer to bridge the gap between user language and document language.

- Generates:
  - Canonical query (QA-style)
  - Multiple semantic expansions
- Uses validation logic (keyword overlap) to filter weak rewrites
- Improves retrieval consistency across different query phrasings

Insight:
> Retrieval failures were often caused by language mismatch, not embeddings.

---

### 🧩 Knowledge Base Segmentation

Introduced test type segmentation to improve retrieval precision.

- Users explicitly select:
  - Functional
  - Non-functional (e.g., security, performance)
- Retrieval is performed on a filtered subset of the dataset

Benefits:

- Reduced search space
- Improved semantic alignment
- Reduced cross-domain noise (e.g., security vs functional mix-ups)

---

### 🧠 Key Learnings

- Retrieval issues are often **alignment problems**, not embedding problems
- More data does not fix retrieval — better structure does
- Evaluation is not just a metric — it is a diagnostic tool
- Consistency across rewrites is a stronger signal than single-query similarity

---

## 🔄 Pipeline Architecture

The system uses a Retrieval-Augmented Generation (RAG) pipeline:

Requirement → Query Rewriting → Filtered Retrieval (by test_type) → FAISS → Aggregation → Prompt → LLM

---

## Project Architecture

AI Test Case Generator

├── cli
│   └── cli.py                    # CLI interface for user input and execution
│
├── core
│   └── testcase_generator.py    # LLM orchestration and test case generation
│
├── eval
│   ├── retrieval
│   │   ├── retrieval_eval.py            # Retrieval evaluation logic (Hit@K, Recall@K)
│   │   └── rag_retrieval_eval_dataset.json  # Ground truth dataset for retrieval eval
│   │
│   └── output
│       └── rag_output_eval_dataset.json     # Dataset for output-level evaluation
│
├── rag
│   ├── documents.py             # Creates and manages test case documents
│   ├── rag_engine.py            # Embedding generation and FAISS retrieval
│   ├── rewriter.py              # Query rewriting (canonical + semantic expansions)
│
├── models
│   └── pydantic_models.py       # Structured schema for test case output
│
├── data
│   └── sample_testcases.csv     # Dataset used for RAG retrieval
│
├── ui
│   └── app.py                  # Streamlit web application
│
├── utils
│   ├── export_csv.py           # Export generated test cases to CSV
│   └── test_type_mapper.py     # Maps and filters test types (functional / non-functional)
│
├── config.py                   # Configuration and environment setup
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Ignored files

---

## Installation

Clone the repository:

git clone https://github.com/vamsi4593/ai-testcase-generator.git  
cd ai-testcase-generator

Create a virtual environment:

python -m venv .venv

Activate it:

Windows  
.venv\Scripts\activate

Mac/Linux  
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Ensure the sample dataset is present in the `data/` directory before running the application.

---

## Code Quality

This project follows Python PEP8 conventions and uses modern linting and formatting tools to maintain consistent code quality.

Tools used:

- **ruff** – fast Python linter for detecting style issues and unused imports
- **black** – automatic code formatter for consistent styling

Run locally:

bash
ruff check .
black .

---

## Environment Setup

Create a file:

project.env

Add your OpenAI API key:

OPENAI_API_KEY=your_api_key_here

---

## Running the CLI

Run the CLI tool:

python cli/cli.py

Example:

Enter requirement: User should be able to log in using email and password

The tool will generate structured test cases and optionally export them to CSV.

---

## Running the Web UI

Launch the Streamlit interface:

streamlit run ui/app.py

Open the provided URL in your browser.

You can:

- Enter requirements
- Generate test cases
- View them in structured tables
- Download them as CSV

---

## Example Output

TC001 - Validate login with valid credentials

1. Navigate to login page  
Expected Result: Login page is displayed

2. Enter valid username and password  
Expected Result: Credentials are accepted

3. Click login button  
Expected Result: User is redirected to dashboard

---

## Roadmap

Planned improvements:

- Improve RAG with better filtering and reranking
- Persist FAISS index for faster retrieval
- Generate executable automation scripts from test cases
- Integration with test management tools (Jira, TestRail, Zephyr)
- Test data generation
- API interface
- Enhanced UI and UX

---

## Author

Built as part of a personal project exploring AI-assisted software testing tools and developer productivity automation.
