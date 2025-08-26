# 🤖 TalentScout Hiring Assistant

An intelligent AI-powered chatbot for initial candidate screening in technology recruitment. Built with Streamlit and Groq's Llama 4 Scout model.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.29.0-red.svg)
![Groq](https://img.shields.io/badge/groq-llama--4--scout-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Overview

TalentScout is an AI hiring assistant designed to streamline the initial candidate screening process for technology positions. The chatbot systematically collects candidate information and generates relevant technical questions based on their declared tech stack.

### ✨ Key Features

- **🎯 Intelligent Conversation Flow**: Context-aware interactions with natural conversation handling
- **📝 Systematic Information Gathering**: Collects all essential candidate details
- **🔧 Dynamic Technical Questions**: Generates 3-5 tailored questions based on candidate's tech stack
- **⚡ Fast AI Responses**: Powered by Groq's Llama 4 Scout 17B model
- **🎨 Clean UI**: Intuitive Streamlit interface for seamless user experience
- **🔒 Data Privacy**: Secure handling of candidate information with GDPR compliance
- **📊 Progress Tracking**: Visual progress indicator throughout the screening process
- **💾 Data Export**: Export conversation data as JSON

## 🛠️ Tech Stack

- **AI Model**: Groq API with Llama 4 Scout 17B (`meta-llama/llama-4-scout-17b-16e-instruct`)
- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Data Handling**: JSON, Pandas
- **Environment Management**: python-dotenv

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/talentscout-hiring-assistant.git
   cd talentscout-hiring-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your Groq API key
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`

### Alternative: Quick Run Script

```bash
python run.py
```

## 📖 Usage Guide

### Information Collection Process

The chatbot systematically collects the following information:

1. **👤 Personal Information**
   - Full Name
   - Email Address
   - Phone Number (exactly 10 digits)

2. **💼 Professional Details**
   - Years of Experience
   - Desired Position
   - Current Location

3. **🔧 Technical Skills**
   - Programming Languages
   - Frameworks
   - Databases
   - Tools and Technologies

4. **❓ Technical Assessment**
   - 3-5 questions generated based on tech stack
   - Mix of conceptual and practical questions
   - Appropriate difficulty for screening

### Sample Conversation Flow

```
Assistant: 👋 Hello! Welcome to TalentScout's Hiring Assistant!
User: Hi, I'm ready to start
Assistant: Great! Let's begin. Could you please provide your full name?
User: John Smith
Assistant: Thank you! What's your email address?
User: john.smith@email.com
Assistant: Perfect! Please share your phone number.
User: 5551234567
Assistant: How many years of professional experience do you have?
User: 3 years
Assistant: What position(s) are you interested in?
User: Full Stack Developer
Assistant: What's your current location?
User: San Francisco, CA
Assistant: Please list your tech stack...
User: Python, React, PostgreSQL, Docker, AWS
Assistant: Based on your tech stack, here are some technical questions...
```

## 🏗️ Project Structure

```
talentscout-hiring-assistant/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── run.py                     # Application runner script
├── test_setup.py              # Setup verification script
├── data/                      # Data storage directory
│   └── .gitkeep              # Keep directory in git
└── src/                       # Source code modules
    ├── __init__.py           # Package initialization
    ├── groq_client.py        # Groq API integration
    ├── conversation_manager.py # Conversation flow management
    └── utils.py              # Utility functions
```

## 🧪 Testing

Run the setup verification:

```bash
python test_setup.py
```

This will test:
- ✅ File structure
- ✅ Python imports
- ✅ Environment configuration
- ✅ Conversation manager functionality
- ✅ Groq API connection

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Model Configuration

The application uses the Llama 4 Scout model by default. You can modify the model in `config.py`:

```python
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
```

## 📊 Features in Detail

### Input Validation

- **Email**: Regex pattern validation
- **Phone**: Exactly 10 digits required
- **Experience**: Numeric validation (0-50 years)
- **Tech Stack**: Parsing and categorization

### Conversation Management

- **State Tracking**: Maintains conversation stage and context
- **Error Handling**: Graceful handling of unexpected inputs
- **Context Awareness**: Remembers previous interactions
- **Exit Handling**: Responds to keywords like "bye", "exit", "quit"

### Technical Question Generation

- **Dynamic Generation**: Questions based on specific tech stack
- **Variety**: Mix of conceptual and practical questions
- **Relevance**: Job-appropriate difficulty level
- **Format**: Numbered list for easy reading

## 🚀 Deployment

### Local Deployment

```bash
streamlit run app.py
```

### Cloud Deployment Options

- **Streamlit Cloud**: Direct GitHub integration
- **Heroku**: Using Procfile
- **AWS EC2**: Docker containers
- **Google Cloud Run**: Serverless deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `python test_setup.py`
6. Commit your changes: `git commit -am 'Add new feature'`
7. Push to the branch: `git push origin feature-name`
8. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints for all functions
- Include docstrings for classes and methods
- Write tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for providing fast LLM inference
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Meta](https://ai.meta.com/) for the Llama models

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/talentscout-hiring-assistant/issues) page
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

## 🔄 Changelog

### v1.0.0 (Current)
- Initial release
- Complete hiring assistant functionality
- Groq API integration with Llama 4 Scout
- Streamlit UI with progress tracking
- Data export functionality
- Comprehensive input validation

---

**Built with ❤️ for better hiring experiences**

⭐ **Star this repo if you find it helpful!**