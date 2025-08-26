import subprocess
import sys
import os
from dotenv import load_dotenv

def check_requirements():
    """Check if requirements are installed"""
    try:
        import streamlit
        import groq
        return True
    except ImportError:
        return False

def install_requirements():
    """Install requirements if missing"""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        return False

def main(): 
    print("🤖 TalentScout Hiring Assistant")
    print("=" * 40)
    
    load_dotenv()
    
    if not check_requirements():
        print("📦 Installing missing requirements...")
        if not install_requirements():
            print("❌ Failed to install requirements")
            print("Please run: pip install -r requirements.txt")
            return False
        print("✅ Requirements installed successfully")
    
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  GROQ_API_KEY not found in environment")
        print("You can add it in the Streamlit interface or create a .env file")
    
    print("🚀 Starting TalentScout Hiring Assistant...")
    print("The application will open in your browser")
    print("Press Ctrl+C to stop the application")
    print("-" * 40)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)