# app/ats_matcher/matcher.py

from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize the feature-extraction pipeline
feature_extractor = pipeline("feature-extraction", model="distilbert-base-uncased")

def extract_features(text):
    features = feature_extractor(text, return_tensors=True)
    return np.mean(features[0], axis=1).squeeze()

def calculate_similarity(text1, text2):
    features1 = extract_features(text1)
    features2 = extract_features(text2)
    return cosine_similarity(features1.reshape(1, -1), features2.reshape(1, -1))[0][0]

def match_resume_to_jd(parsed_jd, parsed_resume):
    scores = {}

    # Calculate overall similarity
    jd_text = ' '.join([' '.join(section) for section in parsed_jd.values() if isinstance(section, list)])
    resume_text = ' '.join([' '.join(section) for section in parsed_resume.values() if isinstance(section, list)])
    scores['overall_similarity'] = calculate_similarity(jd_text, resume_text) * 10

    # Calculate similarity for each section
    for section in ['requirements', 'responsibilities', 'skills']:
        if section in parsed_jd and section in parsed_resume:
            jd_section = ' '.join(parsed_jd[section])
            resume_section = ' '.join(parsed_resume[section])
            scores[f'{section}_match'] = calculate_similarity(jd_section, resume_section) * 10

    # Calculate education match (assuming education is a list of strings)
    if 'education' in parsed_resume and 'requirements' in parsed_jd:
        education_text = ' '.join(parsed_resume['education'])
        requirements_text = ' '.join(parsed_jd['requirements'])
        scores['education_match'] = calculate_similarity(education_text, requirements_text) * 10

    # Calculate experience match (assuming experience is a list of strings)
    if 'work experience' in parsed_resume and 'responsibilities' in parsed_jd:
        experience_text = ' '.join(parsed_resume['work experience'])
        responsibilities_text = ' '.join(parsed_jd['responsibilities'])
        scores['experience_match'] = calculate_similarity(experience_text, responsibilities_text) * 10

    # Calculate overall score
    scores['overall_score'] = np.mean(list(scores.values()))

    # Generate suggestions
    suggestions = generate_suggestions(scores, parsed_resume, parsed_jd)

    return {
        'overall_score': scores['overall_score'],
        'scores': scores,
        'suggestions': suggestions
    }

def generate_suggestions(scores, parsed_resume, parsed_jd):
    suggestions = []

    if scores.get('skills_match', 0) < 7:
        suggestions.append("Consider adding more relevant skills from the job description to your resume.")

    if scores.get('experience_match', 0) < 7:
        suggestions.append("Try to highlight experiences that are more closely related to the job responsibilities.")

    if scores.get('education_match', 0) < 7:
        suggestions.append("Ensure your education section meets the requirements specified in the job description.")

    if scores['overall_similarity'] < 7:
        suggestions.append("Your resume could be more closely aligned with the job description. Try using more key terms from the job posting throughout your resume.")

    return suggestions