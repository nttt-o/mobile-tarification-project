# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 20:31:18 2021

@author: Osina N.
"""
import math
from datetime import datetime

EVENT_TOPUP = 0
EVENT_ROAM_IN = 1
EVENT_ROAM_OUT = 2
EVENT_CALL_IN = 10
EVENT_CALL_OUT = 11
EVENT_SMS_IN = 20
EVENT_SMS_OUT = 21
EVENT_INTERNET = 30

# attribute positions for events
EV_TIME = 0
EV_EVENT = 1
EV_PAYMENT = 2
EV_PHONE = 2
EV_Mb = 2
EV_DURATION = 3
EV_TEXT = 3
EV_SUMMA_RUB = -1

# attribute positions for event_info
EI_PRINT_STR = 0
EI_GET_VALUES_FUNC = 1
EI_TOTALS = 2

# tariffs
PRICE_CALL_IN_HOME = 0
PRICE_CALL_IN_ROAM = 8
PRICE_CALL_OUT_HOME = 2
PRICE_CALL_OUT_ROAM = 20

PRICE_SMS_IN_HOME = 0
PRICE_SMS_IN_ROAM = 0
PRICE_SMS_OUT_HOME = 1
PRICE_SMS_OUT_ROAM = 5

PRICE_INTERNEI_HOME = 0.2
PRICE_INTERNEI_ROAM = 5

# tariff conditions
FREE_CALL_SEC = 3
ROUNDBASE_FOR_SMS = 70
ROUNDBASE_FOR_CALL = 60


def load_data():

    # EVENT_TOPUP (0): time, event, payment
    # EVENT_ROAM_IN (1): time, event
    # EVENT_ROAM_OUT (2): time, event
    # EVENT_CALL_IN (10): time, event, phone, duration
    # EVENT_CALL_OUT (11): time, event, phone, duration
    # EVENT_SMS_IN (20): time, event, phone, text
    # EVENT_SMS_OUT (21): time, event, phone, text
    # EVENT_INTERNET (30): time, event, Mb

    list_of_events = [
            ['05-01-2020 21:17:29', 0, 500.00],
            ['06-01-2020 08:10:13', 10, '+79261112233', 78],
            ['06-01-2020 08:10:33', 10, '+79261112233', 18],
            ['06-01-2020 14:16:01', 20, '+79106541234', 'Перезвони мне'],
            ['08-02-2020 09:27:21', 11, '+79106541234', 240],
            ['10-02-2020 23:00:01', 21, '+79106541234', 'Опять созвон'],
            ['01-03-2020 11:07:12', 1],
            ['09-03-2020 20:11:19', 10, '+79261112233', 40],
            ['11-04-2020 02:10:10', 30, 10],
            ['11-04-2020 13:17:01', 20, '+79106541234', 'Я уже устала'],
            ['11-04-2020 19:17:29', 0, 100.00],
            ['12-04-2020 20:05:49', 2],
            ['13-05-2020 21:10:12', 11, '+79106541234', 2],
            ['14-05-2020 02:10:10', 30, 256],
            ['15-05-2020 23:31:34', 1],
            ['16-06-2020 16:45:57', 21, '+79106541555', 'С днем рождения поздравляю и желаю день за днем быть счастливее и ярче, словно солнце за окном'],
            ['20-07-2020 01:00:21', 11, '+79106541234', 3],
            ['21-07-2020 09:27:21', 11, '+79106541234', 150]
      ]
    return list_of_events


def calculate(events, date_start, date_end):

    def get_call_values(event_, roam_):

        if event_[EV_EVENT] == EVENT_CALL_IN:
            mins = math.ceil(event_[EV_DURATION]/ROUNDBASE_FOR_CALL)
            cost = mins * \
                (PRICE_CALL_IN_ROAM if roam_ else PRICE_CALL_IN_HOME)
            return (1, mins, cost)

        else:
            if event[EV_DURATION] <= FREE_CALL_SEC:
                return (1, 0, 0)
            else:
                mins = math.ceil(event[EV_DURATION]/ROUNDBASE_FOR_CALL)
                cost = mins * \
                    (PRICE_CALL_OUT_ROAM if roam else PRICE_CALL_OUT_HOME)
                return (1, mins, cost)

    def get_sms_values(event_, roam_):

        if event_[EV_EVENT] == EVENT_SMS_IN:
            return (1, math.ceil(len(event_[EV_TEXT])/ROUNDBASE_FOR_SMS) *
                    (PRICE_SMS_IN_ROAM if roam_ else PRICE_SMS_IN_HOME))

        else:
            cnt = math.ceil(len(event_[EV_TEXT])/ROUNDBASE_FOR_SMS)
            return (cnt,  cnt *
                    (PRICE_SMS_OUT_ROAM if roam_ else PRICE_SMS_OUT_HOME))

    def get_internet_values(event_, roam_):
        return (event_[EV_Mb], event[EV_Mb] *
                (PRICE_INTERNEI_ROAM if roam_ else PRICE_INTERNEI_HOME))

    # event_info = {key: value} contains all information about each line in report
    # key =  (event, roam)
    # value = [
    #        string to print in report,
    #        function to calculate event values,
    #        event totals
    #    ]
    # Note: the last item in event totals is always "sum in rubles"

    event_info = {

        (EVENT_CALL_IN, False):
            ['Входящие звонки (домашняя сеть): {}, общая продолжительность: {} мин, списано: {:.2f} руб',
             get_call_values, [0, 0, 0]],

        (EVENT_CALL_IN, True):
            ['Входящие звонки (роуминг): {}, общая продолжительность: {} мин, списано: {:.2f} руб',
             get_call_values, [0, 0, 0]],

        (EVENT_CALL_OUT, False):
            ['Исходящие звонки (домашняя сеть): {}, общая продолжительность: {} мин, списано: {:.2f} руб',
             get_call_values, [0, 0, 0]],

        (EVENT_CALL_OUT, True):
            ['Исходящие звонки (роуминг): {}, общая продолжительность: {} мин, списано: {:.2f} руб',
             get_call_values, [0, 0, 0]],

        (EVENT_SMS_IN, False):
            ['Входящие сообщения (домашняя сеть): {}, списано: {:.2f} руб',
             get_sms_values, [0, 0]],

        (EVENT_SMS_IN, True):
            ['Входящие сообщения (роуминг): {}, списано: {:.2f} руб',
             get_sms_values, [0, 0]],

        (EVENT_SMS_OUT, False):
            ['Исходящие сообщения (домашняя сеть): {}, списано: {:.2f} руб',
             get_sms_values, [0, 0]],

        (EVENT_SMS_OUT, True):
            ['Исходящие сообщения (роуминг): {}, списано: {:.2f} руб',
             get_sms_values, [0, 0]],

        (EVENT_INTERNET, False):
            ['Мобильный интернет (домашняя сеть): {} Мб, списано: {:.2f} руб',
             get_internet_values, [0, 0]],

        (EVENT_INTERNET, True):
            ['Мобильный интернет (роуминг): {} Мб, списано: {:.2f} руб',
             get_internet_values, [0, 0]],
         }

    roam = False  # roaming state, the initial value is False
    total_debet = 0  # sum of debet operations
    total_kredit = 0  # sum of payment operations

    for event in events:
        # keep current roaming state
        if event[EV_EVENT] == EVENT_ROAM_IN:
            roam = True
            continue
        elif event[EV_EVENT] == EVENT_ROAM_OUT:
            roam = False
            continue

        # process each event in range of [date_start; date_end]
        ev_date = datetime.strptime(event[EV_TIME], '%d-%m-%Y %H:%M:%S').date()

        if date_start <= ev_date <= date_end:
            if event[EV_EVENT] == EVENT_TOPUP:
                total_kredit += event[EV_PAYMENT]  # add payment
                continue

            key = (event[EV_EVENT], roam)
            func = event_info[key][EI_GET_VALUES_FUNC]
            event_values = func(event, roam)  # get event values

            for i, val in enumerate(event_values):
                event_info[key][EI_TOTALS][i] += val  # add event values to event totals

            total_debet += event_values[EV_SUMMA_RUB]  # add SUMMA_RUB to total_debet

    # make report
    output = f'Общая сумма пополнения: {total_kredit:.2f} руб\n'
    output += f'Общая сумма расходов: {total_debet:.2f} руб\n'
    output += 'Детализация расходов:\n'

    for val in event_info.values():
        output += val[EI_PRINT_STR].format(*val[EI_TOTALS]) + '\n'
    return output


# make mobile tarification report
while s := input('Введите начальную дату (ДД.ММ.ГГГГ): '):
    try:
        start_date = datetime.strptime(s, '%d.%m.%Y').date()
    except ValueError:
        print('Некорректная дата')
        continue
    while True:
        s = input('Введите конечную дату (ДД.ММ.ГГГГ): ')
        try:
            end_date = datetime.strptime(s, '%d.%m.%Y').date()
        except ValueError:
            print('Некорректная дата')
        else:
            break
    if start_date > end_date:
        print('Период указан некорректно')
    else:
        events_data = load_data()
        if start_date > datetime.strptime(events_data[-1][EV_TIME], '%d-%m-%Y %H:%M:%S').date() or \
           end_date < datetime.strptime(events_data[0][EV_TIME], '%d-%m-%Y %H:%M:%S').date():
            print('Данные не найдены')
        else:
            report = calculate(events_data, start_date, end_date)
            print(report)
