"""
Main Orchestrator - B2B Marketplace Data Engineering Pipeline
Runs the complete pipeline: Scraping → Processing → Analysis
"""

import os
import sys
import time
from datetime import datetime

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_step(step_num, total_steps, description):
    """Print step information"""
    print(f"\n{'>'*5} STEP {step_num}/{total_steps}: {description}")
    print("-"*70)

def run_scraper():
    """Run the web scraper"""
    print_step(1, 3, "WEB SCRAPING")
    
    print("Starting IndiaMART scraper...")
    print("This will scrape products from 5 categories (3 pages each)")
    print("Estimated time: 2-3 minutes\n")
    
    from scraper import IndiaMartScraper
    
    scraper = IndiaMartScraper()
    
    # Product categories
    categories = [
        "industrial machinery",
        "electronic components",
        "textile fabrics",
        "plastic raw materials",
        "safety equipment"
    ]
    
    print(f"Categories to scrape: {categories}\n")
    
    # Scrape each category
    for i, category in enumerate(categories, 1):
        print(f"\n[{i}/{len(categories)}] Scraping: {category}")
        scraper.search_products(category, max_pages=3)
        time.sleep(2)  # Brief delay between categories
    
    # Save data
    json_file, csv_file = scraper.save_data()
    
    print(f"\n✅ Scraping completed!")
    print(f"   Total products: {len(scraper.products)}")
    
    return csv_file

def run_data_processor(input_file):
    """Run the data processor"""
    print_step(2, 3, "DATA PROCESSING (ETL)")
    
    print(f"Processing file: {input_file}\n")
    
    from data_processor import DataProcessor
    
    processor = DataProcessor(input_file)
    processor.clean_data()
    processor.add_derived_features()
    processor.generate_summary()
    csv_file, excel_file = processor.save_processed_data()
    
    print(f"\n✅ Data processing completed!")
    
    return csv_file

def run_eda(input_file):
    """Run exploratory data analysis"""
    print_step(3, 3, "EXPLORATORY DATA ANALYSIS (EDA)")
    
    print(f"Analyzing file: {input_file}\n")
    
    from eda_analysis import EDAAnalyzer
    
    analyzer = EDAAnalyzer(input_file)
    analyzer.perform_eda()
    report_file = analyzer.save_summary_report()
    
    print(f"\n✅ EDA completed!")
    
    return report_file

def main():
    """Main pipeline orchestrator"""
    
    # Print welcome banner
    print("\n" + "="*70)
    print("  B2B MARKETPLACE DATA ENGINEERING PIPELINE")
    print("  Scraping → Processing → Analysis")
    print("="*70)
    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis pipeline will:")
    print("  1. Scrape products from IndiaMART (5 categories)")
    print("  2. Clean and process the data (ETL)")
    print("  3. Perform exploratory data analysis (EDA)")
    print("\nEstimated total time: 3-5 minutes")
    
    input("\nPress ENTER to start the pipeline...")
    
    start_time = time.time()
    
    try:
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Step 1: Scrape data
        raw_data_file = run_scraper()
        
        # Step 2: Process data
        processed_data_file = run_data_processor(raw_data_file)
        
        # Step 3: Analyze data
        report_file = run_eda(processed_data_file)
        
        # Final summary
        elapsed_time = time.time() - start_time
        
        print_header("PIPELINE COMPLETED SUCCESSFULLY! 🎉")
        
        print("⏱️  Execution Summary:")
        print(f"   Total time: {elapsed_time:.1f} seconds ({elapsed_time/60:.1f} minutes)")
        
        print("\n📁 Generated Files:")
        print(f"   Raw data: data/{os.path.basename(raw_data_file)}")
        print(f"   Processed data: data/{os.path.basename(processed_data_file)}")
        print(f"   EDA report: data/{os.path.basename(report_file)}")
        print(f"   Visualizations: Check data/ folder for PNG files")
        
        print("\n📊 Next Steps:")
        print("   1. Check the 'data' folder for all generated files")
        print("   2. Open the visualizations (PNG files)")
        print("   3. Review the EDA report (TXT file)")
        print("   4. Open processed data in Excel for detailed analysis")
        
        print("\n" + "="*70)
        print("Thank you for using the B2B Marketplace Data Pipeline!")
        print("="*70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n\n❌ ERROR: {str(e)}")
        print("\nPlease check:")
        print("  - Internet connection")
        print("  - All required packages are installed")
        print("  - data/ folder has write permissions")
        sys.exit(1)

if __name__ == "__main__":
    main()