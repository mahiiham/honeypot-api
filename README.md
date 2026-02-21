# Honeypot API

## Description
This project implements an AI-powered conversational honeypot system designed to engage potential scammers, extract actionable intelligence, and generate structured fraud analysis reports.

The system simulates a realistic victim persona to prolong scam interactions while collecting key indicators such as phone numbers, UPI IDs, bank accounts, phishing links, and other suspicious identifiers.

The API is optimized for:
- Fast response time (< 30 seconds)
- Structured output compliance
- Multi-turn engagement tracking
- Intelligent scam detection
- Stable production deployment

---

## Tech Stack

- **Language/Framework:** Python 3.11, FastAPI
- **Key Libraries:** 
  - fastapi
  - uvicorn
  - openai (>=1.0.0)
  - python-dotenv
  - requests
- **LLM/AI Models Used:** GPT-4o-mini (OpenAI)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/honeypot-api.git
cd honeypot-api
2. Install dependencies

Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate   # Windows

Install required packages:

pip install -r requirements.txt
3. Set environment variables

Create a .env file in the root directory:

OPENAI_API_KEY=your_openai_api_key
API_KEY=your_secret_api_key
CALLBACK_URL=

OPENAI_API_KEY → Required for LLM-based engagement

API_KEY → Used for header authentication

CALLBACK_URL → Optional (for sending final structured output)

4. Run the application
uvicorn src.main:app --reload

Access Swagger UI:

http://127.0.0.1:8000/docs
API Endpoint

URL: https://your-deployed-url.com/honeypot

Method: POST
Authentication: x-api-key header

Sample Request
{
  "sessionId": "test1",
  "message": {
    "sender": "scammer",
    "text": "Call me at 9876543210 and transfer to fraud@upi",
    "timestamp": "2026-02-21T10:00:00Z"
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "sms",
    "language": "en",
    "locale": "IN"
  }
}
Final Output Endpoint

POST /final?sessionId=test1

Returns structured scam analysis including:

scamDetected

scamType

totalMessagesExchanged

engagementDurationSeconds

extractedIntelligence

agentNotes

confidenceLevel

Approach
1️⃣ Scam Detection Strategy

Scam detection is based on multi-signal analysis:

Red-flag keyword scoring (urgent, OTP, verify, refund, lottery, etc.)

Financial indicators (UPI IDs, bank accounts)

Phishing links

Combined behavioral signals

If suspicious financial entities or red-flag keywords are detected, the system flags the interaction as a scam with calculated confidence levels (Low / Medium / High).

2️⃣ Intelligence Extraction

The system extracts structured intelligence using optimized regex patterns:

Indian phone numbers (validated format)

Email addresses

Phishing URLs

UPI IDs

Bank accounts (11–18 digit format)

Case IDs

Policy numbers

Order numbers

Extracted entities are:

Deduplicated

Stored per session

Returned in structured JSON format

3️⃣ Engagement Strategy

The honeypot uses GPT-4o-mini to:

Maintain realistic victim behavior

Ask investigative follow-up questions

Encourage scammers to reveal more details

Sustain multi-turn conversations

Increase intelligence extraction depth

The model is configured for:

Controlled token usage

Stable response time

Non-blocking execution

Graceful fallback if LLM fails

This implementation ensures:

Fast responses

Structured intelligence reporting

Multi-turn engagement tracking

High detection accuracy

Production stability

Optional callback integration

Designed for hackathon-grade evaluation and real-world extensibility.
