"""
Generate realistic sample B2B marketplace data
This simulates scraped data from IndiaMART
"""

import pandas as pd
import random
from datetime import datetime
import json

# Product categories and their typical products
PRODUCT_DATA = {
    "industrial machinery": [
        "CNC Machine", "Lathe Machine", "Milling Machine", "Drilling Machine",
        "Grinding Machine", "Industrial Mixer", "Conveyor Belt System",
        "Hydraulic Press", "Power Press", "Injection Molding Machine"
    ],
    "electronic components": [
        "LED Display Panel", "Circuit Breaker", "Transformer", "Capacitor",
        "Resistor Set", "Microcontroller Board", "Power Supply Unit",
        "Relay Switch", "Sensor Module", "PCB Board"
    ],
    "textile fabrics": [
        "Cotton Fabric", "Polyester Fabric", "Silk Fabric", "Denim Fabric",
        "Linen Fabric", "Wool Fabric", "Rayon Fabric", "Georgette Fabric",
        "Canvas Fabric", "Velvet Fabric"
    ],
    "plastic raw materials": [
        "PVC Granules", "HDPE Pellets", "PP Raw Material", "PET Resin",
        "LDPE Granules", "ABS Plastic", "Polycarbonate Sheets",
        "Acrylic Sheets", "Nylon Granules", "Polystyrene Beads"
    ],
    "safety equipment": [
        "Safety Helmet", "Safety Goggles", "Hand Gloves", "Safety Shoes",
        "Fire Extinguisher", "Safety Harness", "Reflective Jacket",
        "Ear Plugs", "Face Shield", "First Aid Kit"
    ]
}

# Indian cities with states
LOCATIONS = [
    ("Mumbai", "Maharashtra"), ("Delhi", "Delhi"), ("Bangalore", "Karnataka"),
    ("Ahmedabad", "Gujarat"), ("Chennai", "Tamil Nadu"), ("Kolkata", "West Bengal"),
    ("Pune", "Maharashtra"), ("Hyderabad", "Telangana"), ("Jaipur", "Rajasthan"),
    ("Surat", "Gujarat"), ("Lucknow", "Uttar Pradesh"), ("Indore", "Madhya Pradesh"),
    ("Coimbatore", "Tamil Nadu"), ("Vadodara", "Gujarat"), ("Ludhiana", "Punjab"),
    ("Nagpur", "Maharashtra"), ("Visakhapatnam", "Andhra Pradesh"),
    ("Rajkot", "Gujarat"), ("Kanpur", "Uttar Pradesh"), ("Nashik", "Maharashtra")
]

# Company name templates
COMPANY_PREFIXES = [
    "Shree", "Sri", "Om", "Jai", "Sai", "Perfect", "Prime", "Royal",
    "Supreme", "Global", "Universal", "National", "International", "Elite",
    "Diamond", "Golden", "Silver", "Modern", "Advanced", "Precision"
]

COMPANY_SUFFIXES = [
    "Industries", "Enterprises", "Corporation", "Traders", "Suppliers",
    "Manufacturing", "Engineers", "Solutions", "Systems", "Technologies"
]

def generate_company_name():
    """Generate random company name"""
    prefix = random.choice(COMPANY_PREFIXES)
    suffix = random.choice(COMPANY_SUFFIXES)
    return f"{prefix} {suffix}"

def generate_price(category):
    """Generate realistic price based on category"""
    price_ranges = {
        "industrial machinery": (50000, 5000000),
        "electronic components": (100, 50000),
        "textile fabrics": (50, 5000),
        "plastic raw materials": (500, 100000),
        "safety equipment": (100, 10000)
    }
    
    min_price, max_price = price_ranges.get(category, (100, 10000))
    
    # 20% chance of no price
    if random.random() < 0.2:
        return "Price not available", None
    
    price = random.randint(min_price, max_price)
    
    # Format price text
    if price >= 100000:
        lakhs = price / 100000
        price_text = f"₹ {lakhs:.2f} Lakh"
    elif price >= 1000:
        price_text = f"₹ {price:,}"
    else:
        price_text = f"₹ {price}"
    
    return price_text, float(price)

def generate_rating():
    """Generate random rating"""
    if random.random() < 0.3:  # 30% no rating
        return None
    return round(random.uniform(3.5, 5.0), 1)

def generate_products(num_products=250):
    """Generate sample product data"""
    products = []
    
    for _ in range(num_products):
        # Random category
        category = random.choice(list(PRODUCT_DATA.keys()))
        
        # Random product from category
        product_base = random.choice(PRODUCT_DATA[category])
        
        # Add variation
        variations = ["", "Heavy Duty", "Industrial Grade", "Premium Quality",
                     "High Speed", "Automatic", "Semi-Automatic", "Digital"]
        variation = random.choice(variations)
        product_name = f"{variation} {product_base}".strip()
        
        # Location
        city, state = random.choice(LOCATIONS)
        location = f"{city}, {state}"
        
        # Company
        company = generate_company_name()
        
        # Price
        price_text, price_numeric = generate_price(category)
        
        # Rating
        rating = generate_rating()
        
        product = {
            'name': product_name,
            'price': price_text,
            'price_numeric': price_numeric,
            'company': company,
            'location': location,
            'category': category,
            'rating': f"{rating} ★" if rating else None,
            'url': f"https://www.indiamart.com/proddetail/{random.randint(10000000, 99999999)}.html",
            'scraped_at': datetime.now().isoformat()
        }
        
        products.append(product)
    
    return products

def main():
    """Generate and save sample data"""
    print("="*60)
    print("GENERATING SAMPLE B2B MARKETPLACE DATA")
    print("="*60)
    
    # Generate products
    num_products = 250
    print(f"\nGenerating {num_products} sample products...")
    
    products = generate_products(num_products)
    
    print(f"✓ Generated {len(products)} products")
    print(f"  Categories: {len(PRODUCT_DATA)}")
    print(f"  Companies: {len(set(p['company'] for p in products))}")
    print(f"  Locations: {len(LOCATIONS)}")
    
    # Save as JSON
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_file = f'data/indiamart_products_{timestamp}.json'
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved: {json_file}")
    
    # Save as CSV
    csv_file = f'data/indiamart_products_{timestamp}.csv'
    df = pd.DataFrame(products)
    df.to_csv(csv_file, index=False, encoding='utf-8')
    
    print(f"✓ Saved: {csv_file}")
    
    # Show sample
    print("\n" + "="*60)
    print("SAMPLE PRODUCTS")
    print("="*60)
    
    for i, product in enumerate(products[:3], 1):
        print(f"\n{i}. {product['name']}")
        print(f"   Price: {product['price']}")
        print(f"   Company: {product['company']}")
        print(f"   Location: {product['location']}")
        print(f"   Category: {product['category']}")
    
    print("\n" + "="*60)
    print("✅ Sample data generated successfully!")
    print("="*60)
    print(f"\nNext steps:")
    print(f"1. Run data processor: python data_processor.py {csv_file}")
    print(f"2. Run EDA: python eda_analysis.py data/processed_*.csv")
    print(f"3. Or run full pipeline: python main.py")
    print("="*60)
    
    return csv_file

if __name__ == "__main__":
    main()