# ATS Resume Matcher

## Description

ATS Resume Matcher is an advanced tool that leverages Natural Language Processing (NLP) and Large Language Models (LLM) to compare resumes against job descriptions. It provides detailed matching scores and suggestions for improving resume alignment with specific job requirements.

## Features

- Parse resumes and job descriptions using LLM-based classification
- Calculate similarity scores between resumes and job descriptions
- Provide section-wise matching scores (skills, education, experience)
- Generate personalized suggestions for resume improvement
- Interactive web dashboard for easy use

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Harminder858/ats_resume_builder.git
   cd ats_resume_builder
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Download the necessary model:
   ```
   python -m spacy download en_core_web_sm
   ```

## Usage

1. Run the Flask application:
   ```
   python app/main.py
   ```

2. Open a web browser and navigate to `http://localhost:5000` to access the dashboard.

3. Input the job description and your resume in the provided text areas.

4. Click "Match Resume" to see your matching scores and suggestions for improvement.

## Project Structure

```
ats_resume_builder/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── dashboard.py
│   └── ats_matcher/
│       ├── __init__.py
│       ├── resume_parser.py
│       ├── jd_parser.py
│       ├── matcher.py
│       └── scorer.py
│
├── data/
│   ├── skills_database.json
│   └── industry_keywords.json
│
├── tests/
│   ├── __init__.py
│   ├── test_resume_parser.py
│   ├── test_jd_parser.py
│   └── test_matcher.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Testing

Run the tests using pytest:
```
pytest tests/
```

## Contributing

Contributions to improve ATS Resume Matcher are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

harminderpuri18@gmail.com

Project Link: [https://github.com/Harminder858/ats_resume_builder](https://github.com/Harminder858/ats_resume_builder)

## Acknowledgements

- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Flask](https://flask.palletsprojects.com/)
- [Dash](https://dash.plotly.com/)
- [spaCy](https://spacy.io/)
