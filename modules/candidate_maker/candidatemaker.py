from modules.models.candidate_models import *
from .prompts import CandidateDataExtractionPrompt
from src.ai.client import AIClient
from src.utils.logger import Logger
import os
import json
from src.utils import utils_library as Utils
from time import perf_counter
from ..utils.assetloader import load_module

class CandidateMakerPipeline:

    def _from_asset_path(self, sub:str) -> str:
        return "/".join([
            os.path.dirname(__file__),
            "assets",
            sub
        ])

    def __init__(self, ai: AIClient, logger: Logger) -> None:
        self.ai = ai
        self.logger = logger
        self.prompts = CandidateDataExtractionPrompt()

    @Utils.TimedFunction
    def _load_personal(self) -> Personal: 
        self.logger.log("Loading personal data")
        with open(self._from_asset_path("PersonalData.json"), "r", encoding="utf-8") as f:
            personal = Personal.model_validate_json(f.read())
            self.logger.log("Personal data successfully loaded")
            return personal
        raise Exception()

    @Utils.TimedFunction
    def _load_projects(self, details: DetailsExtraction) -> tuple[ProjectList, DetailsExtraction]:
        projects = ProjectList()

        root = self._from_asset_path("projects")
        dirs = list[str](filter(lambda i: os.path.isfile(os.path.join(root, i)), os.listdir(root)))
        counter = 0
        nfiles = len(dirs)
        self.logger.log(f"Loading {nfiles} projects")

        @Utils.TimedFunction
        def load_project(filename):
            self.logger.log(f"Loading project {filename}")
            #with open(os.path.join(root, filename), "r", encoding="utf-8") as f:
            try:
                data = load_module(os.path.join(root, filename))
                res: ProjectExtended
                try:
                    res = ProjectExtended.model_validate_json(data)
                except:
                    response = self.ai.ask(
                        prompt=self.prompts.build_project_detail_extractor(data),
                        format=ProjectExtended.model_json_schema()
                    )
                    res = ProjectExtended.model_validate_json(response.message.content)

                projects.projects.append(res.project)
                details.extend(res.details)
                nonlocal counter
                counter += 1
                self.logger.log(f"Project {filename} successfully loaded")
                self.logger.log(f"{counter}/{nfiles} projects loaded")
            except UnicodeDecodeError as e:
                self.logger.log(f"ERROR: Project {filename} could not be loaded {e.reason}" )

        for filename in dirs:
            load_project(filename)

        return projects, details

    @Utils.TimedFunction
    def _load_experiences(self, details: DetailsExtraction) -> tuple[ExperienceList, DetailsExtraction]:
        expreiences = ExperienceList()

        root = self._from_asset_path("experience")

        dirs = os.listdir(root)
        counter = 0
        nfiles = len(dirs)
        self.logger.log(f"Loading {nfiles} experiences")

        @Utils.TimedFunction
        def load_experience(filename):
            self.logger.log(f"Loading experience {filename}")
            with open(os.path.join(root, filename), "r", encoding="utf-8") as f:
                response = self.ai.ask(
                    prompt=self.prompts.build_experience_detail_extractor(f.read()),
                    format=ExperienceExtended.model_json_schema()
                )
                res = ExperienceExtended.model_validate_json(response.message.content)

                expreiences.experiences.append(res.experience)
                details.extend(res.details)
            nonlocal counter
            counter += 1
            self.logger.log(f"Experience {filename} successfully loaded")
            self.logger.log(f"{counter}/{nfiles} experiences loaded")

        for filename in dirs:
            load_experience(filename)

        return expreiences, details

    @Utils.TimedFunction
    def _load_educations(self) -> EducationList:
        educations = EducationList()

        root = self._from_asset_path("education")

        dirs = os.listdir(root)
        counter = 0
        nfiles = len(dirs)
        self.logger.log(f"Loading {nfiles} educations")

        def load_education(filename):
            self.logger.log(f"Loading education {filename}")
            with open(os.path.join(root, filename), "r", encoding="utf-8") as f:
                response = self.ai.ask(
                    prompt=self.prompts.build_education_extractor(f.read()),
                    format=Education.model_json_schema()
                )
                res = Education.model_validate_json(response.message.content)

                educations.educations.append(res)
            nonlocal counter
            counter += 1
            self.logger.log(f"Education {filename} successfully loaded")
            self.logger.log(f"{counter}/{nfiles} educations loaded")

        for filename in dirs:
            load_education(filename)


        return educations

    @Utils.TimedFunction
    def _load_languages(self) -> LanguageList:
        with open(self._from_asset_path("Languages.json"), "r", encoding="utf-8") as f:
            return LanguageList.model_validate_json(f.read())

    @Utils.TimedFunction
    def _load_additional(self) -> ListString:
        with open(self._from_asset_path("AditionalInfo.json"), "r", encoding="utf-8") as f:
            return ListString.model_validate_json(f.read())


    def build_candidate(self) -> CandidateProfile:

        details: DetailsExtraction = DetailsExtraction()

        projects, details = self._load_projects(details)
        
        experience, details = self._load_experiences(details)

        education = self._load_educations()

        personal = self._load_personal()
        languages = self._load_languages()
        aditional = self._load_additional()

        result = CandidateProfile(
            target_language="en",
            personal=personal,
            skills=details.skills,
            transferable_skills=details.transferable_skills,
            soft_skills=details.soft_skills,
            projects=projects,
            experience=experience,
            education=education,
            languages=languages,
            additional=aditional
        )

        return result
