import time
import os
from dotenv import load_dotenv
from openai import OpenAI
from src.intelligence_extractor import extract_entities

load_dotenv()

class HoneypotAgent:
    def __init__(self):
        self.sessions = {}

    def scam_score(self, text):
        red_flags = [
            "urgent", "otp", "verify", "click",
            "limited offer", "suspend", "blocked",
            "refund", "prize", "kyc", "lottery",
            "account compromised", "immediate action"
        ]
        return sum(1 for flag in red_flags if flag in text.lower())

    def _format_history(self, history):
        """Convert conversation history list to a readable string."""
        if not history:
            return "No previous messages."
        lines = []
        for msg in history:
            sender = msg.get("sender", "unknown")
            text = msg.get("text", "")
            lines.append(f"{sender.capitalize()}: {text}")
        return "\n".join(lines)

    def generate_reply(self, session_id, message, history):
        # Initialize session if new
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "start_time": time.time(),
                "message_count": 0,
                "red_flags": 0,
                "extracted": {
                    "phoneNumbers": [],
                    "emailAddresses": [],
                    "phishingLinks": [],
                    "upiIds": [],
                    "bankAccounts": [],
                    "caseIds": [],
                    "policyNumbers": [],
                    "orderNumbers": []
                }
            }

        session = self.sessions[session_id]
        session["message_count"] += 1
        session["red_flags"] += self.scam_score(message)

        
        extracted = extract_entities(message)
        for key, values in extracted.items():
            for value in values:
                if value not in session["extracted"][key]:
                    session["extracted"][key].append(value)

        
        formatted_history = self._format_history(history)
        prompt = f"""You are an intelligent scam honeypot.

Keep the scammer engaged. Ask investigative questions. Try to extract financial details (phone, email, bank account, UPI, website). Be curious but skeptical.

Conversation so far:
{formatted_history}

Latest scammer message:
{message}

Your reply:"""

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "Can you provide your official employee ID and callback number?"

        try:
            client = OpenAI(api_key=api_key, timeout=10.0)  
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=120,
                temperature=0.7
            )
            reply = response.choices[0].message.content.strip()
        except Exception:
            reply = "Can you provide your official employee ID and callback number?"

        return reply

    def get_final_output(self, session_id):
        session = self.sessions.get(session_id)
        if not session:
            return None

        extracted = session["extracted"]
        has_financial = bool(extracted["bankAccounts"] or extracted["upiIds"] or extracted["phishingLinks"])
        scam_detected = (session["red_flags"] > 0) or has_financial

        
        if has_financial and session["red_flags"] > 0:
            confidence = "High"
        elif has_financial:
            confidence = "High"
        elif session["red_flags"] > 0:
            confidence = "Medium"
        else:
            confidence = "Low"

        return {
            "sessionId": session_id,
            "scamDetected": scam_detected,
            "scamType": "financial_fraud" if has_financial else "generic",
            "totalMessagesExchanged": session["message_count"],
            "engagementDurationSeconds": int(time.time() - session["start_time"]),
            "extractedIntelligence": extracted,
            "agentNotes": f"Red flags: {session['red_flags']}. Financial indicators present: {has_financial}.",
            "confidenceLevel": confidence
        }