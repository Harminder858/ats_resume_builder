# tests/test_resume_parser.py

import unittest
from app.ats_matcher.resume_parser import parse_resume

class TestResumeParser(unittest.TestCase):
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

    def test_parse_resume(self):
        parsed_resume = parse_resume(self.sample_resume)

        self.assertIn('contact_info', parsed_resume)
        self.assertIn('education', parsed_resume)
        self.assertIn('work experience', parsed_resume)
        self.assertIn('skills', parsed_resume)

        self.assertEqual(parsed_resume['contact_info']['email'], 'john.doe@email.com')
        self.assertEqual(parsed_resume['contact_info']['phone'], '123-456-7890')
        
        self.assertTrue(any('Bachelor of Science in Computer Science' in edu for edu in parsed_resume['education']))
        self.assertTrue(any('Software Developer' in exp for exp in parsed_resume['work experience']))
        self.assertTrue(any('Python' in skill for skill in parsed_resume['skills']))

    def test_empty_resume(self):
        parsed_resume = parse_resume("")
        self.assertEqual(parsed_resume, {'contact_info': {'email': None, 'phone': None}, 'education': [], 'work experience': [], 'skills': []})

if __name__ == '__main__':
    unittest.main()