# views.py

from django.shortcuts import render
from PyPDF2 import PdfReader
from docx import Document
import os


# ROLE SKILLS

ROLE_SKILLS = {

    "Django Developer": {

        "must": ["python", "django", "sql"],

        "good": ["api", "bootstrap", "html", "css"],

        "bonus": ["rest api", "git", "javascript"]
    },

    "Frontend Developer": {

        "must": ["html", "css", "javascript"],

        "good": ["bootstrap", "react"],

        "bonus": ["tailwind", "ui/ux"]
    },

    "Backend Developer": {

        "must": ["python", "django", "sql"],

        "good": ["api", "authentication"],

        "bonus": ["docker", "aws"]
    },

    "Python Developer": {

        "must": ["python"],

        "good": ["django", "flask", "api"],

        "bonus": ["automation", "oop"]
    }

}


# EXTRACT TEXT

def extract_text(file_path):

    text = ""

    # PDF FILE

    if file_path.endswith(".pdf"):

        try:

            reader = PdfReader(file_path)

            for page in reader.pages:

                extracted = page.extract_text()

                if extracted:

                    text += extracted.lower()

        except:

            text = ""

    # DOCX FILE

    elif file_path.endswith(".docx"):

        try:

            doc = Document(file_path)

            for para in doc.paragraphs:

                text += para.text.lower()

        except:

            text = ""

    return text


# HOME VIEW

def home(request):

    result = None
    error = None

    if request.method == "POST":

        name = request.POST.get("name")

        role = request.POST.get("role")

        resume = request.FILES.get("resume")

        # CHECK FILE

        if not resume:

            error = "Please upload a resume."

            return render(request, "home.html", {

                "error": error
            })

        # FILE VALIDATION

        allowed_extensions = [".pdf", ".docx"]

        ext = os.path.splitext(resume.name)[1].lower()

        if ext not in allowed_extensions:

            error = "Only PDF and DOCX files are allowed."

            return render(request, "home.html", {

                "error": error
            })

        # CREATE FOLDER

        os.makedirs("media/resumes", exist_ok=True)

        # SAVE FILE

        save_path = f"media/resumes/{resume.name}"

        with open(save_path, "wb+") as destination:

            for chunk in resume.chunks():

                destination.write(chunk)

        # EXTRACT TEXT

        text = extract_text(save_path)

        # EMPTY TEXT CHECK

        if not text:

            error = "Unable to read this resume file."

            return render(request, "home.html", {

                "error": error
            })

        # ROLE DATA

        role_data = ROLE_SKILLS.get(role)

        must_skills = role_data["must"]

        good_skills = role_data["good"]

        bonus_skills = role_data["bonus"]

        # FINAL VARIABLES

        matched = []
        missing = []

        score = 25

        # MUST SKILLS

        for skill in must_skills:

            if skill in text:

                matched.append(skill)

                score += 12

            else:

                missing.append(skill)

                score -= 8

        # GOOD SKILLS

        for skill in good_skills:

            if skill in text:

                matched.append(skill)

                score += 6

            else:

                missing.append(skill)

                score -= 2

        # BONUS SKILLS

        for skill in bonus_skills:

            if skill in text:

                matched.append(skill)

                score += 2

        # PROJECT CHECK

        project_count = text.count("project")

        if project_count >= 2:

            score += 8

        elif project_count == 1:

            score += 4

        else:

            score -= 10

        # EXPERIENCE CHECK

        if "experience" in text:

            score += 4

        else:

            score -= 5

        # EDUCATION CHECK

        if "education" in text:

            score += 3

        else:

            score -= 5

        # GITHUB CHECK

        if "github" in text:

            score += 5

        else:

            score -= 5

        # LINKEDIN CHECK

        if "linkedin" in text:

            score += 5

        else:

            score -= 5

        # RESUME LENGTH CHECK

        word_count = len(text.split())

        if word_count < 80:

            score -= 15

        elif word_count < 150:

            score -= 5

        # TOO MANY MISSING SKILLS

        if len(missing) >= 3:

            score -= 15

        # FINAL LIMIT

        if score > 95:

            score = 95

        if score < 20:

            score = 20

        # FEEDBACK

        if score >= 85:

            feedback = "Excellent ATS optimized resume."

        elif score >= 70:

            feedback = "Good resume with strong technical skills."

        elif score >= 50:

            feedback = "Average resume. Improve skills and projects."

        else:

            feedback = "Resume lacks important ATS keywords."

        # SUGGESTIONS

        suggestions = []

        if missing:

            suggestions.append(

                f"Add missing skills: {', '.join(missing)}"
            )

        if "github" not in text:

            suggestions.append(

                "Add GitHub profile."
            )

        if "linkedin" not in text:

            suggestions.append(

                "Add LinkedIn profile."
            )

        if "certification" not in text:

            suggestions.append(

                "Add certifications section."
            )

        if project_count == 0:

            suggestions.append(

                "Add strong projects."
            )

        # FINAL RESULT

        result = {

            "name": name,

            "role": role,

            "score": score,

            "matched": matched,

            "missing": missing,

            "feedback": feedback,

            "suggestions": suggestions,

            "resume_url": "/" + save_path
        }

    return render(request, "home.html", {

        "result": result,

        "error": error
    })