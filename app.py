
import os
from pathlib import Path
from tkinter import Tk, filedialog, simpledialog, messagebox

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, field_validator
from pypdf import PdfReader

from prompts import invoice_prompt, resume_prompt


# STEP 1: Load API key

env_path = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found in .env file")

client = genai.Client(api_key=api_key)


# STEP 2: Invoice schema

class Invoice(BaseModel):
    invoice_number: str
    customer_name: str
    date: str
    product: str
    quantity: int
    total_amount: float

    @field_validator("quantity")
    @classmethod
    def check_quantity(cls, value):
        if value <= 0:
            raise ValueError("Quantity must be greater than zero")
        return value

    @field_validator("total_amount")
    @classmethod
    def check_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be greater than zero")
        return value


# STEP 3: Resume schema

class Resume(BaseModel):
    full_name: str
    email: str
    phone: str
    skills: list[str]
    education: str
    experience: str


# STEP 4: Read TXT or PDF file

def read_document(file_path):

    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    else:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()


# STEP 5: Upload document

def upload_file():

    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Invoice or Resume",
        filetypes=[
            ("Supported Documents", "*.txt *.pdf"),
            ("Text Files", "*.txt"),
            ("PDF Files", "*.pdf")
        ]
    )

    if not file_path:
        root.destroy()
        return None, None, None

    choice = simpledialog.askinteger(
        "Document Type",
        "Enter 1 for Invoice or 2 for Resume:",
        minvalue=1,
        maxvalue=2
    )

    if choice is None:
        root.destroy()
        return None, None, None

    try:
        document_text = read_document(file_path)
        root.destroy()

        if not document_text.strip():
            print("The selected document contains no readable text.")
            return None, None, None

        return document_text, choice, file_path

    except Exception as e:
        root.destroy()
        print("File reading error:", e)
        return None, None, None


# STEP 6: Process document

document_text, choice, file_path = upload_file()

if document_text:

    if choice == 1:
        prompt = invoice_prompt(document_text)
        schema = Invoice
        document_name = "INVOICE"

    else:
        prompt = resume_prompt(document_text)
        schema = Resume
        document_name = "RESUME"

    try:
        print("\nProcessing document...")

        # Send document to Gemini

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": schema
            }
        )

        # Validate JSON using Pydantic

        result = schema.model_validate_json(response.text)

        # Display result

        json_output = result.model_dump_json(indent=4)

        print(f"\n========== {document_name} DETAILS ==========")
        print(json_output)

        # Save JSON automatically

        output_path = Path(file_path).with_name(
            Path(file_path).stem + "_extracted.json"
        )

        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write(json_output)

        print("\nDocument extracted and validated successfully!")
        print("JSON saved at:", output_path)

        messagebox.showinfo(
            "Success",
            f"{document_name} extracted successfully!\n\nJSON saved at:\n{output_path}"
        )

    except Exception as e:
        print("\nExtraction or validation error:", e)

else:
    print("\nNo document selected or document reading cancelled.")
