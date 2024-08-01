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

# Function to return translation guidelines
def get_translation_guidelines(target_lang, country):
    return f"""
1. **Accuracy**: Accuracy is paramount. Your translation MUST convey the correct meaning of the source text. This is the most critical aspect and takes precedence over all other considerations, including style, tone, and format. Avoid any errors such as duplications, mistranslations, omissions, or untranslated text.
2. **Linguistically Correct**:
   - **Grammar**: Follow proper sentence structure, verb tense, and overall grammatical correctness according to {target_lang} conventions.
   - **Spelling**: Adhere to the correct spelling as per {target_lang} standards.
   - **Punctuation**: Use punctuation correctly in accordance with {target_lang} norms, recognizing that different languages may have unique punctuation rules.
3. **Stylistically Consistent**:
   - **Tone and Formality**: Match the tone, formality, and style of the source text.
   - **Genre Appropriateness**: Adjust the translation style according to the genre, whether it's factual, descriptive, or technical.
4. **Culturally and Regionally Appropriate**: Align the translation with the cultural and regional norms specific to {country}. For example, in Traditional Chinese with zh-TW locale, "disabled" should be translated as "殘障人士" instead of "殘疾人".
"""


def create_translation_prompt(source_lang, target_lang, country, elements):
    translation_prompt = f"""
    Please translate the following source text from {source_lang} to {target_lang}.

    ### Translation Guidelines:
    {get_translation_guidelines(target_lang, country)}

    Please ensure that your translation adheres to the guidelines provided.

    Output ONLY the translation. Do not provide any explanations or text apart from the translation.

    <SOURCE_TEXT>
    """
    for element in elements:
        translation_prompt += f"{element[1]}\n"
    
    translation_prompt += "</SOURCE_TEXT>"
    return translation_prompt

# Function to define error categories for reviewing translations
def get_error_categories(target_lang, country):
    return f"""
### Error Categories:
1. **Accuracy Issues**: Look for any errors such as duplication, mistranslation, omission, or untranslated text that compromise the correctness of the translation.
2. **Language Quality and Punctuation**:
   - **Grammar**: Identify issues related to sentence structure, verb tense, and overall grammatical correctness.
   - **Spelling**: Ensure that all words are spelled correctly according to the conventions of {target_lang}.
   - **Punctuation**: Check that punctuation is used correctly and conforms to the conventions of {target_lang}. Different languages may have unique punctuation rules that should be followed.
3. **Style Consistency**:
   - **Definition**: "Style" refers to the overall tone, formality, and structure of the text. It includes the choice of words, sentence structure, and the way ideas are presented to suit a specific genre or context.
   - **Examples**: A *news article* might be direct and factual, *literature* might be more descriptive and nuanced, and a *technical document* should be precise and clear.
   - **Task**: Check for mismatches in style between the source and target texts. The translation should mirror the tone and style of the source text in {target_lang}.
4. **Cultural and Regional Appropriateness**: Ensure that the translation adheres to the writing or speaking conventions specific to {country}. For example, in 繁體中文, "disabled" should be translated as "殘障人士" instead of "殘疾人".
"""

# Function to define the error report format for reviewing translations
def get_error_report_format(source_lang, target_lang):
    return f"""
### Error Report Format:
[
  {{
    "original": "string",
    "translated": "string",
    "errors": "string"
  }},
  ...
]

### Attribute Explanations:

- **Original** (attribute):
   - **Definition**: The `original` attribute holds the exact sentence or phrase as it appears in the source text. This text is taken directly from the document or material written in the source language ({source_lang}).
   - **Purpose**: This attribute serves as a reference point for comparison with the translated text. It is used to identify and review the corresponding translation for accuracy and consistency.

- **Translated** (attribute):
   - **Definition**: The `translated` attribute contains the corresponding sentence or phrase from the translated text. This is the version that has been translated from the source language into the target language ({target_lang}).
   - **Purpose**: This attribute is the primary focus of the review process. It is compared against the `original` attribute to ensure that the translation accurately reflects the meaning, style, and nuances of the source text.

- **Errors** (attribute):
   - **Definition**: The `errors` attribute provides a description of specific issues or inaccuracies identified in the `translated` sentence. This may include problems such as mistranslations, omissions, grammatical mistakes, stylistic inconsistencies, or cultural inaccuracies.
   - **Purpose**: The purpose of this attribute is to document any deviations from the expected quality or accuracy in the translation. It helps reviewers pinpoint exactly what is wrong with the translation so that appropriate corrections can be made. The focus is strictly on identifying the errors without suggesting corrections, and each error description should be concise (up to 30 words).
"""

