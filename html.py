import pypandoc
import os

def convert_docx_to_html(docx_file, output_html_file):
    """
    Convert a DOCX file to HTML with CSS styles preserved.
    """
    # Check if the input file exists
    if not os.path.exists(docx_file):
        raise FileNotFoundError(f"File not found: {docx_file}")

    # Pandoc arguments to enhance CSS and style preservation
    extra_args = [
        '--standalone',  # Produce a standalone HTML file
        '--extract-media=.',  # Extract media files to the current directory
    ]
    
    # Convert DOCX to HTML
    output = pypandoc.convert_file(docx_file, 'html', extra_args=extra_args)

    # Write the HTML output to a file
    with open(output_html_file, 'w', encoding='utf-8') as file:
        file.write(output)

def convert_html_to_docx(html_content, output_file):
    """
    Convert HTML content back to a DOCX file.
    """
    # Convert the HTML back to DOCX using pypandoc
    pypandoc.convert_text(html_content, 'docx', format='html', outputfile=output_file)

def main():
    docx_file = 'input.docx'  # Replace with your input DOCX file
    output_html_file = 'output.html'
    output_docx_file = 'output.docx'

    # Convert DOCX to HTML with CSS
    convert_docx_to_html(docx_file, output_html_file)
    
    # Optionally, read back the HTML content for further processing
    with open(output_html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Convert the HTML content back to DOCX
    convert_html_to_docx(html_content, output_docx_file)
    
    print(f"Converted {docx_file} to HTML and back to {output_docx_file} with CSS preserved")

if __name__ == "__main__":
    main()
