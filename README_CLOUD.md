# 🏨 Cullinan Hotel Chatbot

AI-powered hotel assistant built with Streamlit and OpenAI.

## 🚀 Live Demo

This app is deployed on Streamlit Community Cloud:
[**🔗 Try the Live Demo**](https://your-app-name.streamlit.app)

## ✨ Features

- 🤖 AI-powered conversations
- 🏨 Hotel information queries
- 📅 Booking assistance
- 💬 Natural language processing
- 📊 Real-time statistics
- 🎨 Modern, responsive UI

## 🔧 Local Development

### Prerequisites

- Python 3.8+
- OpenAI API Key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/170421015_ahmed_said_kilic_chatbot_odevi.git
cd 170421015_ahmed_said_kilic_chatbot_odevi
```

2. Install dependencies:
```bash
pip install -r requirements_cloud.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

4. Run the app:
```bash
streamlit run app_streamlit_cloud.py
```

## 🌐 Streamlit Cloud Deployment

### Step 1: Push to GitHub

Make sure your repository is public and contains:
- `app_streamlit_cloud.py` (main app file)
- `requirements_cloud.txt` (dependencies)
- `README.md` (this file)

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `app_streamlit_cloud.py`
6. Click "Deploy"

### Step 3: Configure Secrets

In Streamlit Cloud dashboard, add your secrets:

```toml
[secrets]
OPENAI_API_KEY = "your-openai-api-key-here"
```

## 🎯 How to Use

1. **Start a Conversation**: Type your message in the input field
2. **Quick Questions**: Use predefined buttons for common queries
3. **Hotel Information**: Ask about facilities, pricing, and services
4. **Booking Assistance**: Get help with reservations
5. **Debug Mode**: Toggle debug information for troubleshooting

## 🏗️ Project Structure

```
📁 hotel_chatbot/
├── 📄 app_streamlit_cloud.py      # Main Streamlit app (Cloud-ready)
├── 📄 requirements_cloud.txt      # Dependencies for Streamlit Cloud
├── 📄 config_cloud.py            # Configuration (simplified)
├── 📄 README.md                  # This file
└── 📄 .gitignore                 # Git ignore rules
```

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | ✅ Yes |

## 🐛 Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**
   - Solution: Set the API key in Streamlit Cloud secrets

2. **"Module not found"**
   - Solution: Check `requirements_cloud.txt` for all dependencies

3. **"Repository access denied"**
   - Solution: Ensure repository is public and accessible

### Debug Mode

Enable debug mode in the app to see:
- Session state information
- API key status
- System diagnostics

## 📞 Support

If you encounter issues:
1. Check the debug information in the app
2. Verify your OpenAI API key
3. Ensure all dependencies are installed
4. Open an issue on GitHub

## 📄 License

This project is for educational purposes.

## 🎓 Academic Information

- **Student ID**: 170421015
- **Student Name**: Ahmed Said Kılıç
- **Project**: Hotel Chatbot Assignment
- **Technology Stack**: Streamlit, OpenAI GPT, Python

---

**🏨 Cullinan Hotel** - *Luxury Accommodation Experience*
