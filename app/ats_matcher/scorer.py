# app/ats_matcher/scorer.py

from transformers import pipeline
import numpy as np

# Initialize the feature-extraction pipeline
feature_extractor = pipeline("feature-extraction", model="distilbert-base-uncased")

def extract_features(text):
    features = feature_extractor(text, return_tensors=True)
    return np.mean(features[0], axis=1).squeeze()

def calculate_similarity(text1, text2):
    features1 = extract_features(text1)
    features2 = extract_features(text2)
    return np.dot(features1, features2) / (np.linalg.norm(features1) * np.linalg.norm(features2))

def score_resume(parsed_resume, parsed_jd):
    scores = {}

    # Score overall similarity
    resume_text = ' '.join([' '.join(section) if isinstance(section, list) else section for section in parsed_resume.values()])
    jd_text = ' '.join([' '.join(section) if isinstance(section, list) else section for section in parsed_jd.values()])
    scores['overall_similarity'] = calculate_similarity(resume_text, jd_text) * 10

    # Score skills match
    if 'skills' in parsed_resume and 'skills' in parsed_jd:
        resume_skills = ' '.join(parsed_resume['skills'])
        jd_skills = ' '.join(parsed_jd['skills'])
        scores['skills_match'] = calculate_similarity(resume_skills, jd_skills) * 10

    # Score education match
    if 'education' in parsed_resume and 'requirements' in parsed_jd:
        resume_education = ' '.join(parsed_resume['education'])
        jd_requirements = ' '.join(parsed_jd['requirements'])
        scores['education_match'] = calculate_similarity(resume_education, jd_requirements) * 10

    # Score experience match
    if 'work experience' in parsed_resume and 'responsibilities' in parsed_jd:
        resume_experience = ' '.join(parsed_resume['work experience'])
        jd_responsibilities = ' '.join(parsed_jd['responsibilities'])
        scores['experience_match'] = calculate_similarity(resume_experience, jd_responsibilities) * 10

    # Calculate overall score
    scores['overall_score'] = np.mean(list(scores.values()))

    return scores

def generate_suggestions(scores, parsed_resume, parsed_jd):
    suggestions = []

    if scores.get('skills_match', 0) < 7:
        missing_skills = set(parsed_jd.get('skills', [])) - set(parsed_resume.get('skills', []))
        if missing_skills:
            suggestions.append(f"Consider adding these skills to your resume: {', '.join(missing_skills)}")
        else:
            suggestions.append("Try to highlight your skills more effectively in your resume.")

    if scores.get('education_match', 0) < 7:
        suggestions.append("Your education might not fully match the job requirements. Consider highlighting relevant coursework or certifications.")

    if scores.get('experience_match', 0) < 7:
        suggestions.append("Your work experience could be more closely aligned with the job responsibilities. Try to emphasize relevant projects or achievements.")

    if scores['overall_similarity'] < 7:
        suggestions.append("Your resume could be more closely aligned with the job description. Try using more key terms from the job posting throughout your resume.")

    return suggestions