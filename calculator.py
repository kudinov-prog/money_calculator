import datetime as dt


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """ Добавляет новую запись о приёме пищи
        """

        self.records.append(record)

    def get_today_stats(self):
        """ Считает сколько денег потрачено/ калорий съедено за текущий день
        """

        date_now = dt.datetime.now().date()
        sum_today = sum([record.amount for record in self.records if
                         record.date == date_now])
        return sum_today
        
    def get_week_stats(self):
        """ Считает сколько денег потрачено/ калорий съедено за неделю
        """

        start = dt.datetime.now().date() - dt.timedelta(7)
        finish = dt.datetime.now().date()       
        sum_week = sum([record.amount for record in self.records if
                        start < record.date <= finish])
        return sum_week


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        """ Количество калорий, которые можно/нужно получить сегодня
        """

        today_stats = self.get_today_stats()

        if  today_stats < self.limit:
            diff = self.limit - today_stats
            return ('Сегодня можно съесть что-нибудь ещё, '
                   f'но с общей калорийностью не более {diff} кКал')

        elif today_stats >= self.limit:
            return 'Хватит есть!'
        
       
class CashCalculator(Calculator):
    USD_RATE = 60.55
    EURO_RATE = 70.25
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        """ Количество денег, которые можно потратить сегодня в рублях,
            долларах или евро
        """
        
        curr_dict = {'rub': (self.RUB_RATE, 'руб'),
                     'usd': (self.USD_RATE, 'USD'),
                     'eur': (self.EURO_RATE, 'Euro')}

        curr_rate, curr_name = curr_dict[currency]
        today_stats = self.get_today_stats()
        diff_less = (self.limit - today_stats)/curr_rate
        diff_more = (today_stats - self.limit)/curr_rate

        if today_stats == self.limit:
            return 'Денег нет, держись'

        elif today_stats < self.limit:
            return f'На сегодня осталось {diff_less:.2f} {curr_name}'
        
        elif today_stats > self.limit:
            return ('Денег нет, держись: твой долг - '
                        f'{diff_more:.2f} {curr_name}')




calcalc1 = CaloriesCalculator(1000)
calcalc1.add_record(Record(amount= 200, date= '29.04.2020', comment= 'not bad'))
calcalc1.add_record(Record(amount= 300, date= '06.04.2020', comment= 'bad'))
calcalc1.add_record(Record(amount= 700, comment= 'apple'))
calcalc1.add_record(Record(amount= 600, date= '25.04.2020', comment= 'vine'))

print(calcalc1.get_today_stats())
print(calcalc1.get_calories_remained())


cashcalc2 = CashCalculator(2000)
cashcalc2.add_record(Record(amount= 1950, comment= 'dinner'))
cashcalc2.add_record(Record(amount= 500, date= '29.04.2020', comment= 'metro'))

print(cashcalc2.get_today_stats())
print(cashcalc2.get_today_cash_remained('rub'))
print(calcalc1.get_week_stats())
