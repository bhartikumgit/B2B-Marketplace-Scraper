"""
Data Processor - ETL Pipeline
Cleans and transforms scraped B2B marketplace data
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import json

class DataProcessor:
    def __init__(self, filepath):
        """
        Initialize the data processor
        
        Args:
            filepath (str): Path to the raw data file (CSV or JSON)
        """
        self.filepath = filepath
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load data from CSV or JSON file"""
        try:
            if self.filepath.endswith('.csv'):
                self.df = pd.read_csv(self.filepath)
                print(f"✓ Loaded CSV file: {self.filepath}")
            elif self.filepath.endswith('.json'):
                self.df = pd.read_json(self.filepath)
                print(f"✓ Loaded JSON file: {self.filepath}")
            else:
                raise ValueError("File must be CSV or JSON")
            
            print(f"  Initial shape: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            
        except Exception as e:
            print(f"✗ Error loading data: {str(e)}")
            raise
    
    def clean_data(self):
        """Clean and standardize the dataset"""
        print("\n" + "="*60)
        print("CLEANING DATA")
        print("="*60)
        
        initial_rows = len(self.df)
        
        # 1. Remove duplicates
        duplicates_before = self.df.duplicated().sum()
        self.df = self.df.drop_duplicates(subset=['name', 'company'], keep='first')
        print(f"✓ Removed {duplicates_before} duplicate rows")
        
        # 2. Remove rows with missing critical data
        missing_before = self.df.isnull().sum().sum()
        self.df = self.df.dropna(subset=['name'])
        print(f"✓ Removed rows with missing product names")
        
        # 3. Clean price data
        self.df['price_cleaned'] = self.df['price'].apply(self.clean_price)
        print(f"✓ Cleaned price data")
        
        # 4. Standardize location data
        self.df['location_cleaned'] = self.df['location'].apply(self.clean_location)
        self.df['state'] = self.df['location_cleaned'].apply(self.extract_state)
        print(f"✓ Standardized location data")
        
        # 5. Clean company names
        self.df['company_cleaned'] = self.df['company'].apply(self.clean_company_name)
        print(f"✓ Cleaned company names")
        
        # 6. Categorize price ranges
        self.df['price_category'] = self.df['price_cleaned'].apply(self.categorize_price)
        print(f"✓ Created price categories")
        
        # 7. Extract keywords from product names
        self.df['product_keywords'] = self.df['name'].apply(self.extract_keywords)
        print(f"✓ Extracted product keywords")
        
        final_rows = len(self.df)
        print(f"\n  Final shape: {final_rows} rows, {self.df.shape[1]} columns")
        print(f"  Rows removed: {initial_rows - final_rows}")
        print("="*60)
    
    def clean_price(self, price_text):
        """Extract numeric price from text"""
        if pd.isna(price_text) or price_text == "Price not available":
            return np.nan
        
        # Remove currency symbols and extract numbers
        price_str = str(price_text)
        numbers = re.findall(r'\d+\.?\d*', price_str)
        
        if numbers:
            price = float(numbers[0])
            
            # Handle lakhs/crores conversion
            if 'lakh' in price_str.lower():
                price = price * 100000
            elif 'crore' in price_str.lower():
                price = price * 10000000
            elif 'k' in price_str.lower():
                price = price * 1000
            
            return price
        
        return np.nan
    
    def clean_location(self, location):
        """Standardize location text"""
        if pd.isna(location) or location == "Location not available":
            return "Unknown"
        
        # Remove extra whitespace
        location = re.sub(r'\s+', ' ', str(location)).strip()
        
        # Title case
        location = location.title()
        
        return location
    
    def extract_state(self, location):
        """Extract state from location string"""
        if location == "Unknown":
            return "Unknown"
        
        # Common Indian states
        states = [
            'Maharashtra', 'Gujarat', 'Delhi', 'Tamil Nadu', 'Karnataka',
            'Uttar Pradesh', 'West Bengal', 'Rajasthan', 'Haryana',
            'Telangana', 'Andhra Pradesh', 'Punjab', 'Madhya Pradesh'
        ]
        
        for state in states:
            if state.lower() in location.lower():
                return state
        
        # If no state found, return the last part of location
        parts = location.split(',')
        return parts[-1].strip() if parts else "Unknown"
    
    def clean_company_name(self, company):
        """Clean company name"""
        if pd.isna(company) or company == "Unknown":
            return "Unknown"
        
        company = str(company).strip()
        
        # Remove common suffixes
        suffixes = ['Pvt Ltd', 'Private Limited', 'Ltd', 'Inc', 'Corporation', 'Corp']
        for suffix in suffixes:
            company = re.sub(rf'\b{suffix}\b\.?', '', company, flags=re.IGNORECASE)
        
        return company.strip().title()
    
    def categorize_price(self, price):
        """Categorize price into ranges"""
        if pd.isna(price):
            return "Unknown"
        
        if price < 1000:
            return "Budget (< ₹1K)"
        elif price < 10000:
            return "Low (₹1K-10K)"
        elif price < 50000:
            return "Medium (₹10K-50K)"
        elif price < 100000:
            return "High (₹50K-1L)"
        else:
            return "Premium (> ₹1L)"
    
    def extract_keywords(self, product_name):
        """Extract important keywords from product name"""
        if pd.isna(product_name):
            return []
        
        # Convert to lowercase and split
        words = str(product_name).lower().split()
        
        # Remove common words
        stop_words = {'and', 'or', 'the', 'a', 'an', 'in', 'on', 'at', 'for', 'with', 'from', 'to'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords[:5]  # Top 5 keywords
    
    def add_derived_features(self):
        """Add additional analytical features"""
        print("\n" + "="*60)
        print("ADDING DERIVED FEATURES")
        print("="*60)
        
        # 1. Product name length
        self.df['name_length'] = self.df['name'].str.len()
        print(f"✓ Added product name length")
        
        # 2. Has numeric price
        self.df['has_price'] = ~self.df['price_cleaned'].isna()
        print(f"✓ Added price availability flag")
        
        # 3. Category encoding
        self.df['category_code'] = pd.Categorical(self.df['category']).codes
        print(f"✓ Encoded categories")
        
        # 4. Data quality score (0-100)
        self.df['quality_score'] = self.calculate_quality_score()
        print(f"✓ Calculated data quality scores")
        
        print("="*60)
    
    def calculate_quality_score(self):
        """Calculate data quality score for each row"""
        score = pd.Series(0, index=self.df.index)
        
        # Points for having different fields
        score += (~self.df['name'].isna()).astype(int) * 30
        score += (~self.df['price_cleaned'].isna()).astype(int) * 25
        score += (self.df['company'] != 'Unknown').astype(int) * 20
        score += (self.df['location_cleaned'] != 'Unknown').astype(int) * 15
        score += (~self.df['url'].isna()).astype(int) * 10
        
        return score
    
    def generate_summary(self):
        """Generate data summary statistics"""
        print("\n" + "="*60)
        print("DATA SUMMARY")
        print("="*60)
        
        print(f"\nTotal Records: {len(self.df)}")
        print(f"Total Categories: {self.df['category'].nunique()}")
        print(f"Total Companies: {self.df['company_cleaned'].nunique()}")
        print(f"Total States: {self.df['state'].nunique()}")
        
        print(f"\n--- Price Statistics ---")
        print(f"Records with price: {self.df['has_price'].sum()} ({self.df['has_price'].mean()*100:.1f}%)")
        if self.df['price_cleaned'].notna().sum() > 0:
            print(f"Min Price: ₹{self.df['price_cleaned'].min():,.2f}")
            print(f"Max Price: ₹{self.df['price_cleaned'].max():,.2f}")
            print(f"Mean Price: ₹{self.df['price_cleaned'].mean():,.2f}")
            print(f"Median Price: ₹{self.df['price_cleaned'].median():,.2f}")
        
        print(f"\n--- Top 5 Categories ---")
        print(self.df['category'].value_counts().head())
        
        print(f"\n--- Top 5 States ---")
        print(self.df['state'].value_counts().head())
        
        print(f"\n--- Data Quality ---")
        print(f"Average Quality Score: {self.df['quality_score'].mean():.1f}/100")
        
        print("="*60)
    
    def save_processed_data(self, output_prefix='processed'):
        """Save cleaned data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save as CSV
        csv_file = f'data/{output_prefix}_{timestamp}.csv'
        self.df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"\n✓ Processed CSV saved: {csv_file}")
        
        # Save as Excel with multiple sheets
        excel_file = f'data/{output_prefix}_{timestamp}.xlsx'
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            self.df.to_excel(writer, sheet_name='All Data', index=False)
            
            # Summary by category
            category_summary = self.df.groupby('category').agg({
                'name': 'count',
                'price_cleaned': ['mean', 'median', 'min', 'max'],
                'company_cleaned': 'nunique'
            }).round(2)
            category_summary.to_excel(writer, sheet_name='Category Summary')
            
            # Summary by state
            state_summary = self.df.groupby('state').agg({
                'name': 'count',
                'price_cleaned': 'mean',
                'company_cleaned': 'nunique'
            }).round(2).sort_values('name', ascending=False)
            state_summary.to_excel(writer, sheet_name='State Summary')
        
        print(f"✓ Processed Excel saved: {excel_file}")
        
        return csv_file, excel_file

def main():
    """Main function for data processing"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python data_processor.py <data_file.csv|.json>")
        return
    
    # Process data
    processor = DataProcessor(sys.argv[1])
    processor.clean_data()
    processor.add_derived_features()
    processor.generate_summary()
    processor.save_processed_data()
    
    print("\n✅ Data processing completed successfully!")

if __name__ == "__main__":
    main()