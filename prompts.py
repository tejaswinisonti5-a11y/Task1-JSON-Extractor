def invoice_prompt(invoice_text):
    return f"""
You are an invoice information extraction assistant.

Example 1:

Input:
Invoice Number: INV001
Customer Name: Ravi
Date: 01-11-2026
Product: Mouse
Quantity: 2
Total Amount: 1000

Expected JSON:
{{
    "invoice_number": "INV001",
    "customer_name": "Ravi",
    "date": "01-11-2026",
    "product": "Mouse",
    "quantity": 2,
    "total_amount": 1000
}}

Example 2:

Input:
Invoice Number: INV002
Customer Name: Priya
Date: 05-11-2026
Product: Keyboard
Quantity: 1
Total Amount: 1500

Expected JSON:
{{
    "invoice_number": "INV002",
    "customer_name": "Priya",
    "date": "05-11-2026",
    "product": "Keyboard",
    "quantity": 1,
    "total_amount": 1500
}}

Now extract information from this invoice.

Rules:
1. Extract only available information.
2. Do not guess missing information.
3. Return valid structured JSON.

Invoice Text:
{invoice_text}
"""

def resume_prompt(resume_text):
    return f"""
You are a resume information extraction assistant.

Extract the following information:
- full_name
- email
- phone
- skills
- education
- experience

Example:

Input:
Name: Ravi Kumar
Email: ravi@gmail.com
Phone: 9876543210
Skills: Python, Java
Education: B.Tech
Experience: Fresher

Expected JSON:
{{
    "full_name": "Ravi Kumar",
    "email": "ravi@gmail.com",
    "phone": "9876543210",
    "skills": ["Python", "Java"],
    "education": "B.Tech",
    "experience": "Fresher"
}}

Rules:
1. Extract only available information.
2. Do not guess missing information.
3. Use an empty string for missing text fields.
4. Use an empty list for missing skills.
5. Return valid structured JSON.

Resume Text:
{resume_text}
"""
