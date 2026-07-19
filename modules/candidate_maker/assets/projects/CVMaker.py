import os

DATA = """CV Maker
(No further details provided in the original data - likely the tool used to help generate structured CVs like this one.)
"""


def load():
    code = dict[str, str]()
    root = r"C:\Users\user\Documents\MyProjects\CVMaker"
    
    with open(os.path.join(root, "build.js")) as f:
        code["build.js"] = f.read()

    with open(os.path.join(root, "templates", "cv.en.ejs")) as f:
        code["cv.ejs"] = f.read()

    with open(os.path.join(root, "styles", "style.css")) as f:
        code["style.css"] = f.read()

    return """
{
  "project": {
    "name": "",
    "description": "An EJS-based HTML resume template that conditionally renders CV sections from structured input data while remaining ATS-friendly and supporting multiple languages.",
    "achievements": [
      {
        "context": "The template must support incomplete datasets without failing when optional fields are missing.",
        "action": "Implemented reusable helper functions to safely retrieve values and determine whether fields should be rendered before accessing or displaying them.",
        "impact": "Allows the same template to render resumes from partially populated data without runtime errors or empty sections.",
        "metric": null,
        "keywords": []
      },
      {
        "context": "A resume needs to display different information depending on the available candidate data.",
        "action": "Built conditional rendering for sections including header, contact information, summary, professional experience, projects, skills, languages, education, and additional information.",
        "impact": "Produces a dynamically generated resume that only includes populated sections.",
        "metric": null,
        "keywords": []
      },
      {
        "context": "Professional experience and projects contain collections of structured entries.",
        "action": "Implemented iteration over structured datasets to render jobs, projects, descriptions, dates, and bullet points.",
        "impact": "Supports generating resumes from structured data with reusable layouts.",
        "metric": null,
        "keywords": []
      },
      {
        "context": "The template should be reusable across multiple resume languages.",
        "action": "Created language-specific EJS templates sharing a common rendering approach.",
        "impact": "Enables generating resumes for multiple languages from the same structured data model.",
        "metric": null,
        "keywords": []
      }
    ],
    "technologies": [
      {
        "name": "EJS",
        "abbreviation": null,
        "category": null
      },
      {
        "name": "HTML",
        "abbreviation": null,
        "category": null
      },
      {
        "name": "CSS",
        "abbreviation": null,
        "category": null
      },
      {
        "name": "JavaScript",
        "abbreviation": null,
        "category": null
      }
    ],
    "date": null
  },
  "details": {
    "skills": [
      {
        "name": "EJS Templating"
      },
      {
        "name": "HTML"
      },
      {
        "name": "CSS"
      },
      {
        "name": "JavaScript"
      },
      {
        "name": "Template Development"
      },
      {
        "name": "Conditional Rendering"
      },
      {
        "name": "Dynamic Document Generation"
      },
      {
        "name": "Structured Data Rendering"
      }
    ],
    "soft_skills": [],
    "transferable_skills": [
      {
        "name": "Template Design"
      },
      {
        "name": "Data Presentation"
      },
      {
        "name": "Document Automation"
      },
      {
        "name": "Reusable Component Design"
      }
    ]
  }
}
"""