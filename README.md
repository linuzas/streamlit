# AI Interview Suite

A comprehensive interview preparation tool with expert chat, question generation, and image generation capabilities.

## Features

- Expert Chat with customizable expert types
- Question Generator based on job descriptions
- Interview Preparation with coding questions
- Image Generation using DALL-E 3
- User authentication and data persistence

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ai-interview-suite
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_api_key_here
```

5. Run the application:
```bash
streamlit run app.py
```

## Deployment Options

### 1. Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Add your environment variables in Streamlit Cloud settings
5. Deploy!

### 2. Heroku
1. Create a `Procfile`:
```
web: streamlit run app.py
```

2. Deploy using Heroku CLI:
```bash
heroku create your-app-name
git push heroku main
```

3. Set environment variables in Heroku dashboard

### 3. Docker
1. Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

2. Build and run:
```bash
docker build -t ai-interview-suite .
docker run -p 8501:8501 ai-interview-suite
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key with access to GPT-4 and DALL-E 3

## Data Storage

The application uses JSON files for data storage. For production, consider:
- Using a proper database (PostgreSQL, MongoDB)
- Implementing proper session management
- Adding data backup mechanisms

## Security Considerations

- Never commit `.env` file or sensitive data
- Use environment variables for API keys
- Implement proper user authentication
- Consider rate limiting for API calls
- Add input validation and sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 