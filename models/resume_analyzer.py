import os
import re


# =====================================================
# Load Technical Skills
# =====================================================

def load_skills():

    skills_path = os.path.join("dataset", "skills.txt")

    skills = []

    try:

        with open(skills_path, "r", encoding="utf-8") as file:

            for line in file:

                line = line.strip().lower()

                if line:

                    skills.append(line)

    except FileNotFoundError:

        print("skills.txt not found.")

    return skills


TECHNICAL_SKILLS = load_skills()


# =====================================================
# Section Aliases
# =====================================================

SECTION_ALIASES = {

    "summary": [
        "summary",
        "professional summary",
        "profile",
        "career objective",
        "objective"
    ],

    "education": [
        "education",
        "academic background",
        "qualification",
        "qualifications"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "internship"
    ],

    "projects": [
        "projects",
        "project",
        "academic projects",
        "personal projects",
        "research projects"
    ],

    "skills": [
        "skills",
        "technical skills",
        "core skills"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "license",
        "licenses"
    ]

}
# =====================================================
# Helper Functions
# =====================================================

def has_section(text, section):

    text = text.lower()

    aliases = SECTION_ALIASES.get(section, [])

    return any(alias in text for alias in aliases)


def count_skills(text):

    text = text.lower()

    found = set()

    for skill in TECHNICAL_SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            found.add(skill)

    return len(found)


def detect_links(text):

    text = text.lower()

    github = any(

        word in text

        for word in [

            "github",

            "github.com",

            "github.io"

        ]

    )

    linkedin = any(

        word in text

        for word in [

            "linkedin",

            "linkedin.com"

        ]

    )

    return github, linkedin


def check_contact_details(text):

    email = bool(

        re.search(

            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

            text

        )

    )

    phone = bool(

        re.search(

            r"(\+91[\s-]?)?[6-9]\d{9}",

            text

        )

    )

    return email, phone
# =====================================================
# Resume Evaluation
# =====================================================

def evaluate_resume(text):

    score = 0

    strengths = []

    weaknesses = []

    suggestions = []

    text_lower = text.lower()

    email, phone = check_contact_details(text)

    github, linkedin = detect_links(text)

    skill_count = count_skills(text)

    # ---------------------------------------------
    # Contact Details
    # ---------------------------------------------

    if email:

        score += 5

        strengths.append("Professional email address found.")

    else:

        weaknesses.append("Email address is missing.")

        suggestions.append("Add a professional email address.")

    if phone:

        score += 5

        strengths.append("Contact number is available.")

    else:

        weaknesses.append("Phone number is missing.")

        suggestions.append("Include your contact number.")

    # ---------------------------------------------
    # Summary
    # ---------------------------------------------

    if has_section(text_lower, "summary"):

        score += 10

        strengths.append("Professional summary is included.")

    else:

        weaknesses.append("Professional summary is missing.")

        suggestions.append(
            "Add a short professional summary highlighting your skills and career goals."
        )

    # ---------------------------------------------
    # Education
    # ---------------------------------------------

    if has_section(text_lower, "education"):

        score += 10

        strengths.append("Education section is present.")

    else:

        weaknesses.append("Education section is missing.")

        suggestions.append("Include your educational qualifications.")

    # ---------------------------------------------
    # Experience
    # ---------------------------------------------

    if has_section(text_lower, "experience"):

        score += 15

        strengths.append("Experience or internship section is available.")

    else:

        weaknesses.append("Experience section is missing.")

        suggestions.append(
            "Include internship, freelance or work experience if available."
        )

    # ---------------------------------------------
    # Projects
    # ---------------------------------------------

    if has_section(text_lower, "projects"):

        score += 20

        strengths.append("Projects demonstrate practical experience.")

    else:

        weaknesses.append("Projects section is missing.")

        suggestions.append(
            "Include at least one academic or personal project."
        )

    # ---------------------------------------------
    # Certifications
    # ---------------------------------------------

    if has_section(text_lower, "certifications"):

        score += 10

        strengths.append("Certifications strengthen your profile.")

    else:

        weaknesses.append("Certifications section is missing.")

        suggestions.append(
            "Add relevant certifications to showcase continuous learning."
        )
            # ---------------------------------------------
    # Technical Skills
    # ---------------------------------------------

    if skill_count >= 12:

        score += 20

        strengths.append("Excellent technical skill set.")

    elif skill_count >= 8:

        score += 16

        strengths.append("Good technical skill set.")

    elif skill_count >= 5:

        score += 12

        strengths.append("Relevant technical skills are included.")

    elif skill_count >= 3:

        score += 8

        strengths.append("Basic technical skills are present.")

        suggestions.append(
            "Adding more relevant technical skills can strengthen your resume."
        )

    else:

        weaknesses.append("Very few technical skills detected.")

        suggestions.append(
            "Mention programming languages, frameworks and tools relevant to your field."
        )

    # ---------------------------------------------
    # GitHub
    # ---------------------------------------------

    if github:

        score += 3

        strengths.append("GitHub profile detected.")

    else:

        weaknesses.append("GitHub profile is missing.")

        suggestions.append(
            "Add your GitHub profile to showcase your coding projects."
        )

    # ---------------------------------------------
    # LinkedIn
    # ---------------------------------------------

    if linkedin:

        score += 2

        strengths.append("LinkedIn profile detected.")

    else:

        weaknesses.append("LinkedIn profile is missing.")

        suggestions.append(
            "Include your LinkedIn profile to improve professional visibility."
        )
            # ---------------------------------------------
    # Project Description Quality
    # ---------------------------------------------

    action_verbs = [

        "developed",
        "designed",
        "implemented",
        "built",
        "created",
        "optimized",
        "integrated",
        "deployed",
        "engineered",
        "automated"

    ]

    verb_count = 0

    for verb in action_verbs:

        if verb in text_lower:

            verb_count += 1

    if has_section(text_lower, "projects"):

        if verb_count >= 3:

            strengths.append(
                "Project descriptions are action-oriented."
            )

        else:

            suggestions.append(
                "Use action verbs like 'Developed', 'Designed' or 'Implemented' in project descriptions."
            )

    # ---------------------------------------------
    # Final Score
    # ---------------------------------------------

    score = min(score, 100)

    strengths = list(dict.fromkeys(strengths))
    weaknesses = list(dict.fromkeys(weaknesses))
    suggestions = list(dict.fromkeys(suggestions))

    return {

        "resume_score": score,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "suggestions": suggestions

    }


# =====================================================
# Main Function
# =====================================================

def analyze_resume(text):

    return evaluate_resume(text)
