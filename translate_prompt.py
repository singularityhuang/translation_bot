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
    return translation_prompt

def create_error_report_prompt(source_lang, target_lang, country, elements, translated_text):
    error_report_prompt = f"""
    Your task is to carefully read the following source text within <SOURCE_TEXT></SOURCE_TEXT> and its translation within <TRANSLATION></TRANSLATION> from {source_lang} to {target_lang}, and then point out errors of each problematic sentence in an error report.

    When writing errors on the translation, point out:

    (i) Any duplication, mistranslation, omission, or untranslated text errors that make the translation wrong.
    (ii) Any grammar, spelling, or punctuation errors that make the translation hard to read.
    (iii) Any mismatch in the style (e.g., news article, court case, literature, casual conversation, financial report, technology essay, etc.) that make the translation inappropriate. For example, if source text is a news article, the translation should read like a news article in {target_lang}.
    (iv) Any mismatch in writing or speaking wording conventions in {country} or predicted target country. For example, in 繁體中文, "disabled" is "殘障人士" instead of "殘疾人".

    The error report should be in array of objects format:
    [
     {{
       "problemmatic_translated_sentence": "string",
       "respective_source_sentence": "string",
       "errors": "string"
     }},
    ...
    ]

    respective_source_sentence: The sentence in {source_lang}
    problematic_translated_sentence: The translation in {target_lang}
    errors: The errors pointed out by experts regarding problematic_translated_sentence. Point out the errors only. Don't provide corrected sentence. Each one should be less than 30 words

    You must write at least one thing. Output only the error report and nothing else.

    <SOURCE_TEXT>
    """
    for element in elements:
        error_report_prompt += f"{element[1]}\n"

    error_report_prompt += f"</SOURCE_TEXT>\n\n<TRANSLATION>\n{translated_text}\n</TRANSLATION>"

    return error_report_prompt

def create_improvement_prompt(target_lang, country, translated_text, error_report):
    improvement_prompt = f"""
    A translation in {target_lang} is provided below within <TRANSLATION></TRANSLATION>. An error report on the translation is provided below within <ERRORS></ERRORS>. The error report is in array of objects format:

    [
     {{
       "problematic_translated_sentence": "string",
       "respective_source_sentence": "string",
       "errors": "string"
     }},
    ...
    ]

    respective_source_sentence: The sentence in the source language
    problematic_translated_sentence: The translation in {target_lang}
    errors: The errors pointed out by experts regarding problematic_translated_sentence

    Your task is to:

    1. Identify all the problematic_translated_sentence in the translation below within <TRANSLATION></TRANSLATION>
    2. Correct their "errors" respectively
    3. Provide an improved translation that ensures the translation is free from these errors
    4. Make sure you maintain the same style: For example, if the source text is a news article, the translation should read like a news article in {target_lang}. 
    5. Make sure you use the same writing or speaking wording conventions in {country}: For example, in 繁體中文, "disabled" should be "殘障人士" instead of "殘疾人".

    Output only the improved translation and nothing else.

    <TRANSLATION>
    {translated_text}
    </TRANSLATION>

    <ERRORS>
    {error_report}
    </ERRORS>
    """

    return improvement_prompt

def create_natural_translation_prompt(target_lang, country, improved_translation):
    natural_translation_prompt = f"""
    You are a writer and an editor in a translation agency fluent in {target_lang}. Your task is to:

    1. Carefully read the following translation text within <TRANSLATION></TRANSLATION>. 
    2. Paraphrase any paragraph or section if needed so that the edited translation sounds natural and native.
    3. Make sure you maintain the same style: For example, if the source text is a news article, the translation should read like a news article in {target_lang}. 
    4. Make sure you use the same writing or speaking wording conventions in {country}: For example, in 繁體中文, "disabled" should be "殘障人士" instead of "殘疾人".

    Output only the edited translation and nothing else.

    <TRANSLATION>
    {improved_translation}
    </TRANSLATION>
    """
    return natural_translation_prompt

def create_error_free_translation_prompt(target_lang, country, natural_translation):
    error_free_translation_prompt = f"""
    You are a writer and an editor in a translation agency fluent in {target_lang}. You will use the conventional wording in {country}. Your task is to correct any mistakes and then provide the edited translation based on the following guidelines:

    1. Carefully read the following translation text within <TRANSLATION></TRANSLATION>. 
    2. Do not paraphrase any sentence!
    3. Avoid any of the following errors:
    (i) Any duplication or omission errors.
    (ii) Any grammar, spelling, punctuation, or punctuation mark errors.
    4. Make sure you use the same writing or speaking wording conventions in {country} or the predicted target country: For example, in 繁體中文, "disabled" should be "殘障人士" instead of "殘疾人".

    Output only the edited translation and nothing else.

    <TRANSLATION>
    {natural_translation}
    </TRANSLATION>
    """
    return error_free_translation_prompt
