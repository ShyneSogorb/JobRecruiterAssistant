import json
from typing import Any, Callable

from pydantic import BaseModel

from modules.candidate_maker.candidatemaker import CandidateMakerPipeline
from modules.candidate_optimizer.prompts import CandidateOptimizerPrompts
from src.ai.client import AIClient
from src.utils.cache import CacheManager
import src.utils.utils_library as Utils
from modules.models.candidate_models import *
from modules.models.job_models import JobOffer, TargetLanguage

import src.ai.static_prompts as StaticPrompts

from src.ai.prompts_rules.candidate_parse import CV_EXTRACTOR_RULES
from src.ai.prompts_rules.role_rules import CV_PARSER_SYSTEM_PROMPT
from src.utils.logger import Logger




class CandidateOptimizerPipeline:

    class CandidatePromptBuilder:
        def __init__(self, fn: Callable[[str, str], str], job: JobOffer, candidate: BaseModel) -> None:
            self.fn = fn
            self.job = job
            self.candidate_data = candidate

        def build(self) -> str:
            return self.fn(self.job.model_dump_json(), self.candidate_data.model_dump_json())
    
    def __init__(self, ai: AIClient, logger: Logger) -> None:
        self.ai: AIClient = ai
        self.logger: Logger = logger
        self.prompts = CandidateOptimizerPrompts()

    def _filter_skills_impl(self, prompt: CandidatePromptBuilder, model: type[BaseModel]) -> Any:       
        response = self.ai.ask(prompt.build(), format=model.model_json_schema())
        result = model.model_validate_json(response.message.content)
        return result # type: ignore
    

    @Utils.TimedFunction
    def _filter_skills(self, prompt: CandidatePromptBuilder, candidate: CandidateProfile) -> CandidateProfile:

        self.logger.log("Optimizing skills")
        origin = len(candidate.skills.skills)

        prompt.candidate_data = candidate.skills
        candidate.skills = self._filter_skills_impl(prompt, ListSkills)

        self.logger.log(f"Skills optimized, from {origin}, to {len(candidate.skills.skills)}")
        return candidate
    
    @Utils.TimedFunction
    def _filter_soft_skills(self, prompt: CandidatePromptBuilder, candidate: CandidateProfile) -> CandidateProfile:
        
        self.logger.log("Optimizing soft skills")
        origin = len(candidate.soft_skills.array)

        prompt.candidate_data = candidate.soft_skills
        candidate.soft_skills = self._filter_skills_impl(prompt, ListString)

        self.logger.log(f"Soft skills optimized, from {origin}, to {len(candidate.soft_skills.array)}")
        return candidate
    
    @Utils.TimedFunction
    def _filter_transferable_skills(self, prompt: CandidatePromptBuilder, candidate: CandidateProfile) -> CandidateProfile:
        
        self.logger.log("Optimizing transferable skills")
        origin = len(candidate.transferable_skills.array)

        prompt.candidate_data = candidate.transferable_skills
        candidate.transferable_skills = self._filter_skills_impl(prompt, ListString)

        self.logger.log(f"Transferable skills optimized, from {origin}, to {len(candidate.transferable_skills.array)}")
        return candidate

    @Utils.TimedFunction
    def _optimize_skills(self, job: JobOffer, candidate: CandidateProfile) -> CandidateProfile:

        prompt = self.CandidatePromptBuilder(self.prompts.build_skill_optimizer, job, candidate)

        candidate = self._filter_skills(prompt, candidate)

        prompt.fn = self.prompts.build_soft_skill_optimizer
        candidate = self._filter_soft_skills(prompt, candidate)

        prompt.fn = self.prompts.build_transferable_skill_optimizer
        candidate = self._filter_transferable_skills(prompt, candidate)

        return candidate

    @Utils.TimedFunction
    def _optimize_projects(self, prompt: CandidatePromptBuilder, candidate: CandidateProfile) -> CandidateProfile:
        self.logger.log("Optimizing projects")

        prompt.candidate_data = candidate.projects

        response = self.ai.ask(prompt.build(), format=ProjectList.model_json_schema())
        candidate.projects = ProjectList.model_validate_json(response.message.content)

        self.logger.log("Projects successfully optimized")
        return candidate

    @Utils.TimedFunction
    def _optimize_experience(self, prompt: CandidatePromptBuilder, candidate: CandidateProfile) -> CandidateProfile:
        self.logger.log("Optimizing experience")

        prompt.candidate_data = candidate.experience

        response = self.ai.ask(prompt.build(), format=ExperienceList.model_json_schema())
        candidate.experience = ExperienceList.model_validate_json(response.message.content)
        
        self.logger.log("Experience successfully optimized")
        return candidate

    @Utils.TimedFunction
    def _optimize_education(self, prompt: CandidatePromptBuilder, candidate: CandidateProfile) -> CandidateProfile:
        self.logger.log("Optimizing education")

        prompt.candidate_data = candidate.education

        response = self.ai.ask(prompt.build(), format=EducationList.model_json_schema())
        candidate.education = EducationList.model_validate_json(response.message.content)

        self.logger.log("Education successfully optimized")
        return candidate

    @Utils.TimedFunction
    def _optimize_background(self, job: JobOffer, candidate: CandidateProfile) -> CandidateProfile:

        prompt = self.CandidatePromptBuilder(self.prompts.build_project_optimizer, job, candidate)

        candidate = self._optimize_projects(prompt, candidate)

        prompt.fn = self.prompts.build_experience_optimizer
        candidate = self._optimize_experience(prompt, candidate)

        prompt.fn = self.prompts.build_education_optimizer
        candidate = self._optimize_education(prompt, candidate)

        return candidate

    @Utils.TimedFunction
    def _optimize_languages(self, prompt: CandidatePromptBuilder, candidate: CandidateProfile) -> CandidateProfile:
        self.logger.log("Optimizing languages")

        prompt.candidate_data = candidate.languages

        response = self.ai.ask(prompt.build(), format=LanguageList.model_json_schema())
        candidate.languages = LanguageList.model_validate_json(response.message.content)

        self.logger.log("Languages successfully optimized")
        return candidate
    
    @Utils.TimedFunction
    def _optimize_additional(self, prompt: CandidatePromptBuilder, candidate: CandidateProfile) -> CandidateProfile:
        self.logger.log("Optimizing aditional information")

        prompt.candidate_data = candidate.additional

        response = self.ai.ask(prompt.build(), format=ListString.model_json_schema())
        candidate.additional = ListString.model_validate_json(response.message.content)
        
        self.logger.log("Aditional information successfully optimized")
        return candidate

    @Utils.TimedFunction
    def _optimize_details(self, job: JobOffer, candidate: CandidateProfile) -> CandidateProfile:
        
        prompt = self.CandidatePromptBuilder(self.prompts.build_language_optimizer, job, candidate)

        candidate = self._optimize_languages(prompt, candidate)

        prompt.fn = self.prompts.build_aditional_optimizer
        candidate = self._optimize_additional(prompt, candidate)

        return candidate
    
    @Utils.TimedFunction
    def _optimize_summary(self, job: JobOffer, candidate: CandidateProfile) -> CandidateProfile:
        self.logger.log("Optimizing summary")

        class StrModel(BaseModel):
            string: str

        prompt = self.CandidatePromptBuilder(self.prompts.build_optimized_summary, job, candidate)
        
        response = self.ai.ask(prompt.build(), format=StrModel.model_json_schema())

        result = StrModel.model_validate_json(response.message.content)
        candidate.summary = result.string

        self.logger.log("Summary successfully optimized")
        return candidate
    
        
    @Utils.TimedFunction
    def optimize(self, job: JobOffer, candidate: CandidateProfile) -> CandidateProfile:



        candidate = self._optimize_skills(job, candidate)
        candidate = self._optimize_background(job, candidate)
        candidate = self._optimize_details(job, candidate)
        candidate = self._optimize_summary(job, candidate)
        
        return candidate
