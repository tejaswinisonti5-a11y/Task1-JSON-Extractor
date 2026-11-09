# Structured LLM Prompt Pipeline & JSON Extractor

## Project Description
This project is a Python-based application that uses Google's Gemini API to extract structured information from unstructured documents such as invoices and resumes.

It converts document text into structured JSON data and validates the extracted information using Pydantic.

## Features
- Extract information from invoices and resumes.
- Supports TXT and PDF documents.
- Uses Google Gemini API for information extraction.
- Parameterized prompt templates.
- Few-shot prompting for better extraction.
- Structured JSON output.
- Pydantic validation.
- Automatically saves extracted data as JSON files.

## Technologies Used
- Python
- Google Gemini API
- Pydantic
- Python-dotenv
- PyPDF
- Tkinter

## Project Files
- `app.py` – Main application.
- `prompts.py` – Prompt templates and few-shot examples.
- `invoice.txt` – Sample invoice document.
- `resume.txt` – Sample resume document.
- `.gitignore` – Excludes sensitive and unnecessary files.

## Installation

Install the required packages:

```bash
python -m pip install google-genai pydantic python-dotenv pypdf
```

## API Configuration

Create a `.env` file in the project folder and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload your actual API key to GitHub.

## How to Run

Run the following command:

```bash
python app.py
```

Select the document you want to process and choose the extraction type.

The application extracts the information, validates it, and saves the result as a JSON file.

## Project Objective
To build an LLM-powered pipeline that transforms unstructured documents into accurate, structured, and validated JSON data.
