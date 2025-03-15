import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json
import re
import os
import hashlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

genai.configure(api_key="AIzaSyCgifniJvV4nKfsC76MJE2tI3rnRPSkI2E")

def anonymize_data(data):
    """Hashes sensitive data to ensure privacy compliance."""
    return hashlib.sha256(data.encode()).hexdigest()

class HiringAssistant:
    def greeting_prompt(self):
        return """Welcome to TalentScout! 👋 I'm your AI hiring assistant, and I'll be helping you with the initial screening process. 
        I'll ask you a few questions to understand your background and technical expertise. Shall we begin?"""
    
    def name_prompt(self):
        return "Please enter your full name:"

    def email_prompt(self):
        return "Please enter your email address:"

    def phone_prompt(self):
        return "Please enter your phone number (with country code if applicable):"

    def experience_prompt(self):
        return "How many years of professional experience do you have?"

    def position_prompt(self):
        return "What position(s) are you interested in applying for?"

    def location_prompt(self):
        return "What is your current location?"

    def tech_stack_prompt(self):
        return "Please list your technical skills, including programming languages, frameworks, and tools:"

    def technical_questions_prompt(self):
        return "Now, I'll ask you some technical questions based on your skills."

    def farewell_prompt(self):
        return "Thank you for completing the screening! We'll review your responses and get back to you soon. 👍"

    def __init__(self):
        self.steps = {
            'greeting': self.greeting_prompt,
            'name': self.name_prompt,
            'email': self.email_prompt,
            'phone': self.phone_prompt,
            'experience': self.experience_prompt,
            'position': self.position_prompt,
            'location': self.location_prompt,
            'tech_stack': self.tech_stack_prompt,
            'technical_questions': self.technical_questions_prompt,
            'farewell': self.farewell_prompt
        }
    
    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone) is not None
    
    def generate_technical_questions(self, tech_stack):
        prompt = f"""Generate 3-5 technical interview questions for a candidate proficient in: {tech_stack}. 
        Questions should be challenging and specific to assess deep understanding."""
        
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        return response.text if response else "Error generating questions."
    
    def process_user_input(self, user_input):
        current_step = st.session_state.current_step
        
        if current_step == 'greeting':
            st.session_state.current_step = 'name'
            return self.name_prompt()
            
        elif current_step == 'name':
            st.session_state.candidate_info['name'] = anonymize_data(user_input)
            st.session_state.current_step = 'email'
            return self.email_prompt()
            
        elif current_step == 'email':
            if not self.validate_email(user_input):
                return "Please provide a valid email address."
            st.session_state.candidate_info['email'] = anonymize_data(user_input)
            st.session_state.current_step = 'phone'
            return self.phone_prompt()
            
        elif current_step == 'phone':
            if not self.validate_phone(user_input):
                return "Please provide a valid phone number."
            st.session_state.candidate_info['phone'] = anonymize_data(user_input)
            st.session_state.current_step = 'experience'
            return self.experience_prompt()
            
        elif current_step == 'experience':
            st.session_state.candidate_info['experience'] = user_input
            st.session_state.current_step = 'position'
            return self.position_prompt()
            
        elif current_step == 'position':
            st.session_state.candidate_info['position'] = user_input
            st.session_state.current_step = 'location'
            return self.location_prompt()
            
        elif current_step == 'location':
            st.session_state.candidate_info['location'] = anonymize_data(user_input)
            st.session_state.current_step = 'tech_stack'
            return self.tech_stack_prompt()
            
        elif current_step == 'tech_stack':
            st.session_state.candidate_info['tech_stack'] = user_input
            questions = self.generate_technical_questions(user_input)
            st.session_state.current_step = 'technical_questions'
            return f"Based on your tech stack, here are some technical questions:\n\n{questions}"
            
        elif current_step == 'technical_questions':
            st.session_state.current_step = 'farewell'
            return self.farewell_prompt()


def main():
    st.title("TalentScout Hiring Assistant 🤖")
    st.write("Your AI-powered technical screening assistant")
    
    assistant = HiringAssistant()
    
    # Initialize chat
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'greeting'
    if 'candidate_info' not in st.session_state:
        st.session_state.candidate_info = {}
    
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({"role": "assistant", "content": assistant.greeting_prompt()})
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Get user input
    if user_input := st.chat_input("Type your response..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
            
        # Get assistant response
        response = assistant.process_user_input(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

if __name__ == "__main__":
    main()
