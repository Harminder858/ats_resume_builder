# app/ats_matcher/resume_parser.py

from transformers import pipeline
import re

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def parse_resume(resume_text):
    # Basic cleaning
    resume_text = re.sub(r'\s+', ' ', resume_text)

    # Define the sections we want to extract
    sections = ['contact information', 'education', 'work experience', 'skills']

    # Split the resume into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', resume_text)

    parsed_resume = {section: [] for section in sections}

    # Classify each sentence
    for sentence in sentences:
        result = classifier(sentence, sections)
        best_match = result['labels'][0]
        if result['scores'][0] > 0.7:  # Only consider high-confidence classifications
            parsed_resume[best_match].append(sentence)

    # Extract specific information from contact information
    parsed_resume['contact_info'] = extract_contact_info(parsed_resume['contact information'])
    del parsed_resume['contact information']

    return parsed_resume

def extract_contact_info(contact_info_sentences):
    email = None
    phone = None
    for sentence in contact_info_sentences:
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', sentence)
        if email_match and not email:
            email = email_match.group(0)
        phone_match = re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', sentence)
        if phone_match and not phone:
            phone = phone_match.group(0)
    return {'email': email, 'phone': phone}

