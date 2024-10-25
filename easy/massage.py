from colorama import init, Fore, Style
import datetime

def Beautiful_Timestump () -> str:
    return datetime.datetime.now().strftime("[%H:%M:%S]")

init()
def failed(str, en = "\n"):
    print(Beautiful_Timestump (), Fore.RED + ' [FAILED]  ' + Style.RESET_ALL, str, end = en)
    return (f"{Beautiful_Timestump ()} [FAILED] {str}")


def success (str, en = "\n"):
    print(Beautiful_Timestump (), Fore.GREEN + ' [SUCCESS] ' + Style.RESET_ALL, str, end = en)
    return (f"{Beautiful_Timestump ()} [SUCCESS] {str}")

def inform(str, en = "\n"):
    print(Beautiful_Timestump (), Fore.BLUE + ' [INFORM]  ' + Style.RESET_ALL, str, end = en)
    return (f"{Beautiful_Timestump ()} [INFORM] {str}")

def warn(str, en = "\n"):
    print(Beautiful_Timestump (), Fore.YELLOW + ' [ WARN ]  ' + Style.RESET_ALL, str, end = en)
    return (f"{Beautiful_Timestump ()} [WARN] {str}")

def pr(str, en = "\n"):
    print(Beautiful_Timestump (),' [PRINT]   ' , str)
    return (f"{Beautiful_Timestump ()} [PRINT] {str}")

def test(str, en = "\n"):
    print(Fore.MAGENTA + f"{Beautiful_Timestump ()}  [ TEST ]  " + Style.RESET_ALL, str, end = en)
    return (f"{Beautiful_Timestump ()} [TEST] {str}")
