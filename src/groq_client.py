import os
from typing import Dict, List
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    """Client for interacting with Groq API for hiring assistant functionality"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"
        
        self.system_prompt = """You are TalentScout's AI Hiring Assistant for technology position screening. 
        Collect: Full Name, Email, Phone, Years of Experience, Desired Position, Location, Tech Stack.
        Then generate 3-5 relevant technical questions. Be professional, ask one question at a time, 
        validate information, and end conversation on keywords like "bye", "exit", "quit", "end"."""

    def get_response(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """Get response from Groq API"""
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            if conversation_history:
                messages.extend(conversation_history)
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                top_p=1,
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please try again. Error: {str(e)}"

    def generate_technical_questions(self, tech_stack: List[str]) -> str:
        """Generate technical questions based on candidate's tech stack"""
        tech_stack_str = ", ".join(tech_stack)
        prompt = f"""Based on the following tech stack: {tech_stack_str}
        Generate 3-5 relevant technical questions to assess the candidate's proficiency. 
        Requirements: practical, job-relevant, mix of conceptual and practical, appropriate difficulty level, numbered list."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert technical interviewer creating screening questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Unable to generate technical questions at the moment. Error: {str(e)}"

    def check_conversation_end(self, message: str) -> bool:
        """Check if user wants to end the conversation"""
        end_keywords = ["bye", "goodbye", "exit", "quit", "end", "stop", "finish", "done"]
        return any(keyword in message.lower() for keyword in end_keywords)

    def validate_email(self, email: str) -> bool:
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone: str) -> bool:
        """Phone number validation - exactly 10 digits"""
        import re
        digits_only = re.sub(r'\D', '', phone)
        return len(digits_only) == 10