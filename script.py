import os
import shutil
import requests
from dotenv import load_dotenv
import docx
from docx import Document
from translate_prompt import extract_text_with_structure, create_translation_prompt
import re

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment variables
api_key = os.getenv("GEMINI_API_KEY")

def translate_texts():
    # Define your input parameters
    source_lang = "English"  # example: English
    target_lang = "Traditional Chinese"  # example: Traditional Chinese
    country = "Taiwan"
    source_folder = "original_chunks"
    destination_folder = "translated_chunks"
    merged_docx_file = os.path.join(destination_folder, "translated.docx")

    # Ensure the destination directory exists
    os.makedirs(destination_folder, exist_ok=True)

    # Create a new document for the merged translated content
    merged_translated_doc = Document()

    # Iterate over all .docx files in the source folder
    for filename in sorted(os.listdir(source_folder)):
        if filename.endswith(".docx"):
            source_docx_file = os.path.join(source_folder, filename)
            destination_docx_file = os.path.join(destination_folder, filename)
            print(f"Processing {source_docx_file}")

            # Extract text with structure
            elements = extract_text_with_structure(source_docx_file)

            # Check if the extracted text is empty or contains only line breaks
            text_content = "".join(element[1] for element in elements).strip()
            if not text_content:
                print(f"Skipping {source_docx_file} as it contains only line breaks or is empty.")
                # Copy the original file to the translated_chunks folder
                shutil.copy(source_docx_file, destination_docx_file)
                # Append the original content to the merged document
                append_original_to_docx(merged_translated_doc, source_docx_file)
                continue

            # Create the translation prompt
            translation_prompt = create_translation_prompt(source_lang, target_lang, country, elements)

            # Setup the URL and headers for the API request
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
            headers = {
                "Content-Type": "application/json"
            }
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": translation_prompt
                            }
                        ]
                    }
                ]
            }

            # Send the request to the API
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                response_data = response.json()
                # Print the entire response to see its structure
                print("Response JSON:", response_data)

                # Extract the translated text from the response
                candidates = response_data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        translated_text = parts[0].get("text", "No translated text found")
                        # Clean the translated text by removing the <SOURCE_TEXT> tags
                        translated_text = re.sub(r'<SOURCE_TEXT>|</SOURCE_TEXT>', '', translated_text).strip()
                    else:
                        translated_text = "No translated text found"
                else:
                    translated_text = "No translated text found"

                # Save each translated chunk to its own file
                save_translation_to_docx(source_docx_file, translated_text, elements, destination_docx_file)

                # Append the translated text to the merged document
                append_translation_to_docx(merged_translated_doc, translated_text, elements)
            else:
                print(f"Error: {response.status_code} - {response.text}")

    # Save the merged translated document
    merged_translated_doc.save(merged_docx_file)
    print(f"All translations saved to {merged_docx_file}")

def save_translation_to_docx(source_docx_file, translated_text, elements, destination_docx_file):
    translated_paragraphs = translated_text.split('\n')
    
    # Create a new docx document for the translation
    translated_doc = Document()
    
    # Map translated text to the original elements structure
    for element, translated_para in zip(elements, translated_paragraphs):
        if element[0] == 'paragraph':
            new_para = translated_doc.add_paragraph(style=element[2])
            new_run = new_para.add_run(translated_para)
            copy_run_formatting(new_run, element[3][0] if element[3] else None)
        elif element[0] == 'cell':
            new_table = translated_doc.add_table(rows=1, cols=1)
            cell = new_table.cell(0, 0)
            cell.text = translated_para
            for run in element[3]:
                new_run = cell.paragraphs[0].add_run(run.text)
                copy_run_formatting(new_run, run)

    # Save the translated document
    translated_doc.save(destination_docx_file)
    print(f"Translated chunk saved to {destination_docx_file}")

def append_translation_to_docx(merged_doc, translated_text, elements):
    translated_paragraphs = translated_text.split('\n')

    # Map translated text to the original elements structure
    for element, translated_para in zip(elements, translated_paragraphs):
        if element[0] == 'paragraph':
            new_para = merged_doc.add_paragraph(style=element[2])
            new_run = new_para.add_run(translated_para)
            copy_run_formatting(new_run, element[3][0] if element[3] else None)
        elif element[0] == 'cell':
            new_table = merged_doc.add_table(rows=1, cols=1)
            cell = new_table.cell(0, 0)
            cell.text = translated_para
            for run in element[3]:
                new_run = cell.paragraphs[0].add_run(run.text)
                copy_run_formatting(new_run, run)

def append_original_to_docx(merged_doc, source_docx_file):
    original_doc = Document(source_docx_file)
    for paragraph in original_doc.paragraphs:
        new_para = merged_doc.add_paragraph(style=paragraph.style)
        for run in paragraph.runs:
            new_run = new_para.add_run(run.text)
            copy_run_formatting(new_run, run)

def copy_run_formatting(new_run, original_run):
    if original_run:
        new_run.bold = original_run.bold
        new_run.italic = original_run.italic
        new_run.underline = original_run.underline
        new_run.font.size = original_run.font.size
        new_run.font.color.rgb = original_run.font.color.rgb

if __name__ == "__main__":
    translate_texts()
