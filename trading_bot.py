import time
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Replace with your Binance API credentials
API_KEY = 'A1CSEvDsRJoOWYXlCiK1IUIqxdE3dEnlC4Lb45OP9lY20SosaYeCmC1ht0NScTju'
API_SECRET = 'OpIReDJ4JeoOHu4bADL5Rs5hMxRIs6kpVKc06jJaTbFglIepa4rLWeWrdD5yAB8m'

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Define trading parameters
TRADE_SYMBOL = 'BTCUSDT'  # Trading BTC against USDT
BUY_DIP_PERCENTAGE = 0.0015 / 100  # Buy after a 1.1% dip
SELL_HIGH_PERCENTAGE = 2.5 / 100  # Sell after a 2.5% gain
TRADE_QUANTITY = 0.0001  # Quantity of BTC to trade

def get_price():
    """Get the current price of the specified trading symbol."""
    try:
        ticker = client.get_symbol_ticker(symbol=TRADE_SYMBOL)
        current_price = float(ticker['price'])
        print(f"Current Price: {current_price}")
        return current_price
    except BinanceAPIException as e:
        print(f"Error fetching price: {e}")
        return None

def place_buy_order(quantity, price):
    """Place a limit buy order."""
    try:
        return client.order_limit_buy(
            symbol=TRADE_SYMBOL,
            quantity=quantity,
            price=str(price)
        )
    except BinanceAPIException as e:
        print(f"Error placing buy order: {e}")
        return None

def place_sell_order(quantity, price):
    """Place a limit sell order."""
    try:
        return client.order_limit_sell(
            symbol=TRADE_SYMBOL,
            quantity=quantity,
            price=str(price)
        )
    except BinanceAPIException as e:
        print(f"Error placing sell order: {e}")
        return None

def run_trading_bot():
    last_price = get_price()
    if last_price is None:
        print("Failed to get the initial price. Exiting.")
        return
    
    print(f"Starting price: {last_price}")
    
    while True:
        current_price = get_price()
        if current_price is None:
            print("Failed to get current price. Retrying...")
            time.sleep(10)
            continue
        
        dip_price = last_price * (1 - BUY_DIP_PERCENTAGE)
        target_sell_price = last_price * (1 + SELL_HIGH_PERCENTAGE)
        
        if current_price <= dip_price:
            print(f"Dip detected! Buying at {current_price}")
            place_buy_order(TRADE_QUANTITY, current_price)
            bought_price = current_price
            last_price = bought_price  # Update last known price to bought price
            
            while True:
                current_price = get_price()
                if current_price is None:
                    print("Failed to get current price during sell waiting. Retrying...")
                    time.sleep(5)
                    continue
                
                if current_price >= bought_price * (1 + SELL_HIGH_PERCENTAGE):
                    print(f"Price target reached! Selling at {current_price}")
                    place_sell_order(TRADE_QUANTITY, current_price)
                    break
                
                time.sleep(5)  # Check every 5 seconds
            
            print("Trade completed. Restarting the strategy...")
        
        time.sleep(10)  # Check the price every 10 seconds

if __name__ == "__main__":
    run_trading_bot()
