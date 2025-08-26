import streamlit as st
import os
from datetime import datetime
from src.conversation_manager import ConversationManager

st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        text-align: right;
    }
    
    .assistant-message {
        background-color: #e9ecef;
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'conversation_manager' not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False

def display_header():
    """Display the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 TalentScout Hiring Assistant</h1>
        <p>AI-powered initial candidate screening for technology positions</p>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display sidebar with information and controls"""
    with st.sidebar:
        st.header("📋 About This Assistant")
        
        st.markdown("""
        **What I do:**
        - Collect your basic information
        - Understand your tech stack
        - Generate relevant technical questions
        - Provide a smooth screening experience
        
        **Information I'll collect:**
        - Full Name
        - Email & Phone (10 digits)
        - Years of Experience
        - Desired Position
        - Current Location
        - Technical Skills
        """)
        
        st.markdown("---")
        st.subheader("🎛️ Controls")
        
        if st.button("🔄 Reset Conversation", use_container_width=True):
            st.session_state.conversation_manager.reset_conversation()
            st.session_state.messages = []
            st.session_state.conversation_started = False
            st.rerun()
        
        if st.session_state.conversation_started:
            st.markdown("---")
            st.subheader("📊 Progress")
            
            stage = st.session_state.conversation_manager.conversation_stage
            progress_map = {
                "greeting": 0.2,
                "collecting_info": 0.6,
                "technical_questions": 0.9,
                "ending": 1.0
            }
            
            progress = progress_map.get(stage, 0)
            st.progress(progress)
            st.write(f"Stage: {stage.replace('_', ' ').title()}")

def display_chat_interface():
    """Display the main chat interface"""
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <strong>Assistant:</strong> {message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    if not st.session_state.conversation_started:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Conversation", use_container_width=True, type="primary"):
                greeting = st.session_state.conversation_manager.get_greeting_message()
                st.session_state.messages.append(
                    {"role": "assistant", "content": greeting})
                st.session_state.conversation_started = True
                st.rerun()

def display_chat_input():
    """Display chat input separately to avoid container conflicts"""
    if st.session_state.conversation_started:
        user_input = st.chat_input("Type your message here...")

        if user_input:
            st.session_state.messages.append(
                {"role": "user", "content": user_input})

            try:
                response = st.session_state.conversation_manager.process_message(
                    user_input)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response})
            except Exception as e:
                error_message = f"I apologize, but I encountered an error. Please try again. Error: {str(e)}"
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_message})

            st.rerun()

def display_candidate_summary():
    """Display candidate information summary"""
    if st.session_state.conversation_started:
        candidate_data = st.session_state.conversation_manager.candidate_data

        if candidate_data:
            st.markdown("---")
            st.subheader("📝 Candidate Information Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if "full_name" in candidate_data:
                    st.write(f"**Name:** {candidate_data['full_name']}")
                if "email" in candidate_data:
                    st.write(f"**Email:** {candidate_data['email']}")
                if "phone" in candidate_data:
                    st.write(f"**Phone:** {candidate_data['phone']}")
                if "experience_years" in candidate_data:
                    st.write(f"**Experience:** {candidate_data['experience_years']} years")
            
            with col2:
                if "desired_position" in candidate_data:
                    st.write(f"**Position:** {candidate_data['desired_position']}")
                if "location" in candidate_data:
                    st.write(f"**Location:** {candidate_data['location']}")
                if "tech_stack" in candidate_data:
                    st.write(f"**Tech Stack:** {', '.join(candidate_data['tech_stack'])}")
            
            if st.button("📥 Export Conversation", use_container_width=True):
                conversation_export = st.session_state.conversation_manager.export_conversation()
                st.download_button(
                    label="💾 Download Conversation Data",
                    data=conversation_export,
                    file_name=f"candidate_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

def main():
    """Main application function"""
    initialize_session_state()
    display_header()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        display_chat_interface()
        display_candidate_summary()
    
    with col2:
        display_sidebar()
    
    display_chat_input()
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>TalentScout Hiring Assistant v1.0 | Powered by Groq & Streamlit</p>
        <p>🔒 Your data is handled securely and in compliance with privacy standards</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()