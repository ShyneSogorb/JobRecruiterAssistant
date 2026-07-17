JSON_RULES_COMMON = """
Return ONLY valid JSON.

For technical profiles, extract each technology as an individual skill 
(e.g. "C++", "Unreal Engine", "Git"). Do not group multiple technologies
into a single string.

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
"Calm and Patient" -> "Calm", "Patient"

Do not include spoken languages in required_skills or skills. Put them only 
in the languages field.

Do not use markdown.

Do not explain anything.

Follow exactly the JSON schema below.
"""

JOB_OFFER_JSON_RULES = JSON_RULES_COMMON + """
The description field must contain the original job description, not a summary.

If work_mode or employment_type cannot be determined from the text, use the 
value that represents "not specified" rather than guessing based on job type.

If there is no explicit job title in the text, use the clearest short phrase 
from the post that identifies what the position/training/offer is about.

Only include a language in "languages" if it is explicitly stated or clearly 
implied as a requirement (e.g. the offer is written in a specific language 
for a local, in-person role). Do not infer language requirements you are not 
reasonably confident about.

If a field has no information available in the text, leave it as null or an 
empty array/string as appropriate to the schema - never fabricate a plausible-
sounding value.

If there is no information about work mode (remote, hybrid, onsite) set the 
value to unknown
If there is no information about the employement type (full_time, part_time, 
contract, temporary ) set the value to unknown
If there is no information about experience level (junior, mid, senior, lead, 
intern, unknown") Only infer experience level when the wording clearly 
supports it. Otherwise return unknown.
"""