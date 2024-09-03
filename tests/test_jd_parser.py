# tests/test_jd_parser.py

import unittest
from app.ats_matcher.jd_parser import parse_job_description

class TestJDParser(unittest.TestCase):
    def setUp(self):
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

        Qualifications:
        - Strong problem-solving skills
        - Excellent communication skills
        - Experience with Agile methodologies

        Skills:
        Python, JavaScript, SQL, AWS, Agile methodologies
        """

    def test_parse_job_description(self):
        parsed_jd = parse_job_description(self.sample_jd)

        self.assertIn('title', parsed_jd)
        self.assertIn('requirements', parsed_jd)
        self.assertIn('responsibilities', parsed_jd)
        self.assertIn('qualifications', parsed_jd)
        self.assertIn('skills', parsed_jd)

        self.assertTrue('Senior Software Engineer' in parsed_jd['title'])
        self.assertTrue(any('Bachelor's degree' in req for req in parsed_jd['requirements']))
        self.assertTrue(any('Design and implement' in resp for resp in parsed_jd['responsibilities']))
        self.assertTrue(any('Strong problem-solving skills' in qual for qual in parsed_jd['qualifications']))
        self.assertTrue(any('Python' in skill for skill in parsed_jd['skills']))

    def test_empty_jd(self):
        parsed_jd = parse_job_description("")
        self.assertEqual(parsed_jd, {'title': None, 'requirements': [], 'responsibilities': [], 'qualifications': [], 'skills': []})

if __name__ == '__main__':
    unittest.main()