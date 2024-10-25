from easy.massage import failed, success, inform, warn, test, pr

def Checking_turnover (conf, Bybit, data, coin):     # перевірка на наявність достатньо високих обємів торгів. Потім додати коофіцієнт часу.
    
    average = float(calculate_average(data))
    if (conf.get_value(parameter1="exchange",parameter2="Treyd", parameter3="time factor for trading turnover") == "linear"):
        average = (average*(coin.Curent_Candle_Time/(Bybit.Candel_time*60000)))
    if (((float(data[0])/average)*100) > float(conf.get_value(parameter1="exchange",parameter2="Treyd", parameter3="Triger turnover persent"))):
        return 0
    return 1


def Checking_the_rate_of_price_change(conf, Bybit, coin):
    List_of_TRIGER_persents = (conf.get_value(parameter1="exchange",parameter2="Treyd", parameter3="cendel minimal move persents"))
    # print ("Checking_the_rate_of_price_change", end = "")
    # print (List_of_TRIGER_persents)
    for i in range (0, len(List_of_TRIGER_persents)):
        dif = persent_mowe(float(coin.List_of_walues[0][i+1]), float(coin.List_of_walues[3][0]))
        if (dif > 0):
            if (dif > float(List_of_TRIGER_persents[i])):
                test (f"{dif} ?? {float(List_of_TRIGER_persents[i])}")
                success ("TRY Sell")
                Bybit.Try_Plase_Order(coin, "Sell")
        else:
            if (dif*(-1) > float(List_of_TRIGER_persents[i])):
                test (f"{dif} ?? {float(List_of_TRIGER_persents[i])}")
                success ("TRY BUY")
                Bybit.Try_Plase_Order(coin, "Buy")
        



def calculate_average(data):
        total = 0
        for i in data:    
            total += float(i)
        return (float(total) / len(data))
def persent_mowe(a, b):
    # a --> b
    # якщо + то ціна піднялася, - то упала
    if a == 0:
        failed("A cant be zero.")
        exit()
    return ((b - a) / a) * 100
def My_Bool (test):
    if (test == "True"):
        return True
    return False

def CONDIRION (conf, Bybit, coin):
    if(Checking_turnover (conf, Bybit, coin.List_of_walues[4], coin)): return 0 # перевірка достатніх обємів торгів
    # success(f"TURNOVER of {coin.Coin} = {coin.Curent_Candle_Time}")
    Checking_the_rate_of_price_change (conf, Bybit, coin)
    # if(not My_Bool(conf.get_value(parameter1="exchange",parameter2="Treyd", parameter3="Only Buy"))):
    #     test ("TEST_Sell")
    # elif (not My_Bool(conf.get_value(parameter1="exchange",parameter2="Treyd", parameter3="Only Sell"))):
    #     test ("TEST_Buy")

    return 0
    print("")
