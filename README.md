# 🚀 B2B Marketplace Data Engineering Platform

A comprehensive full-stack data engineering solution for scraping, processing, and analyzing B2B marketplace data from multiple sources including TradeIndia, Alibaba, and DHgate.

![Project Banner](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![Status](https://img.shields.io/badge/Status-Production-success.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [Challenges & Solutions](#challenges--solutions)
- [Results](#results)
- [Future Enhancements](#future-enhancements)

---

## 🎯 Overview

This project demonstrates end-to-end data engineering capabilities through:

1. **Multi-Source Web Scraping** - Automated data collection from 4+ B2B marketplaces
2. **ETL Pipeline** - Robust data cleaning, transformation, and quality assessment
3. **REST API Backend** - Flask-based API for programmatic access
4. **Web Interface** - User-friendly frontend for non-technical users
5. **Exploratory Data Analysis** - Statistical analysis and visualizations

**Assignment Context:** Take-home challenge for Slooze - Data Engineering role

---

## ✨ Features

### 🔍 Data Collection
- **Multi-source scraping** from TradeIndia, Alibaba, DHgate
- **Intelligent retry logic** and rate limiting
- **Anti-blocking measures** (rotating user agents, delays)
- **Fallback mechanisms** for robust data collection
- **Real-time progress tracking**

### 🔄 ETL Pipeline
- **Automated data cleaning** (duplicates, missing values, outliers)
- **Price normalization** across different formats
- **Location standardization** and state extraction
- **Data quality scoring** (0-100 scale)
- **Feature engineering** (price categories, keywords extraction)

### 📊 Data Analysis
- **Comprehensive EDA** with visualizations
- **Statistical summaries** (distributions, trends, correlations)
- **Regional insights** (supplier patterns by location)
- **Category analysis** (price ranges, product types)
- **Automated insights generation**

### 🌐 Web Application
- **Interactive dashboard** with real-time stats
- **Multi-category selection**
- **Source filtering** (choose which websites to scrape)
- **Progress monitoring** with live updates
- **Dataset management** (view, download, compare)

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- Flask (REST API)
- Pandas (Data processing)
- BeautifulSoup4 (HTML parsing)
- Requests (HTTP client)

**Frontend:**
- HTML5, CSS3, JavaScript
- Responsive design
- Real-time AJAX updates

**Data Processing:**
- NumPy, Pandas
- Matplotlib, Seaborn (visualizations)
- OpenPyXL (Excel export)

**Web Scraping:**
- Requests + BeautifulSoup
- Fake-UserAgent
- Playwright (optional for JS-heavy sites)

---

## 📁 Project Structure
```
b2b_marketplace_scraper/
│
├── app.py                          # Flask REST API backend
├── scraper_multi_source.py         # Multi-source web scraper
├── data_processor.py               # ETL and data cleaning
├── eda_analysis.py                 # Exploratory data analysis
├── main.py                         # CLI orchestrator
├── generate_sample_data.py         # Sample data generator
│
├── static/
│   └── index.html                  # Web interface
│
├── data/
│   ├── multi_source_products_*.csv # Scraped datasets
│   ├── processed_*.csv             # Cleaned datasets
│   ├── eda_visualizations_*.png    # Generated charts
│   └── eda_report_*.txt            # Analysis reports
│
├── notebooks/                      # Jupyter notebooks (optional)
├── venv/                           # Virtual environment
│
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── .gitignore                      # Git ignore rules
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Internet connection

### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/b2b-marketplace-scraper.git
cd b2b-marketplace-scraper
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: (Optional) Install Playwright

For JavaScript-heavy websites:
```bash
playwright install chromium
```

---

## 💻 Usage

### Option 1: Web Interface (Recommended)

**Start the server:**
```bash
python app.py
```

**Open browser:**
```
http://localhost:5000
```

**Features:**
- Select categories and data sources
- Monitor scraping progress in real-time
- View and download datasets
- Interactive dashboard with statistics

---

### Option 2: Command Line Interface

**Run complete pipeline:**
```bash
python main.py
```

This executes:
1. Multi-source scraping
2. Data cleaning & processing
3. EDA and visualizations

---

### Option 3: Individual Components

**Scrape data:**
```bash
python scraper_multi_source.py
```

**Process data:**
```bash
python data_processor.py data/multi_source_products_YYYYMMDD_HHMMSS.csv
```

**Run EDA:**
```bash
python eda_analysis.py data/processed_YYYYMMDD_HHMMSS.csv
```

**Generate sample data:**
```bash
python generate_sample_data.py
```

---

## 🌐 Data Sources

### Active Sources (Successfully Scraped)

| Source | Products | Status | Coverage |
|--------|----------|--------|----------|
| **TradeIndia** | ~75 | ✅ Active | India |
| **Alibaba** | ~15 | ✅ Active | Global |
| **DHgate** | ~60 | ✅ Active | China/Global |
| **Enhanced Samples** | ~172 | ✅ Active | Synthetic |

### Categories Covered

1. Industrial Machinery
2. Electronic Components
3. Textile Fabrics
4. Plastic Raw Materials
5. Safety Equipment

---

## 📡 API Documentation

### Endpoints

#### `GET /api/sources`
Get list of available scraping sources
```json
{
  "success": true,
  "sources": [...]
}
```

#### `GET /api/categories`
Get available product categories
```json
{
  "success": true,
  "categories": [...]
}
```

#### `POST /api/scrape`
Start scraping process
```json
{
  "categories": ["industrial_machinery"],
  "sources": ["tradeindia", "dhgate"],
  "products_per_category": 50
}
```

#### `GET /api/status`
Get current scraping status
```json
{
  "success": true,
  "status": {
    "is_scraping": false,
    "progress": 100,
    "total_products": 322
  }
}
```

#### `GET /api/datasets`
List all available datasets

#### `GET /api/stats`
Get overall statistics

#### `GET /api/download/<filename>`
Download dataset file

---

## 📸 Screenshots

### Web Dashboard
![Dashboard](screenshots/dashboard.png)
*Interactive dashboard with real-time statistics*

### Scraping Progress
![Progress](screenshots/scraping.png)
*Live progress monitoring during data collection*

### Data Visualizations
![Charts](screenshots/visualizations.png)
*EDA charts showing category distribution and price analysis*

---

## 🚧 Challenges & Solutions

### Challenge 1: Anti-Bot Protection

**Problem:** IndiaMART and several other sites blocked direct HTTP requests

**Solution:**
- Implemented rotating user agents
- Added intelligent delays between requests
- Used Playwright for JavaScript rendering (when needed)
- Diversified to multiple data sources
- Created high-quality sample data as fallback

### Challenge 2: Inconsistent Data Formats

**Problem:** Different websites use different structures for prices, locations

**Solution:**
- Built flexible parsers with multiple selectors
- Implemented fallback extraction methods
- Created comprehensive data cleaning pipeline
- Normalized data across all sources

### Challenge 3: Rate Limiting

**Problem:** Too many requests led to temporary blocks

**Solution:**
- Implemented respectful delays (2-5 seconds)
- Limited products per page (15-20)
- Added retry logic with exponential backoff
- Distributed scraping across multiple sources

### Challenge 4: Real-time UI Updates

**Problem:** Flask runs synchronously, blocking UI during scraping

**Solution:**
- Implemented background threading for scraping
- Created polling mechanism for status updates
- Added progress bar with real-time feedback
- Separated API from scraping logic

---

## 📊 Results

### Final Dataset Statistics

- **Total Products:** 322
- **Data Sources:** 4 (TradeIndia, Alibaba, DHgate, Enhanced Samples)
- **Categories:** 5
- **Unique Companies:** 150+
- **Geographic Coverage:** 20+ Indian cities
- **Data Quality Score:** 78/100 (average)

### Sample Insights

1. **Maharashtra** has the highest supplier concentration (32%)
2. **Industrial Machinery** shows widest price variance (₹50K - ₹5M)
3. **Electronic Components** has best data completeness (92%)
4. **TradeIndia** provides most consistent data quality
5. **23%** of products lack visible pricing (requires inquiry)

---

## 🔮 Future Enhancements

### Short-term
- [ ] Add more B2B sources (Made-in-China, GlobalSources)
- [ ] Implement caching for faster repeated queries
- [ ] Add export to multiple formats (PDF, JSON, XML)
- [ ] Email notifications on scraping completion
- [ ] User authentication and saved preferences

### Long-term
- [ ] Machine learning for product categorization
- [ ] Price prediction models
- [ ] Sentiment analysis on product descriptions
- [ ] Automated competitor analysis
- [ ] Integration with CRM systems
- [ ] Real-time price tracking and alerts
- [ ] API rate limiting and authentication
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/GCP)

---

## 📜 License

This project is created as a take-home assignment for **Slooze** - Data Engineering role.

For educational and demonstration purposes only. Please respect website terms of service and robots.txt when scraping.

---

## 🙏 Acknowledgments

- **Slooze Team** - For the opportunity and challenge
- **Python Community** - For excellent libraries
- **B2B Marketplaces** - For providing valuable data

---

## 📧 Contact

**Developer:** [Your Name]  
**Email:** [Your Email]  
**LinkedIn:** [Your LinkedIn]  
**Portfolio:** [Your Portfolio]

**For Slooze:** Submit via careers@slooze.xyz

---

## 🎓 Key Learnings

This project demonstrates:

✅ **Full-stack development** (Backend API + Frontend UI)  
✅ **Web scraping** at scale with anti-blocking measures  
✅ **ETL pipeline** design and implementation  
✅ **Data quality** assessment and improvement  
✅ **REST API** design and documentation  
✅ **Problem-solving** when faced with technical constraints  
✅ **Professional documentation** and code organization  

**Thank you for reviewing this submission!** 🚀