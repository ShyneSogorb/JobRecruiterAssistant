from pydantic import BaseModel

from src.ai.prompt_constants.html_rules import HTML_RULES
from src.ai.prompts_rules.json_clarifier import CV_CLARIFIER_RULES
from src.ai.prompts_rules.candidate_parse import CV_EXTRACTOR_RULES
from src.ai.prompts_rules.job_parse import JOB_EXTRACTOR_RULES
from src.ai.prompts_rules.translation_rules import CV_TRANSLATOR_RULES
from src.ai.prompts_rules.adapter_rules import CV_ADAPTER_RULES
from src.ai.prompts_rules.role_rules import CV_HTML_SYSTEM_PROMPT, CV_PARSER_SYSTEM_PROMPT, JOB_PARSER_SYSTEM_PROMPT, CV_TRANSLATOR_SYSTEM_PROMPT, CV_ADAPTER_SYSTEM_PROMPT, CV_CLARIFIER_SYSTEM_PROMPT

LANGUAGE_NAMES = {
    "es": "Spanish",
    "en": "English",
    "fr": "French",
    "ca": "Catalan/Valencian",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
}


def BuildCandidateTextToJson(text: str) -> str:
    return f"""

    {CV_PARSER_SYSTEM_PROMPT}
    
    {CV_EXTRACTOR_RULES}

    EXTRACTION TEXT:\n\n

    {text}

"""


def BuildCandidateJsonToLang(original: str, target_lang_code: str) -> str:
    target_lang_name = LANGUAGE_NAMES.get(target_lang_code, target_lang_code)

    rules = CV_TRANSLATOR_RULES.replace("{target_language}", target_lang_name)

    return f"""

    {CV_TRANSLATOR_SYSTEM_PROMPT}

    {rules}

    ORIGINAL JSON:

    {original}

    ────────────────────────────────────────
    FINAL INSTRUCTION - READ CAREFULLY
    ────────────────────────────────────────

    Target language: {target_lang_name} (ISO 639-1 code: "{target_lang_code}")

    Translate every translatable string in the JSON above into
    {target_lang_name}. Set the "language" field to "{target_lang_code}".

    If any translatable field is still in its original language in your
    output, the task has failed.

"""

def BuildJobDescriptionToJson(text: str) -> str:
    return f"""

    {JOB_PARSER_SYSTEM_PROMPT}
    
    {JOB_EXTRACTOR_RULES}

    EXTRACTION TEXT:\n\n

    {text}

"""


def BuildCandidateJsonClarifier(original: str) -> str:
    return f"""

    {CV_CLARIFIER_SYSTEM_PROMPT}

    {CV_CLARIFIER_RULES}

    ORIGINAL JSON:

    {original}

    ────────────────────────────────────────
    FINAL INSTRUCTION - READ CAREFULLY
    ────────────────────────────────────────

    Clarify and polish every translatable string in the JSON above.
    Keep the original language. Do not translate.

    CRITICAL: All achievements and project descriptions MUST use impersonal 
    forms (past participles, infinitives, or noun phrases), NOT first person.

    Examples (Spanish):
    - "Construí un motor" -> "Desarrollo de motor" or "Desarrollado como motor"
    - "Usé Vulkan" -> "Implementación con Vulkan" or "Desarrollado con Vulkan"
    - "Descargué videos" -> "Descarga de videos" or "Permite descargar videos"

    Examples (English):
    - "I built a motor" -> "Built a motor" or "Development of motor"
    - "I used Vulkan" -> "Used Vulkan" or "Implementation with Vulkan"

    If any achievement uses first person, the task has failed.

"""


def BuildCandidateJobAdapter(offer: str, candidate: str) -> str:
    return f"""

{CV_ADAPTER_SYSTEM_PROMPT}

{CV_ADAPTER_RULES}

────────────────────────────────────────
INPUT DATA
────────────────────────────────────────

OFFER JSON:
{offer}

CANDIDATE JSON:
{candidate}

────────────────────────────────────────
OUTPUT REQUIREMENT
────────────────────────────────────────

Return ONLY the adapted CandidateProfile JSON.
No explanations. No markdown. No additional text.

"""


 
def BuildCandidateJsonToHtml(candidate_json: str) -> str:
    # NOTE: plain f-string on purpose. HTML_RULES contains literal CSS braces
    # (e.g. "@page { ... }") that would break str.format(); an f-string only
    # evaluates the {candidate_json} / {CV_HTML_SYSTEM_PROMPT} / {HTML_RULES}
    # expressions explicitly written here, so the CSS braces pass through
    # untouched.
    return f"""
 
    {CV_HTML_SYSTEM_PROMPT}
 
    {HTML_RULES}
 
    CANDIDATE PROFILE JSON:
 
    {candidate_json}
 
    ────────────────────────────────────────
    FINAL INSTRUCTION
    ────────────────────────────────────────
 
    Generate ONLY the HTML document.
    No explanations. No markdown. No code fences.
    Start directly with <!DOCTYPE html> and end with </html>.
 
"""
 