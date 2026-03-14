# import pdfplumber
# import re
# # import spacy

# # # nlp = spacy.load("en_core_web_sm")
# # nlp = None  # Global variable

# # def get_nlp():
# #     global nlp
# #     if nlp is None:
# #         nlp = spacy.load("en_core_web_sm")
# #     return nlp

# COMMON_SKILLS = [
#     "python","java","c++","react","node","mongodb",
#     "mysql","docker","kubernetes","aws","html",
#     "css","javascript","fastapi","spring","django"
# ]

# def parse_resume(file_path):
#     text = ""
#     with pdfplumber.open(file_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() or ""

#     email = re.search(r'\S+@\S+', text)
#     phone = re.search(r'\+?\d[\d\s\-]{8,15}', text)

#     name = ""
#     # doc = nlp(text)
#     # 🔽 THIS is where it goes
#     doc = get_nlp()(text)


#     for ent in doc.ents:
#         if ent.label_ == "PERSON":
#             name = ent.text
#             break

#     skills = [s for s in COMMON_SKILLS if s in text.lower()]

#     return {
#         "name": name,
#         "email": email.group(0) if email else "",
#         "phone": phone.group(0) if phone else "",
#         "skills": list(set(skills)),
#         "raw_text": text
#     }






# import spacy
# import pdfplumber

# # Load spacy model once
# nlp = spacy.load("en_core_web_sm")


# def get_nlp():
#     return nlp


# def extract_text_from_pdf(path: str):
#     text = ""

#     with pdfplumber.open(path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() or ""

#     return text


# def parse_resume(path: str):
#     text = extract_text_from_pdf(path)

#     doc = get_nlp()(text)

#     skills = []
#     emails = []
#     names = []

#     for ent in doc.ents:
#         if ent.label_ == "PERSON":
#             names.append(ent.text)
#         if ent.label_ == "ORG":
#             skills.append(ent.text)

#     for token in doc:
#         if "@" in token.text:
#             emails.append(token.text)

#     return {
#         "name": list(set(names)),
#         "skills": list(set(skills)),
#         "email": list(set(emails)),
#         "text": text[:1000]
#     }





# import spacy
# import pdfplumber

# nlp = spacy.load("en_core_web_sm")

# def get_nlp():
#     return nlp

# def extract_text_from_pdf(path):
#     text = ""

#     with pdfplumber.open(path) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text

#     return text

# def parse_resume(path):
#     text = extract_text_from_pdf(path)

#     if not text:
#         return {"error": "No text extracted from resume"}

#     doc = get_nlp()(text)

#     names = []
#     emails = []

#     for ent in doc.ents:
#         if ent.label_ == "PERSON":
#             names.append(ent.text)

#     for token in doc:
#         if "@" in token.text:
#             emails.append(token.text)

#     return {
#         "name": list(set(names)),
#         "email": list(set(emails)),
#         "text": text[:1000]
#     }



import spacy
import pdfplumber
import re

nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(path):
    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def extract_email(text):
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    emails = re.findall(email_pattern, text)
    return emails


def extract_name(text):
    lines = text.split("\n")

    for line in lines[:5]:
        line = line.strip()

        if len(line.split()) <= 4 and line.isupper():
            return line.title()

    return lines[0]


def extract_skills(text):

    skills_db = [
        "python","java","machine learning","deep learning",
        "data science","springboot","javascript",
        "html","css","react","node","mongodb",
        "sql","c++","c","oop","data structures",
        "artificial intelligence","computer vision"
    ]

    text_lower = text.lower()

    found_skills = []

    for skill in skills_db:
        if skill in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))


def parse_resume(path):

    text = extract_text_from_pdf(path)

    name = extract_name(text)

    emails = extract_email(text)

    skills = extract_skills(text)

    return {
        "name": name,
        "email": emails,
        "skills": skills,
        "text_preview": text[:500]
    }