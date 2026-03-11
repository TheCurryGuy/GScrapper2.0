# Academic Publication API

A comprehensive API for retrieving academic publications from multiple sources including CrossRef, OpenAlex, and Google Scholar. Features a beautiful web interface with advanced search capabilities and CSV export functionality.

## 🌟 Features

- **Dual Search Modes**:
  - **Normal Search**: Search by author name and email (uses CrossRef + OpenAlex)
  - **Advanced Search**: Search by Google Scholar Author ID (uses RapidAPI)

- **Rich Author Metadata**: Display h-index, i10-index, affiliation, and research interests
- **Interactive Web Interface**: Beautiful gradient design with real-time metrics
- **CSV Export**: Download publications with customizable year filters
- **Automatic Deduplication**: Smart merging of results from multiple sources
- **Dual API Key Fallback**: Automatic switching between primary and backup RapidAPI keys

## 📋 Prerequisites

- Python 3.12 or higher
- RapidAPI account with Google Scholar API subscription (optional for advanced search)

## 🚀 Quick Start

### 1. Extract the Project

Extract the `academic-publication-api` folder to your desired location.

### 2. Set Up Python Virtual Environment

Open PowerShell/Terminal in the project directory and run:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt):
.\venv\Scripts\activate.bat

# On Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

The `.env` file is already included in the project with pre-configured API keys. **No additional setup needed!**

If you need to modify the configuration, edit the `.env` file:

```env
# Application
APP_NAME=Academic Publication API
VERSION=1.0.0
DEBUG=False
HOST=0.0.0.0
PORT=8000

# API Keys (already configured)
RAPIDAPI_KEY=your_primary_key_here
RAPIDAPI_KEY_BACKUP=your_backup_key_here

# Email (optional)
USER_EMAIL=your_email@example.com
```

### 5. Run the Application

```powershell
python run.py
```

The API will start on `http://localhost:8000`

## 🎯 Using the Application

### Web Interface

1. Open your browser and navigate to: `http://localhost:8000`

2. **Normal Search** (Tab 1):
   - Enter author's full name
   - Enter author's email address
   - Click "Search Publications"
   - View results from CrossRef and OpenAlex
   - Download CSV with DOI column included

