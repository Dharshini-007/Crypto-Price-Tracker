def apply_filters(data, price_threshold=1000.0):
    filtered_data = []

    for coin in data:
        try:
            # Remove currency symbols and commas, then convert to float
            price_str = coin["Price"].replace("$", "").replace(",", "")
            price = float(price_str)

            if price >= price_threshold:
                filtered_data.append(coin)
        except Exception as e:
            print(f"Error filtering coin {coin.get('Name', '')}: {e}")

    print(f"🔎 Filtered {len(filtered_data)} coins above ${price_threshold}")
    return filtered_data
