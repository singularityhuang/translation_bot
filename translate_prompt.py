import docx

def extract_text_with_structure(docx_file):
    doc = docx.Document(docx_file)
    elements = []

    for block in iter_block_items(doc):
        if isinstance(block, docx.text.paragraph.Paragraph):
            elements.append(('paragraph', block.text, block.style, block.runs))
        elif isinstance(block, docx.table._Cell):
            for paragraph in block.paragraphs:
                elements.append(('cell', paragraph.text, paragraph.style, paragraph.runs))

    return elements

def iter_block_items(parent):
    if isinstance(parent, docx.document.Document):
        parent_elm = parent.element.body
    elif isinstance(parent, docx.table._Cell):
        parent_elm = parent._element
    else:
        raise ValueError("Unknown parent type")

    for child in parent_elm.iterchildren():
        if isinstance(child, docx.oxml.CT_P):
            yield docx.text.paragraph.Paragraph(child, parent)
        elif isinstance(child, docx.oxml.CT_Tc):
            yield docx.table._Cell(child, parent)

def create_translation_prompt(source_lang, target_lang, country, elements):
    translation_prompt = f"""
    Please translate the source text below within <SOURCE_TEXT></SOURCE_TEXT> from {source_lang} to {target_lang}.

    Please translate in the manner below:

    1. Avoid any mismatch in the style: Identify the style of text (e.g., news article, court case, literature, casual conversation, financial report, technology essay, etc.) and consider the cultural and stylistic nuances of {target_lang} as spoken in {country}. For example, if source text is a news article, the translation should read like a news article in {target_lang} too.
    2. Avoid any mistranslation, omission, or untranslated text errors.
    3. Accuracy is very important. So your translation must convey the correct meaning. This trumps everything else.

    Output ONLY the translation. Do not provide any explanations or text apart from the translation.

    <SOURCE_TEXT>
    """
    for element in elements:
        translation_prompt += f"{element[1]}\n"
    
    translation_prompt += "</SOURCE_TEXT>"
    print(translation_prompt)
    return translation_prompt
