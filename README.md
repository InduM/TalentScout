# chatbot-app
 
README File:
Project Overview: Brief description of the Hiring Assistant chatbot and its capabilities.
 "TalentScout" is an intelligent Hiring Assistant chatbot for a fictional recruitment agency specializing in technology placements. This chatbot assists in the initial screening of candidates by gathering essential information and posing relevant technical questions based on the candidate's declared tech stack. 


Installation Instructions: Detailed steps to set up and run the application locally.

Clone the repository:

git clone https://github.com/InduM/TalentScout
cd TalentScout

Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Set up environment variables:
Create a .env file in the project root

Run the application:

streamlit run app.py


Usage Guide: Clear and Concise Readme file.
Starting the Interview.Launch the application.During the Interview the system will generate relevant technical questions
Candidates can type their responses.Follow-up questions will be generated based on responses


Technical Details: Libraries used, model details, and architectural decisions.
Tech Stack:
Frontend: Streamlit
Backend: Python
AI Integration: Hugging Face API
State Management: Streamlit session stat


Prompt Design: Explanation of how prompts were crafted to handle information gathering and technical question generation.
Challenges & Solutions: Discuss any challenges faced during development and how they were addressed.