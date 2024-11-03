from binance.client import Client
import time

# Replace with your actual API key and secret
API_KEY = 'lVoEhrUYuE264vw4DFvg02WpAxHRWuiWCjNhzp5aakptHAAnh8lKZtgjKcyUvJ69'
API_SECRET = 'VHSRivcr1lbnVxzVqZMny5oMNn3t78l4BMKChlR2aBxUyvWtBsEPWqve4kzkDpXw'

# Initialize the Binance client for the live environment
client = Client(API_KEY, API_SECRET)

symbol = 'BTCUSDT'
investment_amount = 5.0  # Amount in USD to spend per order

def get_current_price(symbol):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def calculate_trade_quantity(investment_amount, current_price):
    return round(investment_amount / current_price, 6)  # Adjust precision as necessary

def place_buy_order(symbol, quantity):
    try:
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
        print(f"Buy order done: {order}")
    except Exception as e:
        print(f"An error occurred while placing buy order: {e}")

def place_sell_order(symbol, quantity):
    try:
        order = client.order_market_sell(symbol=symbol, quantity=quantity)
        print(f"Sell order done: {order}")
    except Exception as e:
        print(f"An error occurred while placing sell order: {e}")

def trading_bot():
    previous_price = get_current_price(symbol)  # Initialize previous_price here
    in_position = False

    while True:
        current_price = get_current_price(symbol)
        print(f"Current price of {symbol}: {current_price}")

        # Calculate the price thresholds based on the previous price
        buy_price_threshold = previous_price * 0.95  # 5% down
        sell_price_threshold = previous_price * 1.015  # 1.5% up

        if not in_position:
            if current_price < buy_price_threshold:
                print(f"Price is below {buy_price_threshold:.2f}. Placing buy order.")
                trade_quantity = calculate_trade_quantity(investment_amount, current_price)
                place_buy_order(symbol, trade_quantity)
                in_position = True
                previous_price = current_price  # Update previous price to current
        else:
            if current_price > sell_price_threshold:
                print(f"Price is above {sell_price_threshold:.2f}. Placing sell order.")
                place_sell_order(symbol, trade_quantity)
                in_position = False
                previous_price = current_price  # Update previous price to current

        time.sleep(3)  # Adjust sleep time as necessary

if __name__ == '__main__':
    trading_bot()
