import sqlite3
import os
from datetime import datetime

def init_database():
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'products.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS products')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            stock INTEGER NOT NULL,
            description TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_price ON products(price)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_products_stock ON products(stock)')

        products_data = [
            # Smartphones
            (1, 'iPhone 15 Pro Max', 48900.00, 'Smartphones', 45, '1TB storage, titanium finish'),
            (2, 'iPhone 15 Pro', 42900.00, 'Smartphones', 50, '256GB storage, A17 Pro chip'),
            (3, 'iPhone 15', 32900.00, 'Smartphones', 60, '128GB storage, A16 chip'),
            (4, 'Samsung Galaxy S24 Ultra', 45900.00, 'Smartphones', 40, '512GB storage, S Pen included'),
            (5, 'Samsung Galaxy S24+', 35900.00, 'Smartphones', 45, '256GB storage, AI features'),
            (6, 'Samsung Galaxy S24', 29900.00, 'Smartphones', 55, '128GB storage'),
            (7, 'Google Pixel 8 Pro', 35900.00, 'Smartphones', 35, 'Advanced AI camera features'),
            (8, 'Google Pixel 8', 27900.00, 'Smartphones', 40, 'Android flagship'),
            (9, 'OnePlus 12', 31900.00, 'Smartphones', 30, 'Snapdragon 8 Gen 3'),
            (10, 'Xiaomi 14 Pro', 29900.00, 'Smartphones', 40, 'Leica optics'),

            # Laptops
            (11, 'MacBook Pro 16"', 89900.00, 'Laptops', 25, 'M3 Max chip, 32GB RAM'),
            (12, 'MacBook Pro 14"', 69900.00, 'Laptops', 30, 'M3 Pro chip, 16GB RAM'),
            (13, 'MacBook Air 15"', 49900.00, 'Laptops', 35, 'M2 chip, 8GB RAM'),
            (14, 'MacBook Air 13"', 39900.00, 'Laptops', 40, 'M2 chip, 8GB RAM'),
            (15, 'Dell XPS 15', 65900.00, 'Laptops', 20, 'Intel i9, RTX 4070'),
            (16, 'Dell XPS 13', 45900.00, 'Laptops', 25, 'Intel i7, integrated graphics'),
            (17, 'ASUS ROG Strix SCAR', 89900.00, 'Laptops', 15, 'RTX 4090, i9 processor'),
            (18, 'ASUS ROG Zephyrus', 69900.00, 'Laptops', 20, 'RTX 4080, Ryzen 9'),
            (19, 'Lenovo ThinkPad X1', 55900.00, 'Laptops', 25, 'Business laptop'),
            (20, 'HP Spectre x360', 49900.00, 'Laptops', 30, '2-in-1 laptop'),

            # TVs
            (21, 'Samsung Neo QLED 85"', 289900.00, 'TVs', 10, '8K resolution'),
            (22, 'Samsung QLED 75"', 129900.00, 'TVs', 15, '4K resolution'),
            (23, 'LG OLED G3 77"', 199900.00, 'TVs', 12, 'OLED evo Gallery Edition'),
            (24, 'LG OLED C3 65"', 89900.00, 'TVs', 20, '4K OLED'),
            (25, 'Sony BRAVIA XR 85"', 259900.00, 'TVs', 8, 'Mini LED 8K'),
            (26, 'Sony BRAVIA XR 65"', 99900.00, 'TVs', 18, 'OLED 4K'),
            (27, 'TCL QLED 75"', 49900.00, 'TVs', 25, '4K Google TV'),
            (28, 'Hisense ULED 65"', 39900.00, 'TVs', 30, '4K Smart TV'),
            (29, 'Philips Ambilight 65"', 59900.00, 'TVs', 20, '4K with surround lighting'),
            (30, 'Samsung The Frame 55"', 49900.00, 'TVs', 25, 'Lifestyle TV'),

            # Audio
            (31, 'Sony WH-1000XM5', 13900.00, 'Audio', 60, 'Wireless noise cancelling'),
            (32, 'Apple AirPods Pro 2', 8900.00, 'Audio', 70, 'Active noise cancellation'),
            (33, 'Apple AirPods Max', 19900.00, 'Audio', 40, 'Over-ear ANC headphones'),
            (34, 'Bose QuietComfort Ultra', 12900.00, 'Audio', 50, 'Premium noise cancelling'),
            (35, 'Samsung Galaxy Buds3 Pro', 7900.00, 'Audio', 65, 'ANC earbuds'),
            (36, 'Sennheiser Momentum 4', 14900.00, 'Audio', 45, 'Wireless headphones'),
            (37, 'Sonos Arc', 29900.00, 'Audio', 30, 'Soundbar with Dolby Atmos'),
            (38, 'Sonos Sub', 24900.00, 'Audio', 25, 'Wireless subwoofer'),
            (39, 'JBL Charge 5', 5900.00, 'Audio', 80, 'Portable speaker'),
            (40, 'Marshall Stanmore III', 15900.00, 'Audio', 35, 'Bluetooth speaker'),

            # Tablets
            (41, 'iPad Pro 12.9"', 49900.00, 'Tablets', 30, 'M2 chip, mini-LED'),
            (42, 'iPad Pro 11"', 35900.00, 'Tablets', 35, 'M2 chip'),
            (43, 'iPad Air', 25900.00, 'Tablets', 45, 'M1 chip'),
            (44, 'iPad 10th gen', 18900.00, 'Tablets', 50, 'A14 chip'),
            (45, 'Samsung Galaxy Tab S9 Ultra', 45900.00, 'Tablets', 25, '14.6" display'),
            (46, 'Samsung Galaxy Tab S9+', 35900.00, 'Tablets', 30, '12.4" display'),
            (47, 'Samsung Galaxy Tab S9', 29900.00, 'Tablets', 35, '11" display'),
            (48, 'Microsoft Surface Pro 9', 49900.00, 'Tablets', 20, 'Intel i7'),
            (49, 'Lenovo Tab P12 Pro', 25900.00, 'Tablets', 40, 'OLED display'),
            (50, 'HUAWEI MatePad Pro', 23900.00, 'Tablets', 35, '12.6" OLED'),

            # Wearables
            (51, 'Apple Watch Ultra 2', 31900.00, 'Wearables', 40, 'Titanium case'),
            (52, 'Apple Watch Series 9', 15900.00, 'Wearables', 55, 'Aluminum case'),
            (53, 'Samsung Galaxy Watch 6 Pro', 15900.00, 'Wearables', 45, '47mm titanium'),
            (54, 'Samsung Galaxy Watch 6', 11900.00, 'Wearables', 50, '44mm aluminum'),
            (55, 'Garmin Fenix 7X', 29900.00, 'Wearables', 30, 'Solar edition'),
            (56, 'Garmin Epix Pro', 32900.00, 'Wearables', 25, 'AMOLED display'),
            (57, 'Fitbit Sense 2', 9900.00, 'Wearables', 60, 'Health tracking'),
            (58, 'HUAWEI Watch GT 4', 8900.00, 'Wearables', 55, 'Fitness tracking'),
            (59, 'Withings ScanWatch 2', 13900.00, 'Wearables', 40, 'Hybrid smartwatch'),
            (60, 'Oura Ring Gen 3', 11900.00, 'Wearables', 35, 'Smart ring'),

            # Cameras
            (61, 'Sony A7R V', 129900.00, 'Cameras', 15, 'Full-frame mirrorless'),
            (62, 'Sony A7 IV', 79900.00, 'Cameras', 20, 'Hybrid full-frame'),
            (63, 'Canon EOS R6 Mark II', 89900.00, 'Cameras', 18, 'Full-frame mirrorless'),
            (64, 'Canon EOS R8', 59900.00, 'Cameras', 25, 'Entry full-frame'),
            (65, 'Nikon Z8', 99900.00, 'Cameras', 15, 'Pro mirrorless'),
            (66, 'Nikon Z6 II', 69900.00, 'Cameras', 20, 'All-around mirrorless'),
            (67, 'Fujifilm X-T5', 59900.00, 'Cameras', 25, 'APS-C flagship'),
            (68, 'Fujifilm X-S20', 45900.00, 'Cameras', 30, 'Hybrid shooter'),
            (69, 'GoPro Hero 12 Black', 15900.00, 'Cameras', 40, 'Action camera'),
            (70, 'DJI Osmo Action 4', 14900.00, 'Cameras', 35, 'Action camera'),

            # Gaming
            (71, 'PS5 Pro', 21900.00, 'Gaming', 30, 'Next-gen console'),
            (72, 'PS5 Digital', 14900.00, 'Gaming', 35, 'Digital edition'),
            (73, 'Xbox Series X', 16900.00, 'Gaming', 30, 'Flagship console'),
            (74, 'Xbox Series S', 9900.00, 'Gaming', 40, 'Digital console'),
            (75, 'Nintendo Switch OLED', 11900.00, 'Gaming', 45, 'Enhanced portable'),
            (76, 'Nintendo Switch Lite', 7900.00, 'Gaming', 50, 'Portable only'),
            (77, 'Steam Deck OLED', 19900.00, 'Gaming', 25, 'Portable PC gaming'),
            (78, 'ROG Ally', 21900.00, 'Gaming', 20, 'Windows handheld'),
            (79, 'PS VR2', 19900.00, 'Gaming', 30, 'VR headset'),
            (80, 'Meta Quest 3', 18900.00, 'Gaming', 35, 'VR headset'),

            # Home Appliances
            (81, 'Samsung Bespoke Fridge', 89900.00, 'Appliances', 15, 'Smart refrigerator'),
            (82, 'LG InstaView Fridge', 79900.00, 'Appliances', 18, 'Door-in-door'),
            (83, 'Dyson V15s Detect', 27900.00, 'Appliances', 30, 'Robot vacuum'),
            (84, 'Dyson V12', 19900.00, 'Appliances', 35, 'Cordless vacuum'),
            (85, 'iRobot Roomba j9+', 39900.00, 'Appliances', 25, 'Robot vacuum'),
            (86, 'Philips Airfryer XXL', 7900.00, 'Appliances', 45, 'Digital airfryer'),
            (87, 'Samsung Microwave', 5900.00, 'Appliances', 50, 'Smart inverter'),
            (88, 'LG Washing Machine', 25900.00, 'Appliances', 20, 'AI DD technology'),
            (89, 'Hitachi Air Purifier', 15900.00, 'Appliances', 40, 'HEPA filter'),
            (90, 'Panasonic Rice Cooker', 4900.00, 'Appliances', 55, 'Induction heating'),

            # Accessories
            (91, 'Apple Magic Keyboard', 4900.00, 'Accessories', 70, 'Wireless keyboard'),
            (92, 'Logitech MX Master 3S', 3900.00, 'Accessories', 80, 'Wireless mouse'),
            (93, 'Samsung T7 Shield 2TB', 5900.00, 'Accessories', 65, 'Portable SSD'),
            (94, 'Anker 737 Power Bank', 3900.00, 'Accessories', 75, '24000mAh capacity'),
            (95, 'Apple AirTag 4 Pack', 3900.00, 'Accessories', 85, 'Item tracker'),
            (96, 'Belkin 3-in-1 Charger', 4900.00, 'Accessories', 60, 'Wireless charging'),
            (97, 'Canon Pixma Printer', 7900.00, 'Accessories', 40, 'All-in-one printer'),
            (98, 'LG 32" 4K Monitor', 15900.00, 'Accessories', 35, 'USB-C display'),
            (99, 'Apple Pencil 2', 4900.00, 'Accessories', 70, 'Stylus pen'),
            (100, 'Samsung S Pen Pro', 3900.00, 'Accessories', 75, 'Universal stylus')
        ]

        cursor.executemany('''
        INSERT OR REPLACE INTO products (id, name, price, category, stock, description)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', products_data)

        conn.commit()
        print("Database initialized successfully!")
        return conn

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def display_products(conn, category=None, limit=5):
    try:
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
            SELECT id, name, price, category, stock 
            FROM products 
            WHERE category = ? 
            LIMIT ?
            ''', (category, limit))
        else:
            cursor.execute('''
            SELECT id, name, price, category, stock 
            FROM products 
            LIMIT ?
            ''', (limit,))
        
        products = cursor.fetchall()
        
        print("\nProducts in database:")
        print(f"{'ID':<4} {'Name':<25} {'Price':<12} {'Category':<15} {'Stock':<6}")
        print("-" * 65)
        
        for product in products:
            print(f"{product[0]:<4} {product[1]:<25} {product[2]:<12,.2f} {product[3]:<15} {product[4]:<6}")
            
    except sqlite3.Error as e:
        print(f"Error displaying products: {e}")

def get_categories(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT category FROM products')
        return [category[0] for category in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error getting categories: {e}")
        return []

def main():
    conn = init_database()
    if not conn:
        print("Failed to initialize database")
        return

    try:
        # Display available categories
        categories = get_categories(conn)
        print("\nAvailable categories:", categories)

        # Display sample products from each category
        for category in categories:
            print(f"\nProducts in {category} category:")
            display_products(conn, category=category, limit=3)

    finally:
        conn.close()

if __name__ == "__main__":
    main()