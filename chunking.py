from docx import Document
import os
import shutil
from copy import deepcopy

def append_element(new_doc, element):
    """
    Helper function to append an element along with its formatting.
    """
    try:
        new_element = deepcopy(element)
        new_doc._element.body.append(new_element)
    except Exception as e:
        print(f"Error appending element: {e}")

def estimate_tokens(text):
    """
    Estimate the number of tokens in a given text. This is a basic approximation,
    considering each word as a token.
    """
    # Simple estimation: 1 token per word
    return len(text.split())

def chunk_docx_by_tokens(input_file, output_dir, max_tokens=1500):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        shutil.rmtree(output_dir)  # Clear the directory if it exists
        os.makedirs(output_dir)

    # Load the input DOCX file
    doc = Document(input_file)

    # Initialize variables to keep track of elements
    chunk_index = 0
    output_files = []
    current_tokens = 0

    # Create a new Document for each chunk
    new_doc = Document()

    for element in doc.element.body:
        # Estimate tokens for the current element
        if element.tag.endswith('p'):
            element_text = element.text_content() if hasattr(element, 'text_content') else element.text
            element_tokens = estimate_tokens(element_text)
        elif element.tag.endswith('tbl'):
            # Estimate tokens for a table (simple estimation by summing tokens of all cell contents)
            element_tokens = 0
            for row in element.iter('tr'):
                for cell in row.iter('tc'):
                    cell_text = cell.text_content() if hasattr(cell, 'text_content') else cell.text
                    element_tokens += estimate_tokens(cell_text)
        else:
            element_tokens = 0

        # If adding this element exceeds max_tokens, save the current document and start a new one
        if current_tokens + element_tokens > max_tokens and current_tokens > 0:
            output_file = os.path.join(output_dir, f"chunk_{chunk_index}.docx")
            try:
                new_doc.save(output_file)
                output_files.append(output_file)
                print(f"Saved chunk {chunk_index} successfully.")
            except Exception as e:
                print(f"Error saving chunk {chunk_index}: {e}")
            chunk_index += 1
            new_doc = Document()
            current_tokens = 0

        # Append the current element to the new document
        append_element(new_doc, element)
        current_tokens += element_tokens

    # Save the last document if it contains content
    if len(new_doc.element.body):
        output_file = os.path.join(output_dir, f"chunk_{chunk_index}.docx")
        try:
            new_doc.save(output_file)
            output_files.append(output_file)
            print(f"Saved final chunk {chunk_index} successfully.")
        except Exception as e:
            print(f"Error saving final chunk {chunk_index}: {e}")

    return output_files

def combine_docx_files(file_list, output_file):
    # Create a new empty Document
    master_doc = Document()

    # Iterate through the list of files and append each one to the master document
    file_index = 0
    for file in file_list:
        temp_doc = Document(file)
        element_index = 0
        for element in temp_doc.element.body:
            append_element(master_doc, element)
            element_index += 1
        file_index += 1

    # Save the combined document
    try:
        master_doc.save(output_file)
        print(f"Combined document saved as {output_file}")
    except Exception as e:
        print(f"Error saving combined document: {e}")

def main():
    input_file = 'large_document.docx'
    output_dir = 'original_chunks'
    combined_output_file = 'combined.docx'

    # Step 1: Chunk the document by elements while respecting the 2500 token limit
    chunked_files = chunk_docx_by_tokens(input_file, output_dir, max_tokens=1500)

    # Step 2: Combine the chunked files into one document (if needed)
    combine_docx_files(chunked_files, combined_output_file)

if __name__ == "__main__":
    main()
