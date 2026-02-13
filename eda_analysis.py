 
"""
Exploratory Data Analysis (EDA)
Analyzes B2B marketplace data and generates insights with visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

class EDAAnalyzer:
    def __init__(self, filepath):
        """
        Initialize EDA Analyzer
        
        Args:
            filepath (str): Path to processed data file
        """
        self.filepath = filepath
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load processed data"""
        try:
            if self.filepath.endswith('.csv'):
                self.df = pd.read_csv(self.filepath)
            elif self.filepath.endswith('.xlsx'):
                self.df = pd.read_excel(self.filepath, sheet_name='All Data')
            
            print(f"✓ Loaded data: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            
        except Exception as e:
            print(f"✗ Error loading data: {str(e)}")
            raise
    
    def perform_eda(self):
        """Perform complete exploratory data analysis"""
        print("\n" + "="*70)
        print("EXPLORATORY DATA ANALYSIS (EDA)")
        print("="*70)
        
        # 1. Basic statistics
        self.display_basic_stats()
        
        # 2. Category analysis
        self.analyze_categories()
        
        # 3. Price analysis
        self.analyze_prices()
        
        # 4. Location analysis
        self.analyze_locations()
        
        # 5. Company analysis
        self.analyze_companies()
        
        # 6. Data quality analysis
        self.analyze_data_quality()
        
        # 7. Generate visualizations
        self.create_visualizations()
        
        # 8. Generate insights report
        self.generate_insights()
    
    def display_basic_stats(self):
        """Display basic dataset statistics"""
        print("\n📊 BASIC STATISTICS")
        print("-" * 70)
        
        print(f"Total Products: {len(self.df)}")
        print(f"Unique Categories: {self.df['category'].nunique()}")
        print(f"Unique Companies: {self.df['company_cleaned'].nunique()}")
        print(f"Unique Locations: {self.df['location_cleaned'].nunique()}")
        
        print(f"\nData Types:")
        print(self.df.dtypes.value_counts())
        
        print(f"\nMissing Values:")
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        missing_df = pd.DataFrame({
            'Missing Count': missing,
            'Percentage': missing_pct
        })
        print(missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False))
    
    def analyze_categories(self):
        """Analyze product categories"""
        print("\n📦 CATEGORY ANALYSIS")
        print("-" * 70)
        
        category_counts = self.df['category'].value_counts()
        
        print(f"\nProducts per Category:")
        for cat, count in category_counts.items():
            pct = (count / len(self.df)) * 100
            print(f"  {cat}: {count} ({pct:.1f}%)")
        
        # Average price by category (if available)
        if 'price_cleaned' in self.df.columns:
            print(f"\nAverage Price by Category:")
            avg_price = self.df.groupby('category')['price_cleaned'].mean().sort_values(ascending=False)
            for cat, price in avg_price.items():
                if not pd.isna(price):
                    print(f"  {cat}: ₹{price:,.2f}")
    
    def analyze_prices(self):
        """Analyze price distributions"""
        print("\n💰 PRICE ANALYSIS")
        print("-" * 70)
        
        if 'price_cleaned' not in self.df.columns:
            print("No price data available")
            return
        
        prices = self.df['price_cleaned'].dropna()
        
        if len(prices) == 0:
            print("No valid price data available")
            return
        
        print(f"\nPrice Statistics:")
        print(f"  Products with price: {len(prices)} ({len(prices)/len(self.df)*100:.1f}%)")
        print(f"  Minimum: ₹{prices.min():,.2f}")
        print(f"  Maximum: ₹{prices.max():,.2f}")
        print(f"  Mean: ₹{prices.mean():,.2f}")
        print(f"  Median: ₹{prices.median():,.2f}")
        print(f"  Std Dev: ₹{prices.std():,.2f}")
        
        # Price range distribution
        if 'price_category' in self.df.columns:
            print(f"\nPrice Range Distribution:")
            price_dist = self.df['price_category'].value_counts()
            for cat, count in price_dist.items():
                pct = (count / len(self.df)) * 100
                print(f"  {cat}: {count} ({pct:.1f}%)")
    
    def analyze_locations(self):
        """Analyze geographical distribution"""
        print("\n🌍 LOCATION ANALYSIS")
        print("-" * 70)
        
        # Top states
        if 'state' in self.df.columns:
            print(f"\nTop 10 States by Product Count:")
            top_states = self.df['state'].value_counts().head(10)
            for state, count in top_states.items():
                pct = (count / len(self.df)) * 100
                print(f"  {state}: {count} ({pct:.1f}%)")
        
        # Top cities
        print(f"\nTop 10 Cities by Product Count:")
        top_cities = self.df['location_cleaned'].value_counts().head(10)
        for city, count in top_cities.items():
            pct = (count / len(self.df)) * 100
            print(f"  {city}: {count} ({pct:.1f}%)")
    
    def analyze_companies(self):
        """Analyze supplier/company patterns"""
        print("\n🏢 COMPANY ANALYSIS")
        print("-" * 70)
        
        total_companies = self.df['company_cleaned'].nunique()
        print(f"\nTotal Unique Companies: {total_companies}")
        
        # Top companies by product count
        print(f"\nTop 10 Companies by Product Listings:")
        top_companies = self.df['company_cleaned'].value_counts().head(10)
        for company, count in top_companies.items():
            if company != 'Unknown':
                print(f"  {company}: {count} products")
        
        # Companies per category
        print(f"\nAverage Companies per Category:")
        companies_per_cat = self.df.groupby('category')['company_cleaned'].nunique()
        for cat, count in companies_per_cat.items():
            print(f"  {cat}: {count} companies")
    
    def analyze_data_quality(self):
        """Analyze data quality metrics"""
        print("\n✅ DATA QUALITY ANALYSIS")
        print("-" * 70)
        
        if 'quality_score' in self.df.columns:
            avg_quality = self.df['quality_score'].mean()
            print(f"\nAverage Quality Score: {avg_quality:.1f}/100")
            
            # Quality distribution
            quality_bins = pd.cut(self.df['quality_score'], bins=[0, 50, 70, 90, 100], 
                                  labels=['Poor', 'Fair', 'Good', 'Excellent'])
            print(f"\nQuality Distribution:")
            for quality, count in quality_bins.value_counts().items():
                pct = (count / len(self.df)) * 100
                print(f"  {quality}: {count} ({pct:.1f}%)")
        
        # Completeness by field
        print(f"\nField Completeness:")
        completeness = ((~self.df.isnull()).sum() / len(self.df)) * 100
        for field, pct in completeness.sort_values(ascending=False).items():
            print(f"  {field}: {pct:.1f}%")
    
    def create_visualizations(self):
        """Generate all visualizations"""
        print("\n📈 GENERATING VISUALIZATIONS")
        print("-" * 70)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 12))
        
        # 1. Category Distribution
        ax1 = plt.subplot(2, 3, 1)
        category_counts = self.df['category'].value_counts()
        colors = sns.color_palette('husl', len(category_counts))
        category_counts.plot(kind='bar', color=colors, ax=ax1)
        ax1.set_title('Product Distribution by Category', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Category')
        ax1.set_ylabel('Number of Products')
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Price Distribution
        ax2 = plt.subplot(2, 3, 2)
        if 'price_cleaned' in self.df.columns:
            prices = self.df['price_cleaned'].dropna()
            if len(prices) > 0:
                # Use log scale for better visualization
                prices_log = np.log10(prices + 1)
                ax2.hist(prices_log, bins=30, color='skyblue', edgecolor='black')
                ax2.set_title('Price Distribution (Log Scale)', fontsize=14, fontweight='bold')
                ax2.set_xlabel('Log10(Price + 1)')
                ax2.set_ylabel('Frequency')
        
        # 3. Top 10 States
        ax3 = plt.subplot(2, 3, 3)
        if 'state' in self.df.columns:
            top_states = self.df['state'].value_counts().head(10)
            top_states.plot(kind='barh', color='coral', ax=ax3)
            ax3.set_title('Top 10 States by Products', fontsize=14, fontweight='bold')
            ax3.set_xlabel('Number of Products')
            ax3.set_ylabel('State')
        
        # 4. Price Range Distribution
        ax4 = plt.subplot(2, 3, 4)
        if 'price_category' in self.df.columns:
            price_cat_counts = self.df['price_category'].value_counts()
            colors_pie = sns.color_palette('Set2', len(price_cat_counts))
            ax4.pie(price_cat_counts.values, labels=price_cat_counts.index, autopct='%1.1f%%',
                   colors=colors_pie, startangle=90)
            ax4.set_title('Distribution by Price Range', fontsize=14, fontweight='bold')
        
        # 5. Average Price by Category
        ax5 = plt.subplot(2, 3, 5)
        if 'price_cleaned' in self.df.columns:
            avg_price_cat = self.df.groupby('category')['price_cleaned'].mean().sort_values()
            if not avg_price_cat.empty:
                avg_price_cat.plot(kind='barh', color='lightgreen', ax=ax5)
                ax5.set_title('Average Price by Category', fontsize=14, fontweight='bold')
                ax5.set_xlabel('Average Price (₹)')
                ax5.set_ylabel('Category')
        
        # 6. Data Quality Score Distribution
        ax6 = plt.subplot(2, 3, 6)
        if 'quality_score' in self.df.columns:
            ax6.hist(self.df['quality_score'], bins=20, color='mediumpurple', edgecolor='black')
            ax6.axvline(self.df['quality_score'].mean(), color='red', linestyle='--', 
                       linewidth=2, label=f'Mean: {self.df["quality_score"].mean():.1f}')
            ax6.set_title('Data Quality Score Distribution', fontsize=14, fontweight='bold')
            ax6.set_xlabel('Quality Score')
            ax6.set_ylabel('Frequency')
            ax6.legend()
        
        plt.tight_layout()
        
        # Save figure
        viz_filename = f'data/eda_visualizations_{timestamp}.png'
        plt.savefig(viz_filename, dpi=300, bbox_inches='tight')
        print(f"✓ Visualizations saved: {viz_filename}")
        
        plt.close()
    
    def generate_insights(self):
        """Generate key insights and recommendations"""
        print("\n💡 KEY INSIGHTS & FINDINGS")
        print("="*70)
        
        insights = []
        
        # 1. Category insights
        top_category = self.df['category'].value_counts().index[0]
        top_cat_count = self.df['category'].value_counts().values[0]
        insights.append(f"1. '{top_category}' is the most popular category with {top_cat_count} products")
        
        # 2. Price insights
        if 'price_cleaned' in self.df.columns and self.df['price_cleaned'].notna().sum() > 0:
            price_availability = (self.df['price_cleaned'].notna().sum() / len(self.df)) * 100
            insights.append(f"2. Only {price_availability:.1f}% of products have visible pricing")
            
            avg_price = self.df['price_cleaned'].mean()
            insights.append(f"3. Average product price is ₹{avg_price:,.2f}")
        
        # 3. Location insights
        if 'state' in self.df.columns:
            top_state = self.df['state'].value_counts().index[0]
            top_state_count = self.df['state'].value_counts().values[0]
            insights.append(f"4. '{top_state}' has the most suppliers with {top_state_count} products")
        
        # 4. Company insights
        total_companies = self.df['company_cleaned'].nunique()
        avg_products_per_company = len(self.df) / total_companies
        insights.append(f"5. {total_companies} unique companies with avg {avg_products_per_company:.1f} products each")
        
        # 5. Data quality insights
        if 'quality_score' in self.df.columns:
            avg_quality = self.df['quality_score'].mean()
            if avg_quality >= 80:
                quality_msg = "excellent"
            elif avg_quality >= 60:
                quality_msg = "good"
            else:
                quality_msg = "needs improvement"
            insights.append(f"6. Overall data quality is {quality_msg} (score: {avg_quality:.1f}/100)")
        
        # Print insights
        for insight in insights:
            print(f"\n{insight}")
        
        print("\n" + "="*70)
        
        # Recommendations
        print("\n📋 RECOMMENDATIONS")
        print("-" * 70)
        recommendations = [
            "• Target categories with fewer listings for less competition",
            "• Focus on states with high supplier concentration for better sourcing",
            "• Products without prices may need direct inquiry - automation opportunity",
            "• Consider regional pricing patterns for market positioning",
            "• Data quality improvement needed for products with low scores"
        ]
        
        for rec in recommendations:
            print(rec)
        
        print("\n" + "="*70)
    
    def save_summary_report(self):
        """Save analysis summary to text file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'data/eda_report_{timestamp}.txt'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("B2B MARKETPLACE DATA - EDA SUMMARY REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Dataset: {self.filepath}\n")
            f.write(f"Total Records: {len(self.df)}\n\n")
            
            f.write("DATASET OVERVIEW\n")
            f.write("-"*70 + "\n")
            f.write(self.df.describe(include='all').to_string())
            f.write("\n\n")
            
            f.write("CATEGORY DISTRIBUTION\n")
            f.write("-"*70 + "\n")
            f.write(self.df['category'].value_counts().to_string())
            f.write("\n\n")
            
            if 'state' in self.df.columns:
                f.write("TOP 15 STATES\n")
                f.write("-"*70 + "\n")
                f.write(self.df['state'].value_counts().head(15).to_string())
                f.write("\n\n")
        
        print(f"\n✓ Summary report saved: {report_file}")
        return report_file

def main():
    """Main function for EDA"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python eda_analysis.py <processed_data.csv|.xlsx>")
        return
    
    # Perform EDA
    analyzer = EDAAnalyzer(sys.argv[1])
    analyzer.perform_eda()
    analyzer.save_summary_report()
    
    print("\n✅ EDA completed successfully!")

if __name__ == "__main__":
    main()