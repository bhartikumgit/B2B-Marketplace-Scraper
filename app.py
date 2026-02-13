"""
Flask Backend API for B2B Marketplace Scraper
Provides REST API endpoints for scraping and data analysis
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import pandas as pd
from datetime import datetime
import threading

# Import scrapers
from scraper_multi_source import MultiSourceScraper

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for frontend

# Configuration
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

# Global scraping status
scraping_status = {
    'is_scraping': False,
    'progress': 0,
    'current_category': '',
    'total_products': 0,
    'message': 'Ready'
}

@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('static', 'index.html')

@app.route('/api/sources', methods=['GET'])
def get_sources():
    """Get list of available scraping sources"""
    sources = [
        {
            'id': 'tradeindia',
            'name': 'TradeIndia',
            'status': 'active',
            'description': 'Indian B2B marketplace - Reliable'
        },
        {
            'id': 'alibaba',
            'name': 'Alibaba',
            'status': 'active',
            'description': 'Global B2B platform - Partial access'
        },
        {
            'id': 'dhgate',
            'name': 'DHgate',
            'status': 'active',
            'description': 'Wholesale marketplace - Good access'
        },
        {
            'id': 'sample',
            'name': 'Enhanced Sample Data',
            'status': 'active',
            'description': 'High-quality generated data'
        }
    ]
   
    
    return jsonify({
        'success': True,
        'sources': sources
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get available product categories"""
    categories = [
        {'id': 'industrial_machinery', 'name': 'Industrial Machinery'},
        {'id': 'electronic_components', 'name': 'Electronic Components'},
        {'id': 'textile_fabrics', 'name': 'Textile Fabrics'},
        {'id': 'plastic_raw_materials', 'name': 'Plastic Raw Materials'},
        {'id': 'safety_equipment', 'name': 'Safety Equipment'}
    ]
    
    return jsonify({
        'success': True,
        'categories': categories
    })

@app.route('/api/scrape', methods=['POST'])
def start_scraping():
    """Start scraping process"""
    global scraping_status
    
    if scraping_status['is_scraping']:
        return jsonify({
            'success': False,
            'message': 'Scraping already in progress'
        }), 400
    
    data = request.get_json()
    categories = data.get('categories', [])
    sources = data.get('sources', ['tradeindia'])
    products_per_category = data.get('products_per_category', 50)
    
    if not categories:
        return jsonify({
            'success': False,
            'message': 'Please select at least one category'
        }), 400
    
    # Start scraping in background thread
    thread = threading.Thread(
        target=run_scraping,
        args=(categories, sources, products_per_category)
    )
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Scraping started',
        'categories': categories
    })

