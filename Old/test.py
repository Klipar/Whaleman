from pybit.unified_trading import WebSocket
from time import sleep
from easy.animations import LineProgresBar, SimpleAnimation

# Функція обробки повідомлень
def handle_message(message):
    print(message['topic'])

# Створення об'єкта WebSocket
ws = WebSocket(
    testnet=False,
    channel_type="linear",
)

def Subscribe ():
    
    coins = ["BTCUSDT", "ETHUSDT", "NOTUSDT"]  

    bar = LineProgresBar(MaxLength = 50, text = "Loading ", maxWalue = len(coins), isShowPersent = True, isShowWalue = True)

    for symbol in coins:
        ws.kline_stream(
            interval=1,
            symbol=symbol,
            callback=handle_message
        )
        bar.ShoveAndUpdate(1)



if __name__ == "__main__":
    # Subscribe()
    while True:
        sleep(1)
