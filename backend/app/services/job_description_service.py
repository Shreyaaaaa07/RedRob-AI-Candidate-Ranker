import re


class JobDescriptionService:

    def parse(self, text: str):

        skills = [
            "Python",
            "Java",
            "C++",
            "SQL",
            "FastAPI",
            "React",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "LLMs",
            "LangChain",
            "Vector Database",
            "Docker",
            "AWS",
            "Git",
            "Pandas",
            "NumPy",
            "Scikit-learn",
        ]

        found_skills = [
            skill for skill in skills
            if skill.lower() in text.lower()
        ]

        experience = "Not Specified"

        exp = re.search(r"(\d+\+?\s*(?:years?|yrs?))", text, re.I)

        if exp:
            experience = exp.group(1)

        education = "Not Specified"

        if "bachelor" in text.lower():
            education = "Bachelor's Degree"

        elif "master" in text.lower():
            education = "Master's Degree"

        return {

            "required_skills": found_skills,

            "experience": experience,

            "education": education,

            "keywords": found_skills,

            "job_role": self.extract_role(text),

        }

    def extract_role(self, text):

        lines = text.split("\n")

        if len(lines):

            return lines[0]

        return "Unknown"