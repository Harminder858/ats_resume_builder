# app/ats_matcher/jd_parser.py

from transformers import pipeline
import re

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def parse_job_description(jd_text):
    # Basic cleaning
    jd_text = re.sub(r'\s+', ' ', jd_text)

    # Define the sections we want to extract
    sections = ['job title', 'requirements', 'responsibilities', 'qualifications', 'skills']

    # Split the job description into sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', jd_text)

    parsed_jd = {section: [] for section in sections}

    # Classify each sentence
    for sentence in sentences:
        result = classifier(sentence, sections)
        best_match = result['labels'][0]
        if result['scores'][0] > 0.7:  # Only consider high-confidence classifications
            parsed_jd[best_match].append(sentence)

    # Extract job title
    parsed_jd['title'] = extract_job_title(parsed_jd['job title'])
    del parsed_jd['job title']

    return parsed_jd

def extract_job_title(job_title_sentences):
    if job_title_sentences:
        return job_title_sentences[0]  # Assume the first sentence classified as 'job title' is the actual title
    return None

