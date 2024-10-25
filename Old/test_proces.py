from multiprocessing import Process
from time import sleep
# Функція, яку будемо запускати в окремому процесі
def my_function():
    print("Процес виконується!")
    sleep(30)
    print("Процес завершився!")

# Створення нового процесу
process = Process(target=my_function)

# Запуск процесу
process.start()

# Очікування завершення процесу
process.join()
sleep(5)
process.terminate()
print("Процес")