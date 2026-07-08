JSON_RULES = """
Return ONLY valid JSON.

Extract technologies as individual skills.

Do not group multiple technologies into a single string.

Good:
["C++", "Python", "Linux"]

Bad:
["Extensive experience in C++ and Python"]

Keep skill names concise.

Use canonical names whenever possible.

Examples:
"C++17/C++20" -> "C++"
"Python 3" -> "Python"
"Git workflows" -> "Git"

The description field must contain the original job description, not a summary.

Do not include spoken languages in required_skills. Put them only in the languages field.

Do not use markdown.

Do not explain anything.

Follow exactly the JSON schema below.
"""
