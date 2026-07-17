CV_TRANSLATOR_RULES = """
Translate every user-visible string in the provided JSON into the
target language specified below, while leaving the JSON structure,
keys, and non-translatable values untouched.

────────────────────────────────────────
CORE PRINCIPLE
────────────────────────────────────────

Translate, never adapt.

The meaning, facts, and structure of the JSON must remain exactly the
same. Only the language of user-visible text changes.

Do not shorten, expand, rewrite, or "improve" any field while
translating. A translation must be a faithful equivalent of the
original text, not a new version of it.

────────────────────────────────────────
TARGET LANGUAGE
────────────────────────────────────────

Translate all applicable content into: {target_language}

Set the JSON "target_language" field to the ISO 639-1 two-letter code 
of the target language, in lowercase.

Examples:
Spanish -> "es"
English -> "en"
French -> "fr"
Catalan/Valencian -> "ca"
German -> "de"
Italian -> "it"
Portuguese -> "pt"

Do not use region-specific variants (e.g. not "es-ES", not "en-US").
Use only the plain two-letter code.

[... resto del prompt igual ...]
"""