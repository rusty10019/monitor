#!/usr/bin/env python3
"""
SHEIN User Monitoring Script - Simple Version
User clones from GitHub, adds cookies.txt, runs script
"""

import requests
import json
import time
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================
# CONFIGURATION
# ============================================

# Bot Token - Load from .env file
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
    print("❌ ERROR: Bot token not configured!")
    print("")
    print("Please create a .env file with your bot token:")
    print("1. Copy .env.example to .env")
    print("2. Edit .env and add your bot token")
    print("3. Get token from @BotFather on Telegram")
    print("")
    exit(1)

# Cookies file (user creates this)
COOKIES_FILE = "cookies.txt"

# ============================================
# MONITORING SETTINGS
# ============================================

CHECK_INTERVAL = 10  # seconds between checks
TOTAL_PAGES = 9  # pages to check
PAGE_SIZE = 10  # products per page
REQUEST_TIMEOUT = 10  # seconds
MAX_NOTIFICATIONS_PER_PRODUCT = 3  # max alerts per product

# ============================================
# API ENDPOINTS
# ============================================

WISHLIST_API = "https://www.sheinindia.in/api/wishlist/getwishlist"

# ============================================
# SETUP LOGGING
# ============================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# STATE MANAGEMENT
# ============================================

NOTIFICATION_COUNT_FILE = "notification_count.json"
PREVIOUS_STOCK_STATUS = {}
USER_CHAT_ID = None  # Will be set by user input


