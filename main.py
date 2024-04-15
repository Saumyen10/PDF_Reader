import PyPDF2
import re
import pandas as pd

def extract_contacts(cv_text):
    # Email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    
    # Phone number regex pattern
    phone_pattern = r'\b(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b'
    
    # Extract emails using regex
    emails = re.findall(email_pattern, cv_text)
    
    # Extract phone numbers using regex
    phone_numbers = re.findall(phone_pattern, cv_text)
    
    return {"Emails": emails, "Phone Numbers": phone_numbers}

pdf_file = PyPDF2.PdfReader("")  #PDF File name
cv_text=""

for page_number in range(len(pdf_file.pages)):
    page = pdf_file.pages[page_number]
    page_text = page.extract_text()
    if page_text:  # Check if the extracted text is not None
        cv_text += page_text


# Check if cv_text is not empty before extracting contacts
if cv_text:
    contacts = extract_contacts(cv_text)
    emails = contacts["Emails"]
    phone_numbers = contacts["Phone Numbers"]
    print("Emails:", emails)
    print("Phone Numbers:", phone_numbers)
else:
    print("No text extracted from the PDF file.")

# Ensure the lengths of emails and phone numbers lists are the same
max_length = max(len(emails), len(phone_numbers))
emails += [""] * (max_length - len(emails))
phone_numbers += [""] * (max_length - len(phone_numbers))

# Save extracted contacts to an Excel file
df = pd.DataFrame({"Emails": emails, "Phone Numbers": phone_numbers})
df.to_excel("contacts.xlsx", index=False)

print("Extracted contacts saved to contacts.xlsx")
