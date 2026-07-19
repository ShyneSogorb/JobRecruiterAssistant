from modules.models.simple_models import FloatModel, StringModel
from src.ai.client import AIClient
from modules.models.candidate_models import CandidateProfile
from modules.models.job_models import EJobState, JobApplication, JobOffer, Salary, TargetLanguage

from src.utils.logger import Logger


class IntoductionMaker:
    def __init__(self, ai: AIClient, logger: Logger) -> None:
        self.ai = ai
        self.logger = logger

    def build_hiring_manager_text(self, job: JobOffer, candidate: CandidateProfile) -> str:
        self.logger.log(f"Making hiring manager text for {job.company}")
        res = self.ai.ask(prompt=f"""
You are an assistant that writes concise messages to hiring managers on behalf of a job candidate.

You will be given two JSON objects:
1. "job": structured data about the job posting (JobOffer schema).
2. "candidate": structured data about the applicant (CandidateProfile schema).

Your task is to write a short, professional message that accompanies the candidate's application in the "Message to the Hiring Manager" field.

The hiring manager receives a high volume of applications. Your goal is to explain, in a few sentences, why this candidate is particularly relevant for this specific role.

Field usage guidance:
- Base every statement only on information explicitly present in the provided JSON.
- Use "job.role" and "job.company" naturally if relevant.
- Match the candidate's experience, projects, achievements, and skills against:
  - job.required_skills
  - job.preferred_skills
  - job.ats_keywords
- Mention only the 2–4 strongest and most relevant overlaps.
- If available, include one concrete achievement with measurable impact.
- Do not summarize the entire resume.
- Ignore any field that is empty, null, or "unknown".
- Never invent, infer, exaggerate, or speculate about qualifications.

Style requirements:
- Write in English.
- Professional, confident, and concise.
- Sound like it was written by the candidate, not by a recruiter.
- Write in first person ("I", "my"), as if the candidate wrote the message personally.
- Avoid clichés such as "I am passionate", "hard-working", "fast learner", or "I believe I would be a great fit" unless supported by evidence.
- Focus on concrete relevance to this specific position.
- Keep it between 70 and 140 words.
- Do not mention that the candidate is applying through this platform.
- Do not ask for an interview explicitly.
- Do not include greetings, subject lines, signatures, contact information, or closing phrases such as "Best regards".
- Return only the message text, with no markdown or explanations.)
* If the hiring manager's name is unavailable, begin with "Dear Hiring Team,".
                          
You will receive the following JSON objects.

Job:
{job.model_dump_json()}

Candidate:
{candidate.model_dump_json()}

""",
think=True,
format=StringModel.model_json_schema()

        )
        message = StringModel.model_validate_json(res.message.content)
        self.logger.log(f"Manager text for {job.company} was successfully made")
        return message.string

##################################################################################################

    def build_cover_letter_text(self, job: JobOffer, candidate: CandidateProfile) -> str:
        self.logger.log(f"Making cover letter text for {job.company}")
        res = self.ai.ask(prompt=f"""
You are an assistant that writes tailored cover letters on behalf of job candidates.

You will be given two JSON objects:

1. "job": structured data about the job posting (JobOffer schema).
2. "candidate": structured data about the applicant (CandidateProfile schema).

Your task is to write a professional cover letter specifically tailored to this position.

The cover letter should demonstrate why the candidate is a strong match by referencing only information explicitly present in the provided JSON.

Field usage guidance:

* Base every statement only on information explicitly present in the provided JSON.
* Use "job.role" and "job.company" naturally throughout the letter.
* Match the candidate's experience, projects, achievements, and skills against:

  * job.required_skills
  * job.preferred_skills
  * job.ats_keywords
* Highlight the 3–5 strongest and most relevant qualifications.
* Whenever possible, include concrete achievements, especially those with measurable impact.
* Explain how the candidate's background aligns with the responsibilities or requirements of the role.
* Do not summarize the entire resume.
* Ignore any field that is empty, null, or "unknown".
* Never invent, infer, exaggerate, or speculate about qualifications.

Style requirements:

* Write in English.
* Write in first person ("I", "my").
* Professional, confident, and natural.
* Keep the tone formal but not overly generic.
* Avoid clichés such as "I am passionate", "hard-working", "fast learner", "team player", or "I believe I would be a great fit" unless directly supported by evidence.
* Focus on concrete evidence rather than generic claims.
* Keep the letter between 250 and 450 words.
* Use short, readable paragraphs.
* Do not mention salary expectations unless explicitly relevant in the provided data.
* Do not mention relocation, remote work, or availability unless explicitly present in the candidate or job data.
* Do not invent motivations or personal stories.
* End with a brief, professional closing expressing interest in discussing the opportunity further.

Format requirements:

* Return only the cover letter as plain text.
* Do not use markdown.
* Do not include explanations or comments.
* Do not include placeholder text.
* Sign the letter using candidate.personal.name.

The input will be provided as follows:

<JobOffer>
{job.model_dump_json()}
</JobOffer>

<CandidateProfile>
{candidate.model_dump_json()}
</CandidateProfile>

""",
think=True,
format=StringModel.model_json_schema()

        )
        message = StringModel.model_validate_json(res.message.content)
        self.logger.log(f"Cover letter text for {job.company} was successfully made")
        return message.string

