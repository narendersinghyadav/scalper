from datetime import datetime
import matplotlib.pyplot as plt
# #when heartbeat fail try running code immdeiatly
#live order placing also added supertrend
import talib
import numpy as np

today_date = "05/04/2021 14:55" #update this
filename = "nifty5apr.txt"
EMA21 =None
EMA13=None
flag_ce = 0
bought_price_ce = 0
sum_ce = 0
portfolio = 60000
portfolio_day = 60000
quantity_ce = 0
x_list_ce = []
buy_x_list_ce = []
sell_x_list_ce = []
buy_y_list_ce = []
sell_y_list_ce = []

open_price_ce = []
high_price_ce = []
low_price_ce = []
close_price_ce = []
take_trade = True
print("Current Portfolio @ ", portfolio)
price_list_ce = []
price_list_pe = []
last_date = None
count2 = 0
x_list = []
placed_order = -1
placed_order_id = 0


stoploss_ce = 0
stoploss_pe =0

buy_ce_index = 0
buy_pe_index =0

count1_ce = 0
count1_pe = 0
lot_size = 75
high_price= 0
can_take_trade = True
def calculate_one_minute_data(price_ce, date_time):
    global last_date, x_list, count2, x_list_pe, x_list_ce, last_second_ce, last_second_pe, last_minute_ce,can_take_trade,flag_ce,portfolio,sum_ce,stoploss_ce
    global price_list_ce, price_list_pe, open_price_pe, open_price_ce, close_price_pe, close_price_ce, high_price_ce, high_price_pe, low_price_pe, low_price_ce,placed_order
    if last_date is None:
        last_date = date_time
    elif (datetime.strptime(str(date_time.hour)+" "+ str(int((date_time.minute)/5)),"%H %M") > datetime.strptime(str(last_date.hour)+" "+ str(int((last_date.minute)/5)),"%H %M"))  and len(price_list_ce) > 0 :
        # print(date_time ," ",price_list_pe)
        # print(last_date,price_list_ce[0], max(price_list_ce),min(price_list_ce), price_list_ce[-1])
        last_date = date_time
        placed_order -=1
        if price_ce !=0:
            price_list_ce.append(price_ce)
        open_price_ce.append(price_list_ce[0])
        close_price_ce.append(price_list_ce[-1])
        high_price_ce.append(max(price_list_ce))
        low_price_ce.append(min(price_list_ce))
        count2 += 1
        x_list_ce.append(count2)
        price_list_ce = []
        price_list_pe = []
        last_second_ce = -1
        last_minute_ce =-1
        can_take_trade = True
        if flag_ce == 1:
            high_price = 0
            flag_ce = 0
            sell_price = close_price_ce[-1]
            print(sell_price, " limit hit", index)
            sell_x_list_ce.append(count2)
            sell_y_list_ce.append(sell_price)
            portfolio = portfolio + (sell_price * quantity_ce * lot_size)
            portfolio -= quantity_ce * bought_price_ce * lot_size * 0.004
            sum_ce += sell_price * quantity_ce * lot_size
            print("Current Portfolio @ ", portfolio)
    else:
        if price_ce != 0.0 :
            price_list_ce.append(price_ce)
            last_second_ce = date_time.second
            last_minute_ce = date_time.minute

