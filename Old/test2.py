from pybit.unified_trading import WebSocket
from time import sleep
ws = WebSocket(
    testnet=False,
    channel_type="linear",
)
def handle_message(message):
        print(message['data'][0]['close'])
ws.kline_stream(
    interval=1,
    symbol="ATOMUSDT",
    callback=handle_message
)
while True:
    sleep(1)