def run_scraping(categories, sources, products_per_category):
    """Background scraping task"""
    global scraping_status
    
    scraping_status['is_scraping'] = True
    scraping_status['progress'] = 0
    scraping_status['total_products'] = 0
    
    try:
        scraper = MultiSourceScraper()
        
        for i, category in enumerate(categories):
            scraping_status['current_category'] = category.replace('_', ' ').title()
            scraping_status['progress'] = int((i / len(categories)) * 100)
            scraping_status['message'] = f'Scraping {scraping_status["current_category"]}...'
            
            # Scrape category
            category_name = category.replace('_', ' ')
            # Scrape from selected real sources
            real_sources = [s for s in sources if s != 'sample']
            if real_sources:
                scraper.scrape_category(category_name, sources=real_sources, max_per_source=15)
            
            # Add sample data if selected
            if 'sample' in sources:
                scraper.add_sample_products(category_name, count=35)
            
            
            
            scraping_status['total_products'] = len(scraper.products)
        
        # Save data
        csv_file, json_file = scraper.save_data()
        
        scraping_status['progress'] = 100
        scraping_status['message'] = f'Completed! {len(scraper.products)} products scraped'
        scraping_status['csv_file'] = csv_file
        scraping_status['json_file'] = json_file
        
    except Exception as e:
        scraping_status['message'] = f'Error: {str(e)}'
    
    finally:
        scraping_status['is_scraping'] = False

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current scraping status"""
    return jsonify({
        'success': True,
        'status': scraping_status
    })

@app.route('/api/datasets', methods=['GET'])
def get_datasets():
    """Get list of available datasets"""
    datasets = []
    
    try:
        files = os.listdir(DATA_DIR)
        csv_files = [f for f in files if f.endswith('.csv')]
        
        for filename in sorted(csv_files, reverse=True)[:10]:  # Last 10 files
            filepath = os.path.join(DATA_DIR, filename)
            
            # Get file info
            file_size = os.path.getsize(filepath)
            file_time = os.path.getmtime(filepath)
            
            # Try to get row count
            try:
                df = pd.read_csv(filepath)
                row_count = len(df)
                categories = df['category'].nunique() if 'category' in df.columns else 0
            except:
                row_count = 0
                categories = 0
            
            datasets.append({
                'filename': filename,
                'size': file_size,
                'created': datetime.fromtimestamp(file_time).isoformat(),
                'rows': row_count,
                'categories': categories
            })
    
    except Exception as e:
        pass
    
    return jsonify({
        'success': True,
        'datasets': datasets
    })

@app.route('/api/data/<filename>', methods=['GET'])
def get_data(filename):
    """Get data from a specific file"""
    try:
        filepath = os.path.join(DATA_DIR, filename)
        
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'message': 'File not found'
            }), 404
        
        df = pd.read_csv(filepath)
        
        # Get summary statistics
        summary = {
            'total_products': len(df),
            'categories': df['category'].nunique() if 'category' in df.columns else 0,
            'sources': df['source'].nunique() if 'source' in df.columns else 0,
            'with_prices': df['price_numeric'].notna().sum() if 'price_numeric' in df.columns else 0
        }
        
        # Get sample data
        sample = df.head(20).to_dict('records')
        
        # Category breakdown
        category_counts = df['category'].value_counts().to_dict() if 'category' in df.columns else {}
        
        return jsonify({
            'success': True,
            'summary': summary,
            'sample': sample,
            'category_counts': category_counts
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download a data file"""
    try:
        return send_from_directory(DATA_DIR, filename, as_attachment=True)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        # Find all CSV files
        files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
        
        if not files:
            # Return default stats if no files
            return jsonify({
                'success': True,
                'stats': {
                    'total_datasets': 0,
                    'total_products': 0,
                    'categories': 0,
                    'sources': 0,
                    'latest_scrape': None,
                    'with_prices': 0
                }
            })
        
        # Sort by modification time (newest first)
        files_with_time = []
        for f in files:
            filepath = os.path.join(DATA_DIR, f)
            mtime = os.path.getmtime(filepath)
            files_with_time.append((f, mtime))
        
        files_with_time.sort(key=lambda x: x[1], reverse=True)
        latest_file = files_with_time[0][0]
        
        # Read the latest file
        df = pd.read_csv(os.path.join(DATA_DIR, latest_file))
        
        stats = {
            'total_datasets': len(files),
            'total_products': int(len(df)),
            'categories': int(df['category'].nunique()) if 'category' in df.columns else 0,
            'sources': int(df['source'].nunique()) if 'source' in df.columns else 0,
            'latest_scrape': latest_file,
            'with_prices': int(df['price_numeric'].notna().sum()) if 'price_numeric' in df.columns else 0
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        # Return error with default stats
        print(f"[ERROR] Stats error: {str(e)}")
        return jsonify({
            'success': True,
            'stats': {
                'total_datasets': 0,
                'total_products': 0,
                'categories': 0,
                'sources': 0,
                'latest_scrape': None,
                'with_prices': 0
            }
        })
if __name__ == '__main__':
    print("\n" + "="*60)
    print("B2B MARKETPLACE SCRAPER - BACKEND API")
    print("="*60)
    print("Starting Flask server...")
    print("API will be available at: http://localhost:5000")
    print("Frontend will be available at: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)