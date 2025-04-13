## **Project Overview:**
### 🧠 TalentScout AI — Smart Hiring Assistant

An AI-powered technical interviewer chatbot built using:
- 🤖 **Hugging Face (Mistral-7B-Instruct-v0.3")** via Inference API  
- 💾 **MongoDB Atlas** (with encryption) for secure candidate data storage  
- 🌐 **Streamlit** for a clean, interactive frontend  
- 🛡️ **GDPR-compliant data handling**

## ✨ Features

- Collects essential candidate details:
  - Name, Contact, Years of Experience, Tech Stack
- Generates tailored technical questions using **Mistral-7B-Instruct-v0.3**
- Stores encrypted data securely in **MongoDB**
- User-friendly **Streamlit UI**
- Follows **best practices for privacy and security**
  
## **Installation Instructions:**

1. Clone the repository:

```
git clone https://github.com/InduM/TalentScout`
cd TalentScout
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up environment variables:\
Create a .env file in the project root and initialize the API Keys.

5. Run the application:
```
streamlit run app.py
```

## 🔧 Tech Stack

| Component      | Technology                       |
|----------------|----------------------------------|
| AI Model       | `Mistral-7B-Instruct-v0.3`       |
| Inference      | Hugging Face Inference API       |
| Frontend       | Streamlit                        |
| Database       | MongoDB (local or Atlas)         |
| Security       | Fernet encryption for PII        |

## 🔐 Security & GDPR
- All Personally Identifiable Information (PII) like names and contacts are encrypted at rest using cryptography.Fernet.
- Data is not shared with 3rd parties beyond model inference (via Hugging Face API).
- Optionally support anonymization and delete-on-request via admin panel or CLI tool (coming soon).

## Deployment
The app has been deployed using [streamlit](https://indum-talentscout-app-hgahsd.streamlit.app/)
