# Domain Config Backend

Enterprise-grade FastAPI backend for managing domain_config YAML files with MongoDB persistence, comprehensive validation, and LLM-powered intent interpretation.

## 🚀 Features

- **YAML Upload & Validation** - Upload and validate domain configuration YAML files
- **MongoDB Persistence** - Store and retrieve YAML configurations with metadata
- **Pydantic Validation** - Strict schema validation with detailed error feedback
- **LLM Intent Interpretation** - Convert natural language to structured intents using Groq/OpenAI/Anthropic
- **Domain Pack Listing** - Retrieve all uploaded configurations sorted by date
- **Comprehensive Logging** - Detailed logging for debugging and monitoring
- **Interactive API Docs** - Swagger UI at `/docs` for easy testing

## 📋 Prerequisites

- **Python 3.10+**
- **MongoDB 4.4+** (running locally or remote)
- **LLM API Key** (Groq/OpenAI/Anthropic) for intent interpretation

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
cp .env.example .env
```

Edit `.env` and configure:

```bash
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=domain_config_db
COLLECTION_NAME=yaml_configs

# LLM Configuration
LLM_PROVIDER=groq  # or openai, anthropic
GROQ_API_KEY=your_groq_api_key_here
LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.1
```

**Get API Keys:**
- **Groq**: https://console.groq.com/keys (Free tier available)
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/

### 5. Start MongoDB

Ensure MongoDB is running:

```bash
# Windows (if installed as service)
net start MongoDB

# Linux/Mac
sudo systemctl start mongod

# Or using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 6. Test Database Connection

```bash
python test_connection.py
```

Expected output:
```
✓ MongoDB connection test PASSED
✓ Database access successful: domain_config_db
✓ Collection access successful: yaml_configs
```

## 🎯 Running the Server

### Development Mode (with auto-reload)

```bash
python main.py
```

Or using uvicorn directly:

```bash
python -m uvicorn main:app --reload --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Server will start at: **http://localhost:8000**

## 📚 API Documentation

Once the server is running, access interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing

### Run All Tests

```bash
# Test all endpoints
python test_endpoints.py

# Test intent interpretation
python test_intent.py
```

### Test Individual Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Upload YAML:**
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@sample.yaml"
```

**List Domain Packs:**
```bash
curl http://localhost:8000/domain_pack_list
```

**Intent Interpretation:**
```bash
curl -X POST http://localhost:8000/intent \
  -H "Content-Type: application/json" \
  -d '{
    "domain_pack_id": "Legal_v01",
    "domain_name": "legal",
    "description": "Legal and compliance domain",
    "user_request": "Add new entity CLIENT with attributes client_id, name, type"
  }'
```

**Intent Health Check:**
```bash
curl http://localhost:8000/intent/health
```

## 📁 Project Structure

```
backend/
├── api/
│   └── routes/
│       ├── upload.py          # YAML upload endpoint
│       ├── validate.py        # YAML validation endpoint
│       ├── list.py            # Domain pack listing
│       └── intent.py          # Intent interpretation
├── core/
│   ├── config.py              # Configuration settings
│   └── logging_config.py      # Logging setup
├── db/
│   └── connection.py          # MongoDB connection
├── models/
│   └── document.py            # MongoDB document builder
├── schemas/
│   ├── domain_config.py       # Main YAML schema
│   ├── intention.py           # Intent schema
│   └── ...                    # Other Pydantic models
├── services/
│   ├── yaml_parser.py         # YAML parsing logic
│   ├── llm_service.py         # LLM integration
│   └── validation_service.py  # Validation logic
├── utils/
│   └── error_handlers.py      # Error handling
├── main.py                    # Application entry point
├── requirements.txt           # Dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

## 🔧 Configuration

### LLM Providers

**Groq (Recommended - Fast & Free Tier):**
```bash
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_...
LLM_MODEL=llama-3.3-70b-versatile
```

**OpenAI:**
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-3.5-turbo  # or gpt-4-turbo
```

**Anthropic:**
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
LLM_MODEL=claude-3-opus-20240229
```

### MongoDB Configuration

**Local MongoDB:**
```bash
MONGODB_URI=mongodb://localhost:27017
```

**MongoDB Atlas (Cloud):**
```bash
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

**Docker MongoDB:**
```bash
MONGODB_URI=mongodb://localhost:27017
```

## 🐛 Troubleshooting

### MongoDB Connection Failed

**Problem:** `Failed to connect to MongoDB`

**Solution:**
1. Check if MongoDB is running: `mongosh` or `mongo`
2. Verify MONGODB_URI in `.env`
3. Check firewall settings

### LLM API Errors

**Problem:** `LLM_API_ERROR` or `LLM_CONFIGURATION_ERROR`

**Solution:**
1. Check `/intent/health` endpoint
2. Verify API key in `.env`
3. Ensure correct model name for your provider
4. Check API key has sufficient credits

### Import Errors

**Problem:** `ModuleNotFoundError`

**Solution:**
```bash
pip install -r requirements.txt
```

### Port Already in Use

**Problem:** `Address already in use`

**Solution:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with API info |
| `/health` | GET | Health check with MongoDB status |
| `/upload` | POST | Upload and store YAML file |
| `/validate` | POST | Validate YAML without storing |
| `/domain_pack_list` | GET | List all uploaded domain packs |
| `/intent` | POST | Convert natural language to intent |
| `/intent/health` | GET | Check LLM service status |
| `/docs` | GET | Swagger UI documentation |

## 🔐 Security Notes

- **Never commit `.env`** - Contains sensitive API keys
- **Use environment variables** - Don't hardcode credentials
- **Rotate API keys** - Regularly update your LLM API keys
- **MongoDB authentication** - Enable auth in production
- **CORS configuration** - Restrict origins in production

## 📝 License

[Your License Here]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Built with FastAPI, MongoDB, and LLM Integration** 🚀
