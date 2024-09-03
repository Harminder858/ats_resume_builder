# tests/test_matcher.py

import unittest
from app.ats_matcher.matcher import match_resume_to_jd
from app.ats_matcher.resume_parser import parse_resume
from app.ats_matcher.jd_parser import parse_job_description

class TestMatcher(unittest.TestCase):
    def setUp(self):
        self.sample_resume = """
        John Doe
        john.doe@email.com
        123-456-7890

        Education:
        Bachelor of Science in Computer Science, University of Example, 2020

        Work Experience:
        Software Developer, Tech Corp, 2020-Present
        - Developed web applications using Python and JavaScript
        - Collaborated with cross-functional teams to deliver high-quality software

        Skills:
        Python, JavaScript, HTML, CSS, SQL, Git
        """

        self.sample_jd = """
        Job Title: Senior Software Engineer

        Requirements:
        - Bachelor's degree in Computer Science or related field
        - 5+ years of experience in software development
        - Proficiency in Python and JavaScript

        Responsibilities:
        - Design and implement scalable software solutions
        - Collaborate with cross-functional teams to define and develop new features
        - Mentor junior developers and contribute to team's growth

        Skills:
        Python, JavaScript, SQL, AWS, Agile methodologies
        """

    def test_match_resume_to_jd(self):
        parsed_resume = parse_resume(self.sample_resume)
        parsed_jd = parse_job_description(self.sample_jd)

        match_result = match_resume_to_jd(parsed_jd, parsed_resume)

        self.assertIn('overall_score', match_result)
        self.assertIn('scores', match_result)
        self.assertIn('suggestions', match_result)

        self.assertTrue(0 <= match_result['overall_score'] <= 10)
        self.assertTrue(all(0 <= score <= 10 for score in match_result['scores'].values()))
        self.assertTrue(isinstance(match_result['suggestions'], list))

    def test_empty_inputs(self):
        parsed_resume = parse_resume("")
        parsed_jd = parse_job_description("")

        match_result = match_resume_to_jd(parsed_jd, parsed_resume)

        self.assertIn('overall_score', match_result)
        self.assertIn('scores', match_result)
        self.assertIn('suggestions', match_result)

        self.assertEqual(match_result['overall_score'], 0)
        self.assertTrue(all(score == 0 for score in match_result['scores'].values()))
        self.assertTrue(isinstance(match_result['suggestions'], list))

if __name__ == '__main__':
    unittest.main()