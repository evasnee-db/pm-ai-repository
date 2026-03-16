# Excuse Email Draft Tool

A web application that generates creative excuse emails using Databricks Model Serving LLM. Built with FastAPI backend and React frontend, designed for seamless deployment on Databricks Apps.

![Excuse Email Tool Screenshot](https://img.shields.io/badge/status-production%20ready-green)

## Features

- **AI-Powered Email Generation**: Uses Databricks Model Serving LLM to create contextual excuse emails
- **Multiple Categories**: Running Late, Missed Meeting, Deadline, WFH/OOO, Social, Travel
- **Tone Control**: Sincere, Playful, or Corporate tones
- **Seriousness Levels**: 5-point scale from very silly to serious
- **Modern UI**: Clean, responsive React interface with Tailwind CSS
- **Copy to Clipboard**: One-click email copying functionality
- **Real-time Validation**: Form validation and error handling
- **Health Monitoring**: Multiple health check endpoints
- **Debug Support**: Environment debugging capabilities

## Project Structure

```
excuse-gen-app/
├── app.yaml                    # Databricks Apps configuration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── src/
│   └── app.py                 # FastAPI backend application
└── public/
    └── index.html             # React frontend (single-file)
```

## Quick Start

### Local Development

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd excuse-gen-app
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Databricks credentials
   ```

4. **Run the Application**
   ```bash
   python -m uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Access the Application**
   Open http://localhost:8000 in your browser

### Environment Variables

Create a `.env` file with the following variables:

```env
DATABRICKS_API_TOKEN=your_databricks_personal_access_token
DATABRICKS_ENDPOINT_URL=https://your-workspace.cloud.databricks.com/serving-endpoints/your-endpoint/invocations
```

## Databricks Apps Deployment

### Prerequisites

- Databricks workspace with Apps enabled
- Databricks Model Serving endpoint configured
- Databricks CLI installed and configured

### Deployment Steps

1. **Configure App Secret**
   ```bash
   databricks secrets create-scope --scope excuse-email-app
   databricks secrets put --scope excuse-email-app --key databricks_token
   ```

2. **Deploy Application**
   ```bash
   databricks apps deploy excuse-gen-app --source-code-path /path/to/excuse-gen-app
   ```

3. **Access Your App**
   Your app will be available at the URL provided by Databricks Apps

### App Configuration

The `app.yaml` file configures the deployment:

- **Port**: 8000 (required for Databricks Apps)
- **Host**: 0.0.0.0 (container compatibility)
- **Secrets**: Uses `valueFrom: databricks_token` for secure API token storage
- **Environment**: Pre-configured endpoint URL and runtime settings

## API Endpoints

### Main Endpoints

- `POST /api/generate-excuse` - Generate excuse email
- `GET /` - Serve React frontend

### Health & Monitoring

- `GET /health` - Health check with timestamp
- `GET /healthz` - Simple health status
- `GET /ready` - Readiness probe
- `GET /ping` - Basic connectivity test
- `GET /metrics` - Prometheus-style metrics
- `GET /debug` - Environment debugging

### API Request Format

```json
{
  "category": "Running Late",
  "tone": "Playful", 
  "seriousness": 3,
  "recipient_name": "Alex",
  "sender_name": "Mona",
  "eta_when": "15 minutes"
}
```

### API Response Format

```json
{
  "subject": "Running Late - ETA 15 minutes",
  "body": "Dear Alex,\n\nI wanted to let you know...",
  "success": true,
  "error": null
}
```

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server for FastAPI
- **httpx**: Async HTTP client for LLM calls
- **Pydantic**: Data validation and settings
- **python-dotenv**: Environment variable management

### Frontend
- **React 18**: Modern UI library (CDN-based, no build process)
- **Tailwind CSS**: Utility-first CSS framework
- **Babel Standalone**: JSX transformation in browser

### Deployment
- **Databricks Apps**: Container-based app platform
- **Docker**: Containerization (handled by Databricks Apps)

## Features Deep Dive

### LLM Integration

The application integrates with Databricks Model Serving endpoints:

- **Flexible Response Parsing**: Handles multiple LLM response formats
- **Fallback Responses**: Graceful degradation when LLM is unavailable
- **Context-Aware Prompting**: Dynamic prompts based on user inputs
- **Error Handling**: Comprehensive error handling and logging

### UI/UX Design

- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Loading States**: Visual feedback during API calls
- **Form Validation**: Real-time input validation
- **Error Messages**: User-friendly error displays
- **Copy Functionality**: Native clipboard API integration

### Security & Performance

- **Environment Variables**: Secure credential management
- **CORS Support**: Proper cross-origin configuration
- **Request Logging**: Comprehensive logging for debugging
- **Health Checks**: Multiple monitoring endpoints
- **Error Boundaries**: Graceful error handling throughout

## Customization

### Adding New Categories

1. Update the `categories` list in `public/index.html`
2. Add corresponding fallback responses in `src/app.py`
3. Update validation in the `ExcuseRequest` model

### Modifying Tones

1. Update the `tones` list in the frontend
2. Adjust prompt engineering in `LLMClient._build_prompt()`
3. Update validation accordingly

### Styling Changes

The frontend uses Tailwind CSS classes. Modify the HTML classes in `public/index.html` to customize the appearance.

## Troubleshooting

### Common Issues

1. **Port 8000 Required**: Databricks Apps specifically requires port 8000
2. **CORS Errors**: Ensure CORS middleware is properly configured
3. **LLM Timeout**: Increase timeout values for slow model responses
4. **File Paths**: Check `get_frontend_file_path()` for correct static file resolution

### Debugging

- Use `/debug` endpoint to check environment variables
- Check application logs for detailed error messages
- Verify Databricks Model Serving endpoint accessibility
- Ensure API token has proper permissions

### Performance Optimization

- **Caching**: Consider adding response caching for repeated requests
- **Connection Pooling**: httpx client uses connection pooling by default
- **Error Retry**: Implement retry logic for transient LLM errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review application logs
3. Use the `/debug` endpoint for environment diagnostics
4. Open an issue on the repository

---

**Built with ❤️ for Databricks Apps Platform**





