Project Overview
The Hiring Assistant Chatbot is an AI-driven application designed to streamline the initial stages of the recruitment process. It interacts with candidates to gather essential information, assesses their technical expertise through tailored questions, and ensures data privacy by anonymizing sensitive details. This chatbot aims to enhance the efficiency of hiring by automating preliminary screenings and providing consistent evaluations.

Installation Instructions
To set up and run the Hiring Assistant Chatbot locally, follow these steps:
Clone the Repository:
git clone surajmungath/hiring-assistant-chatbot.git
cd hiring-assistant-chatbot

Create and Activate a Virtual Environment:

python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

Install Dependencies:

pip install -r requirements.txt

Set Up Environment Variables: Create a .env file in the project root directory and add your Gemini API key:

GEMINI_API_KEY=your_gemini_api_key

Run the Application:

Python -m streamlit run app.py
 Open the provided URL in your web browser to interact with the chatbot.




Usage Guide
Start the Application: Launch the chatbot using the instructions above.


Interact with the Chatbot: The chatbot will guide you through a series of prompts to collect information such as your name, email, phone number, years of experience, desired position, location, and technical skills.


Answer Technical Questions: Based on your provided technical skills, the chatbot will generate and present relevant technical interview questions.


Completion: After answering the questions, the chatbot will conclude the session and inform you about the next steps.


Technical Details
Programming Language: Python
Framework: Streamlit for the web interface
AI Model: Gemini API for generating technical questions
Libraries Used:
hashlib for data anonymization
re for input validation
dotenv for environment variable management
