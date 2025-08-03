#!/bin/bash

cleanup() {
    echo "\nStopping all process..."
    kill $!
    wait $!
}

clear

trap cleanup SIGINT SIGTERM

python3 telegramBotLauncher.py &

python3 tradingBotLauncher.py &

wait
