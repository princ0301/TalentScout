from typing import Dict, List, Any
import json
from datetime import datetime
from src.groq_client import GroqClient

class ConversationManager:
    """Manages the conversation flow and candidate data collection"""
    
    def __init__(self):
        self.groq_client = GroqClient()
        self.reset_conversation()
        
        self.required_fields = [
            "full_name", "email", "phone", "experience_years", 
            "desired_position", "location", "tech_stack"
        ]
        
        self.field_prompts = {
            "full_name": "Could you please provide your full name?",
            "email": "What's your email address?",
            "phone": "Please share your phone number.",
            "experience_years": "How many years of professional experience do you have?",
            "desired_position": "What position(s) are you interested in?",
            "location": "What's your current location?",
            "tech_stack": "Please list your tech stack - programming languages, frameworks, databases, and tools you're proficient in."
        }

    def reset_conversation(self):
        """Reset conversation state"""
        self.conversation_history = []
        self.candidate_data = {}
        self.current_field_index = 0
        self.conversation_stage = "greeting"
        self.technical_questions_generated = False

    def get_greeting_message(self) -> str:
        """Get initial greeting message"""
        return """👋 Hello! Welcome to TalentScout's Hiring Assistant!

I'm here to help with your initial screening for technology positions. I'll be collecting some basic information about you and then asking a few technical questions based on your expertise.

This should take about 5-10 minutes. Ready to get started?

(You can type 'exit', 'quit', or 'bye' at any time to end our conversation)"""

    def process_message(self, user_message: str) -> str:
        """Process user message and return appropriate response"""
        if self.groq_client.check_conversation_end(user_message):
            return self.end_conversation()

        self.conversation_history.append({"role": "user", "content": user_message})

        if self.conversation_stage == "greeting":
            response = self.handle_greeting_response(user_message)
        elif self.conversation_stage == "collecting_info":
            response = self.handle_info_collection(user_message)
        elif self.conversation_stage == "technical_questions":
            response = self.handle_technical_questions(user_message)
        else:
            response = "I'm not sure how to help with that. Could you please clarify?"

        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def handle_greeting_response(self, user_message: str) -> str:
        """Handle response after greeting"""
        positive_responses = ["yes", "yeah", "sure", "ok", "okay", "ready", "let's start", "start"]
        
        if any(word in user_message.lower() for word in positive_responses):
            self.conversation_stage = "collecting_info"
            return f"Great! Let's begin. {self.field_prompts[self.required_fields[0]]}"
        else:
            return self.groq_client.get_response(user_message, self.conversation_history)

    def handle_info_collection(self, user_message: str) -> str:
        """Handle information collection phase"""
        current_field = self.required_fields[self.current_field_index]
        
        if self.validate_and_store_field(current_field, user_message):
            self.current_field_index += 1
            
            if self.current_field_index >= len(self.required_fields):
                self.conversation_stage = "technical_questions"
                return self.generate_technical_questions()
            else:
                next_field = self.required_fields[self.current_field_index]
                return f"Thank you! {self.field_prompts[next_field]}"
        else:
            return self.get_field_clarification(current_field, user_message)

    def validate_and_store_field(self, field: str, value: str) -> bool:
        """Validate and store field value"""
        value = value.strip()
        
        if field == "email":
            if self.groq_client.validate_email(value):
                self.candidate_data[field] = value
                return True
            return False
        elif field == "phone":
            if self.groq_client.validate_phone(value):
                self.candidate_data[field] = value
                return True
            return False
        elif field == "experience_years":
            try:
                years = float(value.split()[0])
                if 0 <= years <= 50:
                    self.candidate_data[field] = years
                    return True
            except:
                pass
            return False
        elif field == "tech_stack":
            tech_list = [tech.strip() for tech in value.replace(',', ' ').split() if tech.strip()]
            if len(tech_list) > 0:
                self.candidate_data[field] = tech_list
                return True
            return False
        else:
            if len(value) > 1:
                self.candidate_data[field] = value
                return True
            return False

    def get_field_clarification(self, field: str, user_input: str) -> str:
        """Get clarification for invalid field input"""
        clarifications = {
            "email": "Please provide a valid email address (e.g., john@example.com).",
            "phone": "Please provide a valid 10-digit phone number.",
            "experience_years": "Please provide your years of experience as a number (e.g., 3, 5.5).",
            "tech_stack": "Please list the technologies you know (e.g., Python, React, MySQL).",
            "full_name": "Please provide your full name.",
            "desired_position": "Please specify the position you're interested in.",
            "location": "Please provide your current location."
        }
        
        return clarifications.get(field, "Could you please provide that information again?")

    def generate_technical_questions(self) -> str:
        """Generate technical questions based on tech stack"""
        if not self.technical_questions_generated:
            tech_stack = self.candidate_data.get("tech_stack", [])
            questions = self.groq_client.generate_technical_questions(tech_stack)
            
            response = f"""Perfect! I have all your information. Based on your tech stack ({', '.join(tech_stack)}), here are some technical questions for you:

{questions}

Please feel free to answer these questions. You can answer them one by one or all together, whichever you prefer.

When you're done, just let me know and I'll wrap up our conversation."""
            
            self.technical_questions_generated = True
            return response.strip()
        else:
            return "Thank you for your responses! Is there anything else you'd like to add or clarify about your technical experience?"

    def handle_technical_questions(self, user_message: str) -> str:
        """Handle technical questions phase"""
        if "technical_responses" not in self.candidate_data:
            self.candidate_data["technical_responses"] = []
        
        self.candidate_data["technical_responses"].append({
            "timestamp": datetime.now().isoformat(),
            "response": user_message
        })
        
        return self.groq_client.get_response(
            f"The candidate provided this technical response: {user_message}. Please provide brief, encouraging feedback and ask if they have anything else to add.",
            self.conversation_history
        )

    def end_conversation(self) -> str:
        """End the conversation gracefully"""
        self.conversation_stage = "ending"
        
        return """Thank you for taking the time to speak with me today! 

Here's what happens next:
✅ Your information has been recorded securely
✅ Our recruitment team will review your responses
✅ We'll contact you within 2-3 business days with next steps

If you have any questions in the meantime, feel free to reach out to our team directly.

Have a great day! 👋"""

    def get_candidate_summary(self) -> Dict[str, Any]:
        """Get summary of collected candidate data"""
        return {
            "candidate_data": self.candidate_data,
            "conversation_completed": self.conversation_stage == "ending",
            "timestamp": datetime.now().isoformat()
        }

    def export_conversation(self) -> str:
        """Export conversation history as JSON string"""
        export_data = {
            "candidate_data": self.candidate_data,
            "conversation_history": self.conversation_history,
            "conversation_stage": self.conversation_stage,
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(export_data, indent=2)