##################################################################################################

    def calculate_salary(self, job: JobOffer, cv: str) -> Salary:
      self.logger.log(f"Calculating salary for company {job.company}")
      res = self.ai.ask(prompt=f"""
You are estimating an annual gross salary range for a candidate applying to a specific job.

Rules:
1. If the job posting itself specifies a salary range, use that range as your 
   primary answer and set "source" to "job_posting".
2. If no salary is specified in the job posting, estimate a plausible range based 
   on: the role title, seniority level, required skills, company, and location 
   mentioned in the job information. Set "source" to "estimated".
3. Do not fabricate false certainty — if you estimate, the range should reflect 
   realistic market uncertainty (i.e., don't give an artificially narrow range).
4. Adjust the estimate based on how well the candidate's CV matches the required 
   experience level (e.g., underqualified candidates may realistically be 
   offered toward the lower end).
5. All values must be in annual gross terms, in the currency stated in the job 
   information (or your best-inferred currency if not stated — state this 
   assumption in "notes").

Job information:
{job.model_dump_json()}

Candidate CV:
{cv}
""",
think=True,
format=Salary.model_json_schema()

      )
      salary = Salary.model_validate_json(res.message.content)
      self.logger.log(f"Salary for {job.company} was successfully made")
      return salary

##################################################################################################

    def calculate_match(self, job: JobOffer, cv: str) -> float:
      self.logger.log(f"Calculating score for application at {job.company}")
      res = self.ai.ask(prompt=f"""
You are scoring how well a candidate's CV matches a specific job posting.

Score range: 0-100
- 0 = no meaningful overlap between CV and job requirements
- 100 = CV fully covers all required skills, experience level, and qualifications

STEP 1 - Understand what the role actually requires:
Read the full job description, not just the required_skills list. Some 
postings name a specific tool/engine/technology mainly as example context 
within a broader, more generic task (e.g., "provide feedback on Panda3D 
code" where the real skill being evaluated is general proficiency in 
Python/C++ game development, not mastery of that one specific engine). 
Others require the specific tool as the actual, non-negotiable deliverable 
(e.g., "build and ship our product using Panda3D"). Determine which case 
this is before scoring.

STEP 2 - Score based on:
- Overlap with required_skills and preferred_skills
- Match with the stated experience_level
- Relevant work experience described in the CV
- If a required tool/technology is missing from the CV, weigh the gap 
  according to what you found in Step 1: heavier penalty if the posting 
  needs specific product delivery in that exact tool, lighter penalty if 
  the tool is example context for a more general, transferable skill set 
  the candidate does otherwise demonstrate strongly.

Do not guess at soft skills, personality fit, or cultural fit — you only 
have the CV text and job posting, so base the score strictly on documented 
overlap.

Job information:
{job.model_dump_json()}

Candidate CV:
{cv}
""",
think=True,
format=FloatModel.model_json_schema()

      )
      value = FloatModel.model_validate_json(res.message.content)
      self.logger.log(f"Score for job at {job.company} was successfully calculated")
      return value.value