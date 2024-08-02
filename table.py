from docx import Document

# Load the original document
doc = Document('your_input_file.docx')

# Initialize a counter for the sequential numbers
counter = 1

# Iterate through all tables in the document
for table in doc.tables:
    # Iterate through each row in the table
    for row in table.rows:
        # Iterate through each cell in the row
        for cell in row.cells:
            # Check if the cell contains any paragraphs
            if cell.paragraphs:
                for paragraph in cell.paragraphs:
                    # If the paragraph has runs, process each run
                    if paragraph.runs:
                        for run in paragraph.runs:
                            # Append the sequential number to the text in each run
                            run.text += f" {counter}"
                            counter += 1
                    else:
                        # If the paragraph has no runs, add a new run with the sequential number
                        paragraph.add_run(f" {counter}")
                        counter += 1
            else:
                # If the cell is completely empty, add a paragraph and run with the sequential number
                new_paragraph = cell.add_paragraph()
                new_paragraph.add_run(f" {counter}")
                counter += 1

# Save the modified document
doc.save('output_with_sequential_numbers.docx')

print("Added sequential numbers to each cell in the document.")
