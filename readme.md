# 🐍 AI Voice Assistant - Backend


[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)](https://www.mongodb.com/atlas)
[![LiveKit](https://img.shields.io/badge/LiveKit-WebRTC-orange.svg)](https://livekit.io/)
[![Google AI](https://img.shields.io/badge/Google-Gemini%20Live-red.svg)](https://ai.google.dev/)

> Robust **Python backend** for the AI Voice Assistant featuring real-time voice processing, agricultural expertise, disease detection, and expert consultation services.

## 🌟 Backend Overview

This backend provides the core intelligence and services for the AI Voice Assistant application. It combines Google Gemini Live for voice processing, FastAPI for web services, and MongoDB for data persistence to create a comprehensive agricultural assistance platform.

### 🏗️ **Architecture Components**
- **Voice Agent**: LiveKit + Google Gemini Live integration for real-time conversations
- **Web API**: FastAPI server with disease detection and query management
- **Database**: MongoDB Atlas with optimized indexing and validation
- **AI Services**: Google Gemini Live for natural language processing
- **Data Processing**: CSV data analysis and government API integration

## ✨ Key Features

### 🎙️ **Voice Processing**
- **Real-time Conversations**: Seamless voice chat with low latency
- **Google Gemini Live**: Native voice-to-voice AI processing - This was a concious choice to not go for STT-LLM-TTS.
- **All languages Support**: Multilingual conversation capabilities
- **Function Tools**: Voice-activated query creation and status checking , Market price checkups , 

### 🌾 **Agricultural Services**
- **Expert Query System**: Structured consultation request management
- **Crop Price API**: Real-time market data from Government of India
- **Query Tracking**: Unique 6-character tracking codes

### 🔬 **Disease Detection**
- **Image Analysis**: Plant disease identification from uploaded images
- **ML Processing**: Advanced machine learning for disease recognition
- **Treatment Recommendations**: Expert advice for disease management
- **Result Storage**: Persistent analysis history

### 📊 **Data Management**
- **MongoDB Atlas**: Cloud-native document database
- **Smart Indexing**: Optimized queries for fast retrieval
- **Data Validation**: Comprehensive input sanitization

## 📁 Backend Structure

```
backend/
├── agent.py              # LiveKit voice agent with Gemini Live
├── api.py               # AI assistant class with function tools
├── server.py            # FastAPI web server & disease detection - In progress
├── db_driver.py         # MongoDB operations and query management
├── requirements.txt     # Python dependencies
└── README.md           # This documentation
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** (tested with Python 3.12)
- **MongoDB Atlas account** ([free tier](https://www.mongodb.com/atlas))
- **LiveKit Cloud account** ([get started free](https://cloud.livekit.io/))
- **Google AI API key** ([get API key](https://ai.google.dev/))

### 1. Environment Setup
```bash
cd backend

# Create virtual environment
python -m venv ai

# Activate virtual environment
# Windows:
ai\Scripts\activate
# Linux/Mac:
source ai/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
Create `.env` file in the `backend/` directory:

```bash
# MongoDB Atlas (REQUIRED)
MONGODB_CONNECTION_STRING=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority

# LiveKit (REQUIRED)
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Google AI (REQUIRED)
GOOGLE_API_KEY=your-google-ai-api-key

# Government API (OPTIONAL - for crop prices)
GOV_API_KEY=your-government-api-key
GOV_API_URL=https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070

# FastAPI Configuration (OPTIONAL)
API_HOST=0.0.0.0
API_PORT=8000
```

### 3. Run Services

**Option 1: FastAPI Web Server (for disease detection & REST APIs)**
```bash
python server.py
# Starts on http://localhost:8000
# API docs at http://localhost:8000/docs
```

**Option 2: Voice Agent (for LiveKit voice interactions)**
```bash
python agent.py
# Connects to LiveKit and waits for voice sessions
```

**Option 3: Run Both (recommended)**
```bash
# Terminal 1 - Web server
python server.py

# Terminal 2 - Voice agent
python agent.py
```

## 🔧 Core Components

### 1. Voice Agent (`agent.py`)

**Primary Function**: LiveKit integration with Google Gemini Live

**Key Features**:
- Real-time voice communication via LiveKit
- Google Gemini Live integration for natural conversations
- Automatic participant handling and session management

**Usage**:
```python
# Starts LiveKit voice agent
python agent.py

# Connects to room: "voice-assistant"
# Waits for participants to join from frontend
```

### 2. AI Assistant (`api.py`)

**Primary Function**: Core AI logic and function tools

**Function Tools Available**:

#### 🎯 `create_query(name, mobile, location, description)`
Creates expert consultation requests with validation:
- **Indian mobile validation**: 10+ digits, starts with 6/7/8/9
- **Location requirement**: Complete address (village, district, state)
- **Unique tracking codes**: 6-character hexadecimal identifiers
- **UTC timestamps**: Global time compatibility

**Example Usage**:
```python
# Voice command: "I need help from an expert"
# AI guides through: Name → Mobile → Location → Problem
# Returns: "Query created! Tracking code: AB123C"
```

#### 📊 `check_status(request_code)`
Retrieves query status and expert assignment:
- **Code lookup**: Find query by tracking code
- **Status tracking**: pending → assigned → completed
- **Expert details**: Assigned expert information
- **Creation date**: Query submission timestamp

**Example Usage**:
```python
# Voice command: "Check status AB123C"
# Returns: Query details, status, expert assignment
```

#### 💰 `check_crop_prices(commodity, state, market)`
Government API integration for market prices:
- **20+ crops supported**: wheat, rice, onion, tomato, etc.
- **State-wise pricing**: Market-specific rates
- **Real-time data**: Government of India official APIs
- **Error handling**: Graceful fallback for API issues

**Example Usage**:
```python
# Voice command: "What is tomato price in Maharashtra?"
# Returns: Market rates from multiple locations
```

### 3. Web Server (`server.py`) - In progress

**Primary Function**: FastAPI REST API and disease detection

### 4. Database Manager (`db_driver.py`)

**Primary Function**: MongoDB operations and data management

**Key Features**:
- **Connection management**: Efficient Atlas connectivity
- **Query operations**: CRUD for expert consultation requests
- **Indexing**: Optimized for fast retrieval
- **Validation**: Input sanitization and mobile number validation
- **Error handling**: Graceful MongoDB error recovery

**Database Schema**:
```python
# Query document structure
{
    "_id": ObjectId("..."),
    "request_code": "AB123C",        # Unique 6-char hex
    "name": "राज कुमार",
    "mobile": "9876543210",          # Validated Indian mobile
    "location": "कानपुर, उत्तर प्रदेश",
    "description": "गेहूं की फसल में बीमारी है",
    "status": "pending",             # pending|assigned|completed
    "created_at": datetime,          # UTC timestamp
    "expert_assigned": None,         # Expert details when assigned
    "notes": None                    # Expert notes and updates
}
```

## 🔬 Disease Detection System - Part of Frontend (Direct API/Model calling)

### Image Processing Pipeline

1. **Upload Handling**: Secure file upload with validation
2. **Image Preprocessing**: Resize, format conversion, quality checks
3. **ML Analysis**: Plant disease identification using trained models
4. **Result Processing**: Confidence scoring and treatment recommendations
5. **Data Storage**: Analysis results saved to MongoDB

### Supported Diseases
- **Wheat**: Rust, blight, powdery mildew
- **Rice**: Blast, brown spot, bacterial leaf streak
- **Tomato**: Early blight, late blight, septoria leaf spot
- **Cotton**: Bollworm, aphids, whitefly
- **And more...** (expandable ML model system)

### Usage Example
```bash
# Upload plant image for analysis
curl -X POST http://localhost:8000/api/disease/analyze \
  -F "image=@plant_disease.jpg"

# Response includes disease identification and treatment
```

## 🎙️ Voice Command Examples

### Expert Query Creation (Hindi)
```
👤 User: "मुझे एक विशेषज्ञ से बात करनी है"
🤖 Assistant: "अपना नाम बताएं"

👤 User: "मेरा नाम राज कुमार है"
🤖 Assistant: "अपना मोबाइल नंबर बताएं - अंक एक-एक करके"

👤 User: "9 8 7 6 5 4 3 2 1 0"
🤖 Assistant: "अपना पूरा पता बताएं"

👤 User: "कानपुर, उत्तर प्रदेश"
🤖 Assistant: "क्या समस्या है?"

👤 User: "गेहूं की फसल में बीमारी है"
🤖 Assistant: "आपका अनुरोध बन गया! ट्रैकिंग कोड: AB123C"
```

### Status Checking (English)
```
👤 User: "Check status AB123C"
🤖 Assistant: "Request Code: AB123C
            Name: राज कुमार
            Status: Expert assigned - Dr. Sharma
            Problem: गेहूं की फसल में बीमारी है
            Created: 2025-01-22 14:30:00"
```

### Crop Price Inquiry
```
👤 User: "What is tomato price in Maharashtra?"
🤖 Assistant: "Tomato Prices in Maharashtra:
            Found 3 market records:
            1. Mumbai Market: ₹25 per kg
            2. Pune Market: ₹23 per kg
            3. Nashik Market: ₹22 per kg
            Data updated: Today"
```

### Government API Integration

**Supported APIs**:
- **Price Data**: Real-time market prices
- **Weather**: Agricultural weather information
- **Crop Reports**: Government agricultural reports
- **Subsidies**: Farmer subsidy information

## 🧪 Testing & Development

### Database Testing
```bash
# Test MongoDB connection
python -c "
from db_driver import db_manager
if db_manager:
    print('✅ Database: Connected')
    
    # Test query creation
    code = db_manager.create_query(
        'Test User', 
        '9876543210', 
        'Test Location', 
        'Test problem'
    )
    print(f'✅ Query Creation: {code}')
    
    # Test status retrieval
    status = db_manager.get_query_status(code)
    print(f'✅ Status Retrieval: {status}')
else:
    print('❌ Database: Connection failed')
"
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `MONGODB_CONNECTION_STRING` | ✅ | MongoDB Atlas connection | `mongodb+srv://user:pass@cluster.net/` |
| `LIVEKIT_URL` | ✅ | LiveKit server WebSocket URL | `wss://project.livekit.cloud` |
| `LIVEKIT_API_KEY` | ✅ | LiveKit API key | `your-api-key` |
| `LIVEKIT_API_SECRET` | ✅ | LiveKit API secret | `your-api-secret` |
| `GOOGLE_API_KEY` | ✅ | Google AI API key | `your-google-ai-key` |
| `GOV_API_KEY` | ❌ | Government API key | `your-gov-api-key` |
| `GOV_API_URL` | ❌ | Government API endpoint | `https://api.data.gov.in/...` |
| `API_HOST` | ❌ | FastAPI host (default: 0.0.0.0) | `localhost` |
| `API_PORT` | ❌ | FastAPI port (default: 8000) | `8080` |

### Dependencies

**Core Dependencies** (`requirements.txt`):
```
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
livekit>=0.10.0
livekit-agents>=0.7.0
google-generativeai>=0.3.0
pymongo>=4.6.0
python-multipart>=0.0.6
python-dotenv>=1.0.0
pillow>=10.1.0
requests>=2.31.0
pandas>=2.1.0
numpy>=1.24.0
```

### Performance Optimization

**MongoDB Indexing**:
```javascript
// Automatically created indexes
db.queries.createIndex({ "request_code": 1 }, { unique: true })
db.queries.createIndex({ "mobile": 1 })
db.queries.createIndex({ "created_at": -1 })
db.queries.createIndex({ "status": 1 })
```

**Memory Management**:
- Connection pooling for MongoDB
- Async processing for FastAPI
- Efficient image handling for disease detection
- Lazy loading for large datasets

### Environment Setup
```bash
# Production environment variables
export MONGODB_CONNECTION_STRING="your-production-atlas-connection"
export LIVEKIT_URL="your-production-livekit-url"
export GOOGLE_API_KEY="your-production-api-key"

# Start services
python server.py &
python agent.py &
```

### Scaling Considerations
- **MongoDB Atlas**: Auto-scales with M10+ clusters
- **LiveKit**: Supports concurrent voice sessions
- **FastAPI**: Async processing for high throughput


## 📚 API Documentation

### FastAPI Interactive Docs

When running the server, comprehensive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Voice Command Reference

**Expert Query Commands**:
- "I need help from an expert"
- "मुझे एक विशेषज्ञ से बात करनी है"
- "Create a new query"
- "Expert consultation"

**Status Check Commands**:
- "Check status [CODE]"
- "What is the status of [CODE]"
- "Query status [CODE]"

**Price Check Commands**:
- "What is [crop] price in [state]?"
- "[crop] की कीमत क्या है [state] में?"
- "Check market price of [crop]"


## 🔗 Related Documentation

- **[Main Project README](../README.md)**: Full-stack project overview
- **[Frontend README](../frontend/README.md)**: React frontend documentation
- **[FastAPI Documentation](https://fastapi.tiangolo.com/)**: Web framework docs
- **[LiveKit Python SDK](https://docs.livekit.io/guides/)**: Voice infrastructure docs
- **[MongoDB Python Driver](https://pymongo.readthedocs.io/)**: Database operations

---

<div align="center">

**🐍 Intelligent Backend for Voice AI**  
*Robust Python services powering agricultural voice assistance*

[![FastAPI](https://img.shields.io/badge/Powered%20by-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB%20Atlas-green.svg)](https://www.mongodb.com/atlas)

*Built with ❤️ for scalable agricultural solutions*

</div> 
