
# AI Test Case Generator

An AI-powered tool that generates structured software test cases from natural language requirements using Large Language Models (LLMs).

The project provides both a CLI interface and a web-based UI built with Streamlit, enabling testers and developers to quickly generate functional and non-functional test cases and export them in a structured format.

---

## Features

- Generate test cases from plain English requirements
- Structured output using Pydantic models
- CLI interface for quick generation
- Streamlit web UI for interactive usage
- Export generated test cases to CSV
- Modular architecture for easy extension
- Designed to evolve into a RAG-powered QA assistant

---

## Project Architecture

AI Test Case Generator

├── cli
│   └── cli.py              # CLI interface
│
├── core
│   └── TCGenerator.py      # LLM interaction and test case generation
│
├── models
│   └── PydanticModels.py   # Structured output models
│
├── utils
│   └── ExportToCSV.py      # CSV export utilities
│
├── ui
│   └── app.py              # Streamlit web application
│
├── config.py               # Environment configuration
├── requirements.txt
└── .gitignore

---

## Installation

Clone the repository:

git clone https://github.com/YOUR_USERNAME/ai-testcase-generator.git  
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

- Retrieval-Augmented Generation (RAG) for smarter test case generation
- Integration with test management tools (Jira, TestRail, Zephyr)
- Test data generation
- API interface
- Enhanced UI and UX

---

## License

This project is licensed under the MIT License.

---

## Author

Built as part of a personal project exploring AI-assisted software testing tools and developer productivity automation.