def load_notification_counts():
    """Load notification counts from file"""
    if os.path.exists(NOTIFICATION_COUNT_FILE):
        try:
            with open(NOTIFICATION_COUNT_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_notification_counts(counts):
    """Save notification counts to file"""
    with open(NOTIFICATION_COUNT_FILE, 'w') as f:
        json.dump(counts, f, indent=2)


NOTIFICATION_COUNTS = load_notification_counts()


def parse_cookie_header(cookie_string):
    """Parse cookie string into dictionary"""
    cookies = {}
    pairs = cookie_string.strip().split(';')
    for pair in pairs:
        if '=' in pair:
            key, value = pair.strip().split('=', 1)
            cookies[key] = value
    return cookies


def load_cookies():
    """Load cookies from cookies.txt file"""
    if not os.path.exists(COOKIES_FILE):
        logger.error(f"❌ Cookies file not found: {COOKIES_FILE}")
        logger.error("")
        logger.error("Please create cookies.txt file with your SHEIN cookies!")
        logger.error("")
        logger.error("How to get cookies:")
        logger.error("1. Open https://www.sheinindia.in/ in browser")
        logger.error("2. Login to your account")
        logger.error("3. Press F12 (DevTools)")
        logger.error("4. Go to Network tab")
        logger.error("5. Refresh page")
        logger.error("6. Click any request")
        logger.error("7. Copy Cookie header")
        logger.error("8. Paste into cookies.txt file")
        logger.error("")
        return None
    
    try:
        with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
            cookie_string = f.read().strip()
            
        if not cookie_string:
            logger.error("❌ cookies.txt is empty!")
            return None
            
        cookies = parse_cookie_header(cookie_string)
        
        if len(cookies) < 3:
            logger.error("❌ Invalid cookies! Too few cookies found.")
            return None
            
        logger.info(f"✅ Loaded {len(cookies)} cookies from {COOKIES_FILE}")
        return cookies
        
    except Exception as e:
        logger.error(f"❌ Error loading cookies: {e}")
        return None


def get_user_chat_id():
    """Get user's Chat ID from input"""
    print("")
    print("=" * 70)
    print("📱 TELEGRAM NOTIFICATION SETUP")
    print("=" * 70)
    print("")
    print("To receive notifications, you need your Telegram Chat ID.")
    print("")
    print("How to get your Chat ID:")
    print("1. Open Telegram")
    print("2. Search for the bot")
    print("3. Send /start")
    print("4. Bot will show your Chat ID")
    print("")
    print("=" * 70)
    print("")
    
    while True:
        chat_id = input("Enter your Chat ID: ").strip()
        
        if not chat_id:
            print("❌ Chat ID cannot be empty!")
            continue
            
        if not chat_id.isdigit():
            print("❌ Chat ID must be numbers only!")
            continue
        
        # Verify with user
        print("")
        print(f"Your Chat ID: {chat_id}")
        confirm = input("Is this correct? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            return chat_id
        else:
            print("Let's try again...")
            print("")


def send_telegram_message(chat_id, message):
    """Send message via Telegram Bot API"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"❌ Failed to send Telegram message: {e}")
        return False


def send_notification_to_user(product):
    """Send notification to user"""
    raw_url = product.get('url', '')
    if raw_url.startswith('http'):
        import re
        product_url = re.sub(r'-[a-z0-9]+\.html$', '.html', raw_url, flags=re.IGNORECASE)
    elif raw_url:
        import re
        clean_url = re.sub(r'-[a-z0-9]+\.html$', '.html', raw_url, flags=re.IGNORECASE)
        product_url = f"https://www.sheinindia.in{clean_url}"
    else:
        product_url = f"https://www.sheinindia.in/product-{product['productCode']}.html"
    
    message = (
        f"🔔 *IN-STOCK ALERT!*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📦 Product: {product['name']}\n"
        f"📏 Size: {product['size']}\n"
        f"💰 Price: Rs.{product['price']}\n"
        f"🔖 Code: `{product['productCode']}`\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🛒 [OPEN PRODUCT]({product_url})\n\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📢 @rusty\\_whoo"
    )
    
    return send_telegram_message(USER_CHAT_ID, message)


def send_notification_to_admin(product, username):
    """Send notification to admin"""
    raw_url = product.get('url', '')
    if raw_url.startswith('http'):
        import re
        product_url = re.sub(r'-[a-z0-9]+\.html$', '.html', raw_url, flags=re.IGNORECASE)
    elif raw_url:
        import re
        clean_url = re.sub(r'-[a-z0-9]+\.html$', '.html', raw_url, flags=re.IGNORECASE)
        product_url = f"https://www.sheinindia.in{clean_url}"
    else:
        product_url = f"https://www.sheinindia.in/product-{product['productCode']}.html"
    
    message = (
        f"🔔 *Stock Alert - User @{username}*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👤 User: @{username} (`{USER_CHAT_ID}`)\n"
        f"📦 Product: {product['name']}\n"
        f"📏 Size: {product['size']}\n"
        f"💰 Price: Rs.{product['price']}\n"
        f"🔖 Code: `{product['productCode']}`\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🛒 [OPEN PRODUCT]({product_url})"
    )
    
    return send_telegram_message(ADMIN_CHAT_ID, message)


def fetch_wishlist_page(cookies, page_num):
    """Fetch single page of wishlist"""
    params = {
        'currentPage': page_num,
        'pageSize': PAGE_SIZE,
        'store': 'shein'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.sheinindia.in/',
        'Authorization': f'Bearer {cookies.get("A", "")}',
    }
    
    try:
        response = requests.get(
            WISHLIST_API,
            params=params,
            cookies=cookies,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        return data.get('products', [])
        
    except Exception as e:
        logger.debug(f"Error fetching page {page_num}: {e}")
        return []


def extract_wishlist_products(cookies):
    """Extract all in-stock products from wishlist"""
    in_stock_products = []
    total_products = 0
    
    for page_num in range(TOTAL_PAGES + 1):
        products = fetch_wishlist_page(cookies, page_num)
        
        if not products:
            break
        
        for product in products:
            total_products += 1
            product_code = product.get('productCode', '')
            product_name = product.get('name', 'Unknown')
            
            if 'variantOptions' in product:
                for variant in product['variantOptions']:
                    stock = variant.get('stock', {})
                    if stock.get('stockLevelStatus') == 'inStock':
                        size = next(
                            (q['value'] for q in variant.get('variantOptionQualifiers', [])
                             if q['qualifier'] == 'size'),
                            'Unknown'
                        )
                        
                        in_stock_products.append({
                            'productCode': product_code,
                            'name': product_name,
                            'size': size,
                            'price': product.get('price', {}).get('value', 0),
                            'url': product.get('url', '')
                        })
        
        time.sleep(0.1)  # Small delay between pages
    
    return in_stock_products, total_products


def monitor_wishlist():
    """Main monitoring loop"""
    global PREVIOUS_STOCK_STATUS, NOTIFICATION_COUNTS, USER_CHAT_ID
    
    # Load cookies
    cookies = load_cookies()
    if not cookies:
        return
    
    # Get user's Chat ID
    USER_CHAT_ID = get_user_chat_id()
    
    # Get username from Telegram
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChat"
        response = requests.get(url, params={"chat_id": USER_CHAT_ID}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            username = data.get('result', {}).get('username', 'Unknown')
        else:
            username = 'Unknown'
    except:
        username = 'Unknown'
    
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ███████╗██╗  ██╗███████╗██╗███╗   ██╗                         ║
║   ██╔════╝██║  ██║██╔════╝██║████╗  ██║                         ║
║   ███████╗███████║█████╗  ██║██╔██╗ ██║                         ║
║   ╚════██║██╔══██║██╔══╝  ██║██║╚██╗██║                         ║
║   ███████║██║  ██║███████╗██║██║ ╚████║                         ║
║   ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝                         ║
║                                                                  ║
║              📱 USER MONITORING SCRIPT 📱                       ║
║                                                                  ║
║              Running on YOUR device                             ║
║              Using YOUR cookies                                 ║
║              Using YOUR IP (no proxy!)                          ║
║                                                                  ║
║══════════════════════════════════════════════════════════════════║
║                                                                  ║
║              👤 Created by: @rusty_whoo                         ║
║              📢 Channels: @rusty_whoo & @Looters_01             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    
    print(banner)
    logger.info("🚀 Starting SHEIN Wishlist Monitor...")
    logger.info(f"👤 User: @{username} ({USER_CHAT_ID})")
    logger.info(f"⏱️  Check interval: {CHECK_INTERVAL}s")
    logger.info(f"📦 Monitoring {TOTAL_PAGES + 1} pages...")
    
    # Send start notification to user
    send_telegram_message(
        USER_CHAT_ID,
        f"🚀 *MONITORING STARTED*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👤 User: @{username}\n"
        f"⏱️ Check interval: {CHECK_INTERVAL}s\n"
        f"🔔 Max alerts: {MAX_NOTIFICATIONS_PER_PRODUCT} per product\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"✅ Monitor is running on your device!\n"
        f"💬 You'll get alerts when stock is found!\n\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📢 @rusty\\_whoo"
    )
    
    # Send start notification to admin
    send_telegram_message(
        ADMIN_CHAT_ID,
        f"🚀 *USER STARTED MONITORING*\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👤 User: @{username}\n"
        f"🆔 Chat ID: `{USER_CHAT_ID}`\n"
        f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"━━━━━━━━━━━━━━━━"
    )
    
    # Initial scan
    logger.info("🔄 Performing initial scan...")
    initial_products, total_count = extract_wishlist_products(cookies)
    PREVIOUS_STOCK_STATUS = {p['productCode']: True for p in initial_products}
    logger.info(f"📊 Total: {total_count} | In-stock: {len(initial_products)} | Out-of-stock: {total_count - len(initial_products)}")
    
    scan_count = 0
    
    try:
        while True:
            scan_count += 1
            start_time = time.time()
            
            # Fetch current wishlist
            products, total = extract_wishlist_products(cookies)
            
            notified = 0
            
            # Check for new stock
            for product in products:
                code = product['productCode']
                
                # Check if this is new stock
                was_in_stock = PREVIOUS_STOCK_STATUS.get(code, False)
                PREVIOUS_STOCK_STATUS[code] = True
                
                if was_in_stock:
                    continue  # Already in stock, skip
                
                # Check notification limit
                notify_count = NOTIFICATION_COUNTS.get(code, 0)
                if notify_count >= MAX_NOTIFICATIONS_PER_PRODUCT:
                    continue  # Max notifications reached
                
                # Increment notification count
                notify_count += 1
                NOTIFICATION_COUNTS[code] = notify_count
                save_notification_counts(NOTIFICATION_COUNTS)
                
                # Send notification to user
                if send_notification_to_user(product):
                    logger.info(f"📨 Alert sent to user: {product['name']} ({code})")
                    notified += 1
                else:
                    logger.error(f"❌ Failed to send alert to user for {code}")
                
                # Send notification to admin
                if send_notification_to_admin(product, username):
                    logger.info(f"📨 Alert sent to admin: {product['name']} ({code})")
                else:
                    logger.error(f"❌ Failed to send alert to admin for {code}")
                
                time.sleep(0.5)  # Small delay between notifications
            
            # Update out-of-stock products
            current_codes = {p['productCode'] for p in products}
            for code in list(PREVIOUS_STOCK_STATUS.keys()):
                if code not in current_codes:
                    PREVIOUS_STOCK_STATUS[code] = False
            
            duration = time.time() - start_time
            logger.info(f"Scan #{scan_count}: {duration:.1f}s | Total: {total} | In-stock: {len(products)} | Notified: {notified}")
            
            # Wait before next scan
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("\n⏹️  Monitor stopped by user")
        send_telegram_message(
            USER_CHAT_ID,
            "⏹️ *Monitoring Stopped*\n\n"
            "━━━━━━━━━━━━━━━━\n"
            "📢 @rusty\\_whoo"
        )
        send_telegram_message(
            ADMIN_CHAT_ID,
            f"⏹️ *USER STOPPED MONITORING*\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"👤 User: @{username}\n"
            f"🆔 Chat ID: `{USER_CHAT_ID}`\n"
            f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"━━━━━━━━━━━━━━━━"
        )
    except Exception as e:
        logger.error(f"❌ Monitor error: {e}")
        send_telegram_message(
            USER_CHAT_ID,
            f"❌ *Monitor Error*\n{str(e)}\n\n"
            "━━━━━━━━━━━━━━━━\n"
            "📢 @rusty\\_whoo"
        )


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              📱 SHEIN USER MONITORING SCRIPT 📱                 ║
║                                                                  ║
║              👤 Created by: @rusty_whoo                         ║
║              📢 Channels: @rusty_whoo & @Looters_01             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    logger.info("🚀 Starting User Monitoring Script...")
    logger.info("📱 This script runs on YOUR device")
    logger.info("🍪 Uses YOUR cookies from cookies.txt")
    logger.info("🌐 Uses YOUR IP (no proxy needed!)")
    logger.info("🔔 Sends notifications to YOU and ADMIN")
    
    try:
        monitor_wishlist()
    except KeyboardInterrupt:
        logger.info("\n⏹️  Script stopped by user")
