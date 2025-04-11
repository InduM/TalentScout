import streamlit as st
import random
from questions import tech_questions
from scripts import *
from db_scripts import *
#from transformers import  BlenderbotTokenizer, BlenderbotForConditionalGeneration,BlenderbotSmallForConditionalGeneration
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


# Load model & tokenizer once
@st.cache_resource
def load_model():
    #model_name =  "facebook/blenderbot-3B"
   # model_name = "facebook/blenderbot_small-90M"
    #tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
    #model = BlenderbotSmallForConditionalGeneration.from_pretrained(model_name)
    model_name  = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

# Session state initialization
if "state" not in st.session_state:
    st.session_state.state = "initial_info"
    st.session_state.user_data = {}
    st.session_state.history = []
    st.session_state.questions = []
    st.session_state.question_number = 0
    st.session_state.answers = []
    st.session_state.awaiting_tech_answers = False
    st.session_state.consent_given = False


exit_keywords = ['bye', 'exit', 'quit', 'stop']
accept_keywords = ['yes', 'agree', 'ok', 'okay', 'yup', 'yep', 'sure', 'definitely', 'absolutely','yeah']
delete_keywords = ['delete', 'delete data',"delete my data"]

# UI
st.title("TalentScout Hiring Chatbot")
# User input box
user_input = st.chat_input(placeholder="Say something...")

def generate_bot_reply(user_input):
    instruction = "Instruction: respond like a helpful AI recruiter."
    context = " ".join([x[1] for x in st.session_state.history[-5:] if x[0] == "user"])
    full_prompt = f"{instruction} Context: {context} User: {user_input}"

    inputs = tokenizer([full_prompt], return_tensors="pt")
    reply_ids = model.generate(**inputs, max_length=128)
    reply = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
    return reply


def generate_tech_questions(techs):
    questions = []
    for tech in techs:
        tech_key = tech.strip().lower()
        if tech_key in tech_questions:
            samples = random.sample(tech_questions[tech_key], k= random.randint(1,3))
            questions.extend(samples)
            if len(questions) >= 5:
                break
    # Fill up to 5 if fewer collected
    if len(questions) < 5:
        all_questions = []
        for tech in techs:
            tech_key = tech.strip().lower()
            if tech_key in tech_questions:
                all_questions.extend(tech_questions[tech_key])
        remaining = list(set(all_questions) - set(questions))
        if remaining:
            questions += random.sample(remaining, min(5 - len(questions), len(remaining)))
    return questions[:5]
    

def get_answer(question):
    st.session_state.history.append(("bot", question))
    answer = user_input
    st.session_state.history.append(("user", answer))

def store_data():
    db = load_db()
    db[st.session_state.candidate_id] = st.session_state.user_data
    db[st.session_state.candidate_id]['questions'] = st.session_state.questions
    db[st.session_state.candidate_id]['answers'] = st.session_state.answers
    save_db(db)

def delete_data():
    db = load_db()
    if st.session_state.candidate_id in db:
        del db[st.session_state.candidate_id]
        save_db(db)
        return "🧹 Your data has been permanently deleted."
    else:
        return "❌ Candidate ID not found."

def handle_input(user_input):
    if any(word in user_input.lower() for word in exit_keywords):
        st.session_state.state = 'end'
        if st.session_state.consent_given:
            store_data()
            return "Thank you for your time.We’ve recorded your responses and our team will be in touch soon. Goodbye!"
        else:
            return "The interview has been terminated. Thank you for your time."
    
    if any(word in user_input.lower() for word in delete_keywords):
        st.session_state.state = 'delete'
        return delete_data()

    match st.session_state.state:
        case "initial_info":
            st.session_state.state = "greeting"
            return " Hi! I’m TechScreenBot, here to help with your application. Before we begin, please note that your responses will be recorded for recruitment purposes. Your data will not be shared with third parties, and you can request deletion at any time. Do you agree to proceed?"
        case "greeting":
            if any(word in user_input.lower() for word in accept_keywords):
                st.session_state.consent_given = True
                st.session_state.state = "info_name"
                st.session_state.candidate_id = str(uuid.uuid4())
                return "Then let's begin. What's your full name?"
            else:
                st.session_state.consent_given = False
                st.session_state.state = "end"
                return "Consent is required to proceed with the interview."

        case "info_name":
            if validate_name(user_input):
                st.session_state.user_data['name'] = encrypt(user_input)
                st.session_state.state = "info_email" 
                return "Thanks! May I have your email address?"
            else:
                return "Please enter a valid name."

        case "info_email":
            if validate_email(user_input):
                st.session_state.user_data['email'] = encrypt(user_input)
                st.session_state.state = "info_phone"
                return "Got it. Your phone number?"
            else:
                return "Please enter a valid email address."

        case "info_phone":
            if validate_phone(user_input):  
                st.session_state.user_data['phone'] = encrypt(user_input)
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
            questions = generate_tech_questions(techs)
            st.session_state.questions.extend(questions)
            st.session_state.state = "awaiting_answers"
            st.session_state.awaiting_tech_answers = True
            store_data()
            return f"Your profile has been saved with the id {st.session_state.candidate_id}. Please answer the following questions:\n" +st.session_state.questions[st.session_state.question_number]
             
        case "awaiting_answers":
            st.session_state.answers.append(user_input)
            st.session_state.question_number += 1
            if st.session_state.question_number < len(st.session_state.questions):
                return st.session_state.questions[st.session_state.question_number]
            st.session_state.state = "chatting"
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

