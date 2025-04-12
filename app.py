import os
import requests
import streamlit as st
from dotenv import load_dotenv
from scripts import *
from db_scripts import *

load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}


# Session state initialization
if "state" not in st.session_state:
    st.session_state.state = "initial_info"
    st.session_state.user_data = {}
    st.session_state.history = []
    st.session_state.questions = []
    st.session_state.question_number = 0
    st.session_state.answers = []
    st.session_state.consent_given = False


exit_keywords = ['bye', 'exit', 'quit', 'stop']
accept_keywords = ['yes', 'agree', 'ok', 'okay', 'yup', 'yep', 'sure', 'definitely', 'absolutely','yeah']
delete_keywords = ['delete', 'delete data',"delete my data"]

# UI
st.title("TalentScout Hiring Chatbot")
# User input box
user_input = st.chat_input(placeholder="Say something...")

def generate_bot_reply(user_input):
    instruction = "Instruction: You are a senior technical interviewer assessing software engineering candidates."
    context = " ".join([x[1] for x in st.session_state.history[-5:] if x[0] == "user"])
    full_prompt = f"{instruction} Context: {context} User: {user_input}"
    return generate_reply_via_api(full_prompt)

def generate_reply_via_api(user_input):
    payload = {"inputs": user_input}
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"HuggingFace API Error: {response.text}")

    generated = response.json()
    if isinstance(generated, list):
        generated_text = generated[0]["generated_text"]
    else:
        generated_text = generated["generated_text"]

    return generated_text

def generate_questions_via_api(tech_stack, num_questions=5):
    tech_str = ", ".join(tech_stack)
    prompt = ( f"You are a technical interviewer. Generate {num_questions} interview questions"
              f"for a software engineer skilled in {tech_str}. List the questions immediately."
    )
    generated_text = generate_reply_via_api(prompt)
    questions = [line.strip("-•1234567890. ") for line in generated_text.split("\n") if "?" in line]
    return questions[:num_questions]
    
def store_data():
    db=st.session_state.user_data
    db['questions'] = st.session_state.questions
    db['answers'] = st.session_state.answers
    save_candidate(db)

def delete_data():
    delete_candidate(st.session_state.candidate_id)
    return "🧹 Your data has been permanently deleted."


def handle_input(user_input):
    if any(word in user_input.lower() for word in exit_keywords):
        st.session_state.state = 'end'
        if st.session_state.consent_given:
            return ("Thank you for your time.We’ve recorded your responses and our"
                    " team will be in touch soon. Goodbye!"
            )
        else:
            return "The interview has been terminated. Thank you for your time."
    
    if any(word in user_input.lower() for word in delete_keywords):
        st.session_state.state = 'delete'
        return delete_data()

    match st.session_state.state:
        case "initial_info":
            st.session_state.state = "greeting"
            return ("Hi! I’m TechScreenBot, here to help with your application. Before we begin,"
                    " please note that your responses will be recorded for recruitment purposes."
                     " Your data will not be shared with third parties, and you can request deletion"
                      " at any time. Do you agree to proceed?"
            )
        case "greeting":
            if any(word in user_input.lower() for word in accept_keywords):
                st.session_state.consent_given = True
                st.session_state.state = "info_name"
                return "Then let's begin. What's your full name?"
            else:
                st.session_state.consent_given = False
                st.session_state.state = "end"
                return "Consent is required to proceed with the interview."

        case "info_name":
            if validate_name(user_input):
                st.session_state.user_data['name'] = user_input
                st.session_state.state = "info_location" # change to info_email
                return "Thanks! May I have your email address?"
            else:
                return "Please enter a valid name."

        case "info_email":
            if validate_email(user_input):
                st.session_state.user_data['email'] = user_input
                st.session_state.state = "info_phone"
                return "Got it. Your phone number?"
            else:
                return "Please enter a valid email address."

        case "info_phone":
            if validate_phone(user_input):  
                st.session_state.user_data['phone'] = user_input
                st.session_state.state = "info_experience"
                return "How many years of experience do you have?"
            else:
                return "Please enter a valid phone number."

        case "info_experience":
            st.session_state.user_data['experience'] = user_input
            st.session_state.state = "info_position"
            return "Which position(s) are you interested in?"

        case "info_position":
            st.session_state.user_data['position'] = user_input
            st.session_state.state = "info_location"
            return "Where are you currently based?"

        case "info_location":
            st.session_state.user_data['location'] = user_input
            st.session_state.state = "info_tech_stack"
            return "Great. Could you list your tech stack? (e.g., Python, Django, React, MySQL)"

        case "info_tech_stack":
            techs = [t.strip().lower() for t in user_input.split(',')]
            st.session_state.user_data['tech_stack'] = techs
            questions = generate_questions_via_api(techs)
            st.session_state.questions.extend(questions)
            st.session_state.state = "awaiting_answers"
            return (f"Your profile has been saved with the id {st.session_state.candidate_id}."
                    " Please answer the following questions:\n" +st.session_state.questions[st.session_state.question_number]
            )
             
        case "awaiting_answers":
            st.session_state.answers.append(user_input)
            st.session_state.question_number += 1
            if st.session_state.question_number < len(st.session_state.questions):
                return st.session_state.questions[st.session_state.question_number]
            st.session_state.state = "chatting"
            st.session_state.candidate_id = store_data()
            return "Thanks for your answers!Type 'bye' to end the interview."

        case "chatting":
            return generate_bot_reply(user_input)
        
    return "Hmm... I didn't quite get that. Can you rephrase?"


# Handle user input
if user_input:
    st.session_state.history.append(("user", user_input))
    response = handle_input(user_input)
    st.session_state.history.append(("bot", response))

# Show chat history
for role, msg in st.session_state.history:
    if role == "user":
        st.chat_message("user").markdown(msg)
    else:
        st.chat_message("assistant").markdown(msg)

