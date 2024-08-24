import pdfplumber

def pdf_to_text(pdf_path, txt_path):
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Open the text file to write the extracted text
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            # Loop through the pages in the PDF
            for page in pdf.pages:
                # Extract text from the page
                text = page.extract_text()
                # Write the text to the file
                if text:
                    txt_file.write(text)
                    txt_file.write('\n')  # Add a newline after each page

    print(f"Text extracted and saved to {txt_path}")

# Usage example
pdf_path = "input.pdf"  # Replace with your PDF file path
txt_path = "output.txt"  # Replace with your desired output TXT file path
pdf_to_text(pdf_path, txt_path)
