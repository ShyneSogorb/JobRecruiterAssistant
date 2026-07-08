from src.ai.prompts import PromptBuilder
from src.jobs.parser import JobOfferParser
from src.ai.client import AIClient
import os

def main():
    ai = AIClient()

    prompts = PromptBuilder()

    parser = JobOfferParser(ai, prompts)

    with open("job.txt", encoding="utf8") as f:
        offer = f.read()

    job = parser.parse(offer)

    job_string = job.model_dump_json(indent=4)
    filename = f"./test/data/{job.company}_offer.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf8") as f:
        f.write(job_string)

    print(job_string)


if __name__ == "__main__":
    main()