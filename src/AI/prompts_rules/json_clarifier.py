CV_CLARIFIER_RULES = """
Improve the clarity, grammar, and professional tone of every user-visible 
string in the provided JSON, while preserving all factual content exactly.

────────────────────────────────────────
CORE PRINCIPLE
────────────────────────────────────────

Clarify and polish, never invent or remove.

The meaning, facts, and structure of the JSON must remain exactly the same.
Only improve grammar, clarity, and professional tone.

Do not add new information, achievements, or skills.
Do not remove information present in the original.
Fix grammatical errors and awkward phrasing.

────────────────────────────────────────
IMPERSONAL FORM CONVERSION (CRITICAL)
────────────────────────────────────────

ALL achievements, responsibilities, and project descriptions MUST be 
converted to TRUE IMPERSONAL FORM. This means NO first-person verbs, 
even implicit ones.

FORBIDDEN VERB FORMS (these imply "I did X"):
- "Built..." ❌ (implies "I built")
- "Used..." ❌ (implies "I used")
- "Designed..." ❌ (implies "I designed")
- "Implemented..." ❌ (implies "I implemented")
- "Created..." ❌ (implies "I created")
- "Developed..." ❌ (implies "I developed")
- "Worked..." ❌ (implies "I worked")
- "Collaborated..." ❌ (implies "I collaborated")

REQUIRED IMPERSONAL FORMS:

Option 1 - Noun phrases (MOST PREFERRED):
- "Development of custom C++ game engine using CMake"
- "Implementation of Vulkan rendering API"
- "Design of interface-based abstraction for independent module development"
- "Direct work with low-level C APIs"
- "Build system management using CMake"
- "Module connection using linker"
- "SDL2 implementation for window management"
- "HLSL as shader language"

Option 2 - Past participles as adjectives:
- "Custom C++ game engine developed from scratch using CMake"
- "Vulkan used as rendering API"
- "Interface-based abstraction designed for independent module development"
- "Low-level C APIs worked with directly"

Option 3 - Present tense for features/capabilities:
- "Downloads any public video via link"
- "Converts MP4 video into MP3 audio"
- "Processes single files or entire folders"
- "Uses multithreading for faster processing"

Spanish examples:
- "Construí un motor" → "Desarrollo de motor" or "Motor desarrollado"
- "Usé Vulkan" → "Implementación de Vulkan" or "Vulkan utilizado"
- "Diseñé sistemas" → "Diseño de sistemas" or "Sistemas diseñados"
- "Trabajé con APIs" → "Trabajo con APIs" or "APIs utilizadas"

English examples:
- "I built a motor" → "Development of motor" or "Motor developed"
- "I used Vulkan" → "Implementation of Vulkan" or "Vulkan used"
- "I designed systems" → "Design of systems" or "Systems designed"
- "I worked with APIs" → "Work with APIs" or "APIs worked with"

────────────────────────────────────────
CLARIFICATION RULES
────────────────────────────────────────

You may:
- Fix grammatical errors in the original text
- Improve awkward phrasing while preserving meaning
- Use more professional vocabulary
- Ensure consistent verb tense (past for completed work, present for features)
- Convert ALL first-person statements (explicit or implicit) to impersonal forms
- Shorten overly verbose descriptions while keeping all key information
- Remove filler words and redundant phrases

You must NOT:
- Add new facts, achievements, or skills
- Remove any information present in the original
- Change dates, names, companies, or technical terms
- Alter the JSON structure or keys
- Translate to another language (keep original language)
- Leave ANY verb in first-person form (even implicit)

────────────────────────────────────────
WHAT TO CLARIFY
────────────────────────────────────────

Improve all natural-language, user-facing text fields:

- role / job titles (as free text, not proper nouns)
- summary
- skills descriptions (not the technology names themselves)
- soft_skills
- transferable_skills
- achievements / responsibilities (CRITICAL: convert to impersonal)
- project descriptions and achievements (CRITICAL: convert to impersonal)
- education field names and descriptions
- additional/notes fields

────────────────────────────────────────
WHAT NEVER TO CHANGE
────────────────────────────────────────

Never modify:

- Proper nouns: person names, company names, institution names, product names.
- Technology names: programming languages, frameworks, libraries, engines, 
  tools, APIs, standards (e.g., "Python", "Unreal Engine", "Git", "C++").
- Certifications and standard acronyms (e.g., "PMP", "AWS", "ISO 9001").
- Email addresses, phone numbers, URLs, social media handles.
- Dates (structured date fields).
- Fixed enum values (e.g., "unknown", "remote", "full_time").
- JSON keys.
- target_language field.

────────────────────────────────────────
OUTPUT
────────────────────────────────────────

Return ONLY valid JSON conforming exactly to the same schema as the input.

Do not include explanations, comments, or Markdown formatting.
Do not wrap the JSON in code fences.

────────────────────────────────────────
FINAL REMINDER
────────────────────────────────────────

Keep the original language. Do not translate.

CRITICAL: ALL achievements and project descriptions MUST use TRUE IMPERSONAL 
forms. NO first-person verbs allowed, even implicit ones.

Examples of CORRECT transformations:
- "Built a custom engine" → "Development of custom engine" ✅
- "Used Vulkan for rendering" → "Implementation of Vulkan for rendering" ✅
- "Designed interface-based abstraction" → "Design of interface-based abstraction" ✅
- "Worked with low-level C APIs" → "Direct work with low-level C APIs" ✅
- "Implemented SDL2" → "SDL2 implementation" ✅

Examples of INCORRECT transformations (DO NOT DO THIS):
- "Built a custom engine" → "Built a custom engine" ❌ (still first person)
- "Used Vulkan" → "Used Vulkan" ❌ (still first person)
- "Designed systems" → "Designed systems" ❌ (still first person)
"""