from utils.scraper import scrape_top_10_coins
from utils.exporter import export_to_csv
from utils.filters import apply_filters
from config import HEADLESS, FILTER_BY_PRICE, PRICE_THRESHOLD

def main():
    print("🚀 Starting Cryptocurrency Price Tracker...")

    coins_data = scrape_top_10_coins(headless=HEADLESS)

    if FILTER_BY_PRICE:
        coins_data = apply_filters(coins_data, price_threshold=PRICE_THRESHOLD)

    export_to_csv(coins_data)

    print("✅ Tracking complete.")

if __name__ == "__main__":
    main()
