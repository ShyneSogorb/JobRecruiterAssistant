

from modules.models.job_models import TargetLanguage
from modules.models.simple_models import StringModel, TargetLanguageModel
from src.utils.logger import Logger
from src.ai.client import AIClient


class Translator():
    def __init__(self, ai: AIClient, logger: Logger) -> None:
        self.ai = ai
        self.logger = logger

    GET_LANGUAGE_PROMPT="""
Eres un clasificador de idioma. Se te dará el texto de una oferta de trabajo (descripción del puesto).
Tu única tarea es determinar el idioma principal en el que está escrita la oferta.
Responde SOLO con un JSON que tenga la clave "language" con el valor "en" o "es".
No expliques tu razonamiento. No agregues texto fuera del JSON.
"""

    TRANSLATION_PROMPT="""
You are a professional translator. You will be given a raw HTML document written in English.

Your task is to translate ONLY the human-readable text content into {target_language}, while:
- Preserving the exact HTML structure, tags, and attributes unchanged.
- NOT translating: tag names, attribute names/values (href, src, class, id, style, etc.), inline CSS, JavaScript code, or content inside <script> or <style> tags.
- NOT translating text inside code blocks (<code>, <pre>) unless it's clearly natural-language content meant for the reader.
- Keeping placeholders, variables, or template syntax (e.g. {{variable}}, {%...%}, %s) untouched.
- Preserving whitespace/formatting so the HTML remains valid.
- If an attribute is meant for the reader (e.g. alt text, title, placeholder, meta description content), DO translate that value.

Return ONLY the translated HTML. Do not add explanations, comments, or markdown code fences. Do not wrap the output in ```html.
"""

    def deduce_language(self, text: str) -> TargetLanguage:
        self.logger.log(f"Deducing language for text {text[:30]}...")
        res = self.ai.ask(
            prompt=self.GET_LANGUAGE_PROMPT, 
            think=False,
            format=TargetLanguageModel.model_json_schema()
        )
        lang = TargetLanguageModel.model_validate_json(res.message.content)
        self.logger.log(f"{lang} is the deduced language for text {text[:30]}")
        return TargetLanguage(lang.language)
        

    def translate_html(self, html: str, language: TargetLanguage) -> str:
        target_language = language.name
        self.logger.log(f"Translating {html[:30]}... to {target_language}")
        res = self.ai.ask(
            prompt=f"""
You are a professional translator. You will be given a raw HTML document written in English.

Your task is to translate ONLY the human-readable text content into {target_language}, while following these rules strictly:

STRUCTURE:
- Preserve the exact HTML structure, tags, and attributes unchanged.
- Do NOT translate: tag names, attribute names/values (href, src, class, id, style, etc.), inline CSS, JavaScript code, or content inside <script> or <style> tags.
- Do NOT translate text inside code blocks (<code>, <pre>) unless it's clearly natural-language content meant for the reader.
- Keep placeholders, variables, or template syntax (e.g. {{variable}}, {{%...%}}, %s) untouched.
- Preserve whitespace/formatting so the HTML remains valid.
- If an attribute is meant for the reader (e.g. alt text, title, placeholder, meta description content), DO translate that value.

CONTENT - DO NOT TRANSLATE:
- Proper nouns (people's names, company names, brand names, product names).
- Technology names, programming languages, frameworks, libraries, tools (e.g. "Python", "React", "Kubernetes", "AWS").
- Job titles that function as industry-standard terms if there is no natural equivalent (e.g. "Product Manager" can stay as-is if untranslated is standard in the target language/industry; use judgment based on what a native professional would actually say).
- Acronyms and standard technical terms widely used in their English form within the target language's industry.

STYLE:
- The translation must sound formal, natural, and idiomatic to a native speaker of {target_language} - never literal or mechanical.
- Use the register and phrasing a professional in that language would naturally use in this context (e.g. job postings, business communication), not a word-for-word translation.
- Adapt sentence structure, idioms, and phrasing as needed to sound native, as long as the original meaning is fully preserved.

OUTPUT:
Return ONLY the translated HTML. Do not add explanations, comments, or markdown code fences.

html:
{html}
""", 
            think=True,
            format=StringModel.model_json_schema()
        )
        new_html = StringModel.model_validate_json(res.message.content).string
        self.logger.log(f"HTML successfully translated {new_html[:30]}")
        return new_html
        

    def translate_text(self, text: str, language: TargetLanguage) -> str:
        target_language = language.name
        self.logger.log(f"Translating {text[:30]}... to {target_language}")
        res = self.ai.ask(
            prompt=f"""
You are a professional translator.

You will be given a text written in English.

Your task is to translate it into {target_language} while following these rules:

CONTENT:
- Preserve the original meaning exactly.
- Do NOT add, remove, or rewrite information.
- Do NOT summarize or expand the text.
- Do NOT invent details.
- Preserve the original paragraph structure.
- Preserve bullet lists if present.
- Preserve punctuation and formatting whenever possible.

DO NOT TRANSLATE:
- Proper nouns (people's names, company names, brand names, product names).
- Technology names, programming languages, frameworks, libraries, tools (e.g. Python, Unreal Engine, Kubernetes, AWS).
- Acronyms and widely used technical terms unless a native professional would naturally translate them.

STYLE:
- Produce a fluent, natural, professional translation.
- Translate the meaning, not the individual words.
- Use terminology that a native professional would naturally use.
- Maintain the same level of formality as the original.
- Do not make the text more or less formal than it already is.

OUTPUT:
Return ONLY the translated text.
Do not add explanations, comments, markdown, or quotation marks.

Text:
{text}
""", 
            think=True,
            format=StringModel.model_json_schema()
        )
        new_text = StringModel.model_validate_json(res.message.content).string
        self.logger.log(f"Text successfully translated {text[:30]}")
        return text
        
    