# Usage example in a larger prompt
def create_error_report_prompt(source_lang, target_lang, country, elements, translated_text):
    error_report_prompt = f"""
    Your task is to carefully read the following source text within <SOURCE_TEXT></SOURCE_TEXT> and its translation within <TRANSLATION></TRANSLATION> from {source_lang} to {target_lang}. Identify and point out errors in each problematic sentence in an error report.

    Use the following error categories to guide your review:

    ### Error Categories:
    {get_error_categories(target_lang, country)}

    After identifying the errors, document them in the format specified below:

    ### Error Report Format:
    {get_error_report_format(source_lang, target_lang)}

    Ensure that you identify at least one error. Output only the error report in the specified format and nothing else.

    <SOURCE_TEXT>
    """
    # Append the source text elements to the prompt
    for element in elements:
        error_report_prompt += f"{element[1]}\n"

    error_report_prompt += f"</SOURCE_TEXT>\n\n<TRANSLATION>\n{translated_text}\n</TRANSLATION>"

    return error_report_prompt

def create_improvement_prompt(source_lang, target_lang, country, translated_text, error_report):
    improvement_prompt = f"""
    A translation in {target_lang} is provided below within <TRANSLATION></TRANSLATION>. An error report on the translation is provided below within <ERRORS></ERRORS>. The error report follows this format:

    ### Error Report Format:
    {get_error_report_format(source_lang, target_lang)}

    Your task is to:

    1. Identify all the problematic sentences in the translation provided within <TRANSLATION></TRANSLATION>.
    2. Correct the identified errors according to the descriptions in the "errors" attribute of each object in the error report.
    3. Provide an improved translation that addresses and corrects all listed errors.
    4. Ensure the improved translation adheres to the following guidelines:

    ### Translation Guidelines:
    {get_translation_guidelines(target_lang, country)}

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
    You are a writer and editor at a translation agency fluent in {target_lang}. Your task is to:

    1. Carefully read the following translation text within <TRANSLATION></TRANSLATION>.
    2. Paraphrase any paragraph or section as needed so that the edited translation sounds natural and native in {target_lang}.
    3. Ensure that the edited translation maintains the same meaning as the original translation. Do not alter the intended meaning or introduce new information.
    4. Pay special attention to the natural grammatical structure in {target_lang}. For example, in Chinese, it's common to use shorter sentences with fewer subordinate clauses compared to English or other languages. Adjust sentence structure accordingly to reflect the natural flow of {target_lang}.

    Output only the edited translation and nothing else.

    <TRANSLATION>
    {improved_translation}
    </TRANSLATION>
    """
    return natural_translation_prompt

def create_error_free_translation_prompt(target_lang, country, natural_translation):
    error_free_translation_prompt = f"""
    You are a writer and editor at a translation agency fluent in {target_lang}. Your task is to review the following translation for any remaining errors and ensure it adheres to conventional wording in {country}. 

    Please follow these guidelines:

    1. Carefully read the translation text provided within <TRANSLATION></TRANSLATION>.
    2. Do not paraphrase or rephrase any sentences; focus solely on correcting errors.
    3. Correct any of the following errors:
       - Duplication or omission of content.
       - Grammar errors, including verb tense, sentence structure, and subject-verb agreement.
       - Spelling mistakes according to {target_lang} standards.
       - Punctuation errors, ensuring the correct use of punctuation marks as per {target_lang} conventions.
    4. Ensure the translation uses appropriate wording and conforms to the cultural and linguistic norms of {country}. For example, in 繁體中文, "disabled" should be translated as "殘障人士" instead of "殘疾人".

    Output only the edited, error-free translation and nothing else.

    <TRANSLATION>
    {natural_translation}
    </TRANSLATION>
    """
    return error_free_translation_prompt