3. **Advanced Search** (Tab 2):
   - Enter Google Scholar Author ID (e.g., `VUlo65MAAAAJ`)
   - Click "Search by Author ID"
   - View author metadata (h-index, i10-index, affiliation, interests)
   - Download CSV (without DOI column as Google Scholar doesn't provide it)

### Finding Google Scholar Author ID

1. Go to [Google Scholar](https://scholar.google.com/)
2. Search for the author
3. Click on their profile
4. The Author ID is in the URL: `https://scholar.google.com/citations?user=AUTHOR_ID`
5. Example: For URL `https://scholar.google.com/citations?user=VUlo65MAAAAJ`, the ID is `VUlo65MAAAAJ`

### API Endpoints

#### 1. Normal Search (POST)

**Endpoint**: `POST /api/v1/publications/search`

**Request Body**:
```json
{
  "author_name": "Subhalaxmi Chakraborty",
  "email": "subhalaxmi@example.com"
}
```

**Response**: Returns publications from CrossRef and OpenAlex with DOI information

#### 2. Advanced Search (GET)

**Endpoint**: `GET /api/v1/publications/search/advanced?author_id=VUlo65MAAAAJ`

**Response**: Returns publications from Google Scholar with author metadata

#### 3. Health Check

**Endpoint**: `GET /api/v1/health`

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-10-28T10:00:00",
  "services": {
    "crossref": "available",
    "openalex": "available",
    "google_scholar": "available"
  }
}
```

## 📊 Features Breakdown

### Year Filtering
- Filter publications by year directly in the web interface
- Shows publication count for each year
- "All Years" option to view complete results

### CSV Export
- **Normal Search CSV**: Includes Title, Year, Authors, Venue, Citations, DOI, URL, Source
- **Advanced Search CSV**: Includes Title, Year, Authors, Venue, Citations, URL, Source (no DOI)
- Downloads filtered results based on selected year
- Filename includes date and year filter for easy organization

### Metrics Display
- Total Publications
- Total Citations
- Average Citations per Paper
- H-Index (Advanced Search only)
- i10-Index (Advanced Search only)

### Author Metadata (Advanced Search)
- Author Name
- Institutional Affiliation
- Research Interests (as tags)
- Citation Metrics

## 🏗️ Project Structure

```
academic-publication-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── publications.py    # Publication search endpoints
│   │       │   └── health.py          # Health check endpoint
│   │       └── router.py              # API router configuration
│   ├── core/
│   │   ├── config.py                  # Configuration settings
│   │   └── logging.py                 # Logging setup
│   ├── models/
│   │   ├── request.py                 # Request models
│   │   └── response.py                # Response models
│   ├── services/
│   │   ├── aggregator.py              # Aggregates all academic sources
│   │   ├── crossref.py                # CrossRef API integration
│   │   ├── openalex.py                # OpenAlex API integration
│   │   ├── google_scholar.py          # Google Scholar (RapidAPI) integration
│   │   └── base.py                    # Base service class
│   ├── utils/
│   │   ├── deduplication.py           # Publication deduplication logic
│   │   └── helpers.py                 # Helper functions
│   └── main.py                        # FastAPI application
├── static/
│   └── index.html                     # Web interface
├── logs/                              # Application logs
├── .env                               # Environment variables (included)
├── requirements.txt                   # Python dependencies
├── run.py                             # Application runner
└── README.md                          # This file
```

## 🔑 API Rate Limits

- **CrossRef**: No authentication required, rate limit ~50 requests/second
- **OpenAlex**: No authentication required, polite pool with User-Agent header
- **Google Scholar (RapidAPI)**: 
  - Primary Key: 100 requests/month
  - Backup Key 1: 100 requests/month
  - Backup Key 2: 100 requests/month
  - Total: 300 requests/month with automatic fallback across all keys

## 🐛 Troubleshooting

### Virtual Environment Issues

**Problem**: `Activate.ps1` cannot be run
```powershell
# Solution: Run PowerShell as Administrator and execute:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port Already in Use

**Problem**: Port 8000 is already occupied
```powershell
# Solution: Edit .env file and change PORT value:
PORT=8080
```

### Module Import Errors

**Problem**: `ModuleNotFoundError`
```powershell
# Solution: Ensure virtual environment is activated and reinstall:
pip install -r requirements.txt --force-reinstall
```

### RapidAPI Rate Limit

**Problem**: "Rate limit exceeded" errors
- The application automatically switches to backup API key
- If both keys are exhausted, wait for the monthly reset
- Consider upgrading your RapidAPI subscription for higher limits

### No Results Found

**Problem**: Search returns no publications
- **Normal Search**: Verify the author name spelling and email accuracy
- **Advanced Search**: Confirm the Google Scholar Author ID is correct
- Check if the author has publications in the respective databases

## 📝 Development

### Running in Debug Mode

Edit `.env` and set:
```env
DEBUG=True
```

This enables detailed logging and error messages.

### Viewing Logs

Logs are stored in the `logs/` directory:
- `logs/app.log` - Application logs
- Console output for real-time monitoring

## 🌐 Data Sources

1. **CrossRef**: Comprehensive database of scholarly publications with DOI information
2. **OpenAlex**: Open-access catalog of scholarly papers, authors, and institutions
3. **Google Scholar**: Extensive academic search engine via RapidAPI

## 📄 License

This project is provided as-is for academic and research purposes.

## 👨‍💻 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review application logs in the `logs/` directory
3. Ensure all environment variables are correctly configured

## 🎉 Acknowledgments

- CrossRef API for open publication data
- OpenAlex for comprehensive academic metadata
- RapidAPI for Google Scholar integration
- FastAPI framework for robust API development

---

**Version**: 1.0.0  
**Last Updated**: October 28, 2025

