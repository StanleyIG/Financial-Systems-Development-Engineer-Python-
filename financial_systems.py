"""
Тестовое задание на ваĸансию "Инженерразработчиĸ по финансовым системам (Python)"
1. Реализовать итератор по данной UML-диаграмме:
UML-диаграмма
returns
InterestInput
+period: int
+date1: date
+date2: date
+withdraw: Decimal
+max_return: Decimal
+rate: Decimal
InterestIterator
-withdraw: dict[int,Decimal]
-max_return: dict[int,Decimal]
-rate: Decimal
-dates: dict[int,date]
+__iter__() : Iterator
+__next__() : InterestInput
Описание параметров
Итератор получает на вход:
Параметр Смысл
withdraw Суммы, ĸоторые получает ĸлиент по ĸредиту в соответствующем периоде
max_return Маĸс сумма, ĸоторую ĸлиент может вернуть в соответствующем периоде
rate Ставĸа ĸредита
dates Даты платежей по ĸредиту
InterestInput содержит следующее:
Параметр Смысл
period Номер периода
date1 Дата начала периода
date2 Дата ĸонца периода
withdraw Сумма, ĸоторую получает ĸлиент по ĸредиту в данном периоде
max_return Маĸс сумма, ĸоторую ĸлиент может вернуть в данном периоде
rate Ставĸа ĸредита
Доп.условия
• Атрибуты InterestInput должны быть доступны через десĸриптор
• Итератор должен использовать ĸаĸ можно меньше памяти
Данные для теста
Данный ввод:
deposit = {
 3: Ruble(100),
 4: Ruble(0),
 5: Ruble(0)
}
max_withdraw = {
 3: Ruble(40),
 4: Ruble(40),
 5: Ruble(40)
}
rate = Decimal('0.1')
dates = {
 3: Date(2023, 1, 10),
 4: Date(2023, 2, 10),
 5: Date(2023, 3, 10)
}
в сочетании с:
interest_iter = IterestIterator(deposit, max_withdraw, rate, dates)
for row in interest_iter:
 print(row)
должен вернуть построчно в виде <InterestInput>:
period date1 date2 deposit max_withdraw rate
3 2023-01-10 2023-02-10 100.00 40.00 0.1
4 2023-02-10 2023-03-10 0.00 40.00 0.1
5 2023-03-10 2023-03-10 0.00 40.00 0.1
2. Написать сĸрипт, формирующий таблицу pandas.DataFrame
Выходная таблица представляет собой графиĸ погашения ĸредита:
period date1 date2 deposit max_withdraw rate balance interest payment
period date1 date2 deposit max_withdraw rate balance interest payment
1 2023-01-10 2023-02-10 100.00 40.00 0.1 100.00 0.85 40.00
2 2023-02-10 2023-03-10 0.00 40.00 0.1 60.85 0.47 40.00
3 2023-03-10 2023-04-10 0.00 40.00 0.1 21.32 0.18 21.50
4 2023-04-10 2023-04-10 0.00 0.00 0.1 0.00 0.00 0.00
• Входные данные совпадают с заданием’ 1.
• Можно использовать итератор из задания 1.
• Столбцы balance, interest и payment должны быть рассчитаны внутри сĸрипта.
• Проценты считаются исходя из 365 дней в году.
• Сначала происходит погашение процентов, затем основного долга.
• Решение, использующее релевантные паттерны-программирования, получит доп.баллы.
"""

from decimal import Decimal
from datetime import date
import pandas as pd



class Ruble:
    def __init__(self, amount):
        self.amount = amount

    def __repr__(self):
        return f'{self.amount}'


class Date:
    def __init__(self, year, month, day):
        self.date = date(year, month, day)

    def __repr__(self):
        return str(self.date)
    

"""класс дескриптор"""
class InterestInputDescriptor:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
         if self.name == 'deposit' and value < 0:
             raise ValueError(f"{self.name} не может быть отрицательным")
         if self.name == 'max_withdraw' and value < 0:
             raise ValueError(f"{self.name} не может быть отрицательным")
         instance.__dict__[self.name] = value


class InterestInput:
    period = InterestInputDescriptor('period')
    date1 = InterestInputDescriptor('date1')
    date2 = InterestInputDescriptor('date2')
    deposit = InterestInputDescriptor('deposit')
    max_withdraw = InterestInputDescriptor('max_withdraw')
    rate = InterestInputDescriptor('rate')
    balance = InterestInputDescriptor('balance')
    interest = InterestInputDescriptor('interest')
    payment = InterestInputDescriptor('payment')
    

    def __init__(self, period, date1, date2, deposit, max_withdraw, rate, balance, interest, payment):
        self.period = period
        self.date1 = date1
        self.date2 = date2
        self.deposit = deposit
        self.max_withdraw = max_withdraw
        self.rate = rate
        self.balance = balance
        self.interest = interest
        self.payment = payment