def trade(price_ce, index):
    global flag_ce, bought_price_ce, sum_ce, count1_ce, quantity_ce, x_list_ce, buy_y_list_ce, buy_x_list_ce, sell_y_list_ce, sell_x_list_ce
    global lot_size, portfolio,count1_ce,high_price,can_take_trade,EMA21,EMA13
    # EMA21 = talib.EMA(np.array(close_price_ce), 21)
    # EMA13 = talib.EMA(np.array(close_price_ce), 13)
    if price_ce != 0.0 and len(open_price_ce)>2 :
        if flag_ce == 0 and  price_ce> high_price_ce[-1] and open_price_ce[-1]*0.99 <= low_price_ce[-1] and high_price_ce[-1]*0.99 <= close_price_ce[-1] and open_price_ce[-1]< close_price_ce[-1] and can_take_trade:
            can_take_trade = False
            bought_price_ce = float(price_ce)
            quantity_ce = int(portfolio / (bought_price_ce * lot_size))
            if (quantity_ce > 0) and bought_price_ce >= 10 :
                high_price = bought_price_ce
                flag_ce = 1
                count1_ce += 1
                print(bought_price_ce, " buy PUT", index)
                buy_x_list_ce.append(count2)
                buy_y_list_ce.append(bought_price_ce)
                print("LOT size @75, #oopen_price_cef lot-> ", quantity_ce)
                sum_ce -= bought_price_ce * quantity_ce * lot_size
                portfolio = portfolio - bought_price_ce * quantity_ce * lot_size
                print("Current Portfolio @ ", portfolio)

        elif flag_ce == 1 and  price_ce > bought_price_ce*1.03:
            high_price = 0
            flag_ce = 0
            sell_price = price_ce
            print(sell_price, " sell CALL", index)
            sell_x_list_ce.append(count2)
            sell_y_list_ce.append(sell_price)
            portfolio = portfolio + (sell_price * quantity_ce * lot_size)
            portfolio -= quantity_ce*bought_price_ce*lot_size*0.004
            sum_ce += sell_price * quantity_ce * lot_size
            print("Current Portfolio @ ", portfolio)
        elif flag_ce == 1 and  price_ce < bought_price_ce*0.94:
            high_price = 0
            flag_ce = 0
            sell_price = price_ce
            print(sell_price, " limit hit", index)
            sell_x_list_ce.append(count2)
            sell_y_list_ce.append(sell_price)
            portfolio = portfolio + (sell_price * quantity_ce * lot_size)
            portfolio -= quantity_ce*bought_price_ce*lot_size*0.004
            sum_ce += sell_price * quantity_ce * lot_size
            print("Current Portfolio @ ", portfolio)
        elif flag_ce == 1:
            high_price = max(price_ce,high_price)


with open(filename, 'r') as file:
    for line in file.readlines():
        data = line.split(" ")
        date_time = data[2]+" "+data[3][:-1]
        price_ce, price_pe = data[0],data[1]
        # date_time = line.split(",")[1][:-1]
        # price_ce,price_pe = line.split(",")[0].split(" ")
        dateTimeObject = datetime.strptime(date_time, "%d/%m/%Y %H:%M:%S")
        if(dateTimeObject >datetime.strptime(today_date, "%d/%m/%Y %H:%M")):
            print("out of trade")
            if flag_ce == 1:
                # SELL
                flag_ce = 0  # selling
                print(open_price_ce[index], " squareOff call ")
                sell_x_list_ce.append(index)
                sell_y_list_ce.append(open_price_ce[index])
                portfolio = portfolio + (open_price_ce[index] * quantity_ce * lot_size)
                portfolio -= 200
                sum_ce += open_price_ce[index] * quantity_ce * lot_size
                print("Current Portfolio @ ", portfolio)
            take_trade = False
            if flag_ce == 0:
                break
        calculate_one_minute_data(float(price_ce), dateTimeObject)
        # print(datetime.strptime("03:00", "%H:%M").time())
        index = count2 - 1
        if len(open_price_ce) == 0 :
            continue
        trade(float(price_ce),index)
#Assign the callbacks.
print()
print("# of trade on CALL ", count1_ce)
plt.plot(x_list_ce,open_price_ce)
plt.plot(x_list_ce, close_price_ce)
# plt.plot(x_list_ce, EMA21)
# plt.plot(x_list_ce, EMA13)
#plt.plot(x_list_ce, RSI_ce)
plt.plot(buy_x_list_ce, buy_y_list_ce, 'o', color='green')
plt.plot(sell_x_list_ce, sell_y_list_ce, 'o', color='red')
plt.show()
plt.show()
# removing brokerage
print("portfolio P&L @ Rupee", portfolio - portfolio_day)
if (portfolio - portfolio_day >= 0):
    print("Wohoo! your bot did the job for you, today's return +",
          ((portfolio - portfolio_day) / portfolio_day) * 100), "%"
else:
    print("Next Time! your bot need to try harder, today's return ",
          ((portfolio - portfolio_day) / portfolio_day) * 100), "%"