"""класс итератор использует встроенный метод python __iter__ и __next__"""
class InterestIterator:
    def __init__(self, deposit, max_withdraw, rate, dates):
        self.deposit = deposit
        self.max_withdraw = max_withdraw
        self.rate = rate
        self.dates = dates
        self.current_period = min(dates.keys()) # объявляю текущий период
        self.current_balance = deposit[self.current_period].amount # объявляю текущий баланс, т.к. расчёт баланса должен начинаться сл следующего месяца от снятия депозита
       


    def __iter__(self):
        return self

    def __next__(self):
        if self.current_period > max(self.dates.keys()): # проверка значения текущего периодв, если оно выше чем максимальное значение в словаре dates, то итерация завершается
            raise StopIteration
        period = self.current_period # теущий период
        date1 = self.dates[period].date # дата1, первая дата текщего периода
        date2 = self.dates.get(period + 1, self.dates[period]).date # конечная дата текущего периода
        deposit = self.deposit.get(period, Ruble(0)).amount # сумма кредита
        max_withdraw = self.max_withdraw.get(period, Ruble(0)).amount # Маĸс сумма, ĸоторую ĸлиент может вернуть в соответствующем периоде
        rate = self.rate # процентная ставка
        days = (date2 - date1).days # дельта, колличество дней за текущий период(колличество дней между дата1 и дата2)
        balance = self.current_balance - max_withdraw # баланс, остаток д/с на счёте клиента.
        interest = balance * rate * days / 365 # интерес банка, начисленные проценты на баланс за определённый период
        payment = min(balance + interest, max_withdraw) # минимальная сумма выплат, которую клиент может выплатить банку. 
        # клиент должен выплтить либо максимальную сумму снятия, либо балан + интерес банка в заисимости что будет меньше.
        # если сумма снятия больше чем баланс + интерес, то задолженность переносится на следующий период.
        """
        Банк начисляет проценты на остаток денежных средств на счете клиента за текущий период. 
        Если клиент снимает деньги с баланса, то остаток денежных средств на счете уменьшается, и начисленные 
        проценты также уменьшаются. Если клиент не снимает деньги с баланса, то остаток денежных 
        средств на счете остается неизменным, и начисленные проценты будут больше.
        """

        if self.current_period == min(self.dates.keys()):
            balance = deposit
            interest = self.current_balance * rate * days / 365
        elif days == 0 or days is None:
            balance = 0

        self.current_balance = balance + interest
        self.current_period += 1


        return InterestInput(period, date1, date2, deposit, max_withdraw, rate, balance, interest, payment)
    
    

"""продолжаю философию класса итератора InterestIterator"""    
class AddPandas(InterestIterator):
    def to_dataframe(self):
        data = []
        for input_object in self:
            data.append({
                'period': input_object.period,
                'date1': input_object.date1,
                'date2': input_object.date2,
                'deposit': input_object.deposit,
                'max_withdraw': input_object.max_withdraw,
                'rate': input_object.rate,
                'balance': round(input_object.balance, 2),
                'interest': round(input_object.interest, 2),
                'payment': round(input_object.payment, 2)
            })
        return pd.DataFrame(data) 


deposit = {
    1: Ruble(100),
    2: Ruble(0),
    3: Ruble(0),
    4: Ruble(0)
}
max_withdraw = {
    1: Ruble(40),
    2: Ruble(40),
    3: Ruble(40),
    4: Ruble(0)
}
rate = Decimal('0.1')
dates = {
    1: Date(2023, 1, 10),
    2: Date(2023, 2, 10),
    3: Date(2023, 3, 10),
    4: Date(2023, 4, 10)
}

interest_iter = InterestIterator(deposit, max_withdraw, rate, dates)
print('period date1 date2 deposit max_withdraw rate balance interest payment')
for row in interest_iter:
    print(row.period, row.date1, row.date2, row.deposit, row.max_withdraw, row.rate, round(row.balance, 2), round(row.interest, 2), round(row.payment, 2))

print()
print(32*'*')
print('pandas')
print()

"""т.к. наследуюсь от класса "итератора", то передаю в класс AddPandas все необходимые атрибуты"""
add_pandas = AddPandas(deposit, max_withdraw, rate, dates)
# Получаю pandas DataFrame
df = add_pandas.to_dataframe()

# Вывожу DataFrame
print(df)