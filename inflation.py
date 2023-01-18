from datetime import date

class InflationCalculator():
    def __init__(self):
        """
        Calculates Polish złoty's value in given date including inflation and gets CPI in Poland for given date.
        """
        from requests import get
        from csv import reader
        data, final_data = {}, {}
        url = 'https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultstronaopisowa/4741/1/1/miesieczne_wskazniki_cen_towarow_i_uslug_konsumpcyjnych_od_1982_roku.csv'
        content = get(url).content.decode('windows-1250').replace(',', '.').replace(';', ',')
        lines = list(reader(content.split('\n')))[1:-1]
        for record in lines:
            _, _, method, year, month, value, _, _, _ = record
            if method != 'Poprzedni miesiąc = 100': continue
            record_date = date(int(year), int(month), 1)
            data[record_date] = float(value)
        data[date(1995, 1, 1)] = 0.01041
        self.__first_date = date(1981, 12, 1)
        data[self.__first_date] = 100
        previous = 1.0
        for record_date, value in sorted(data.items()):
            final_data[record_date] = (value * previous) / 100
            previous = final_data[record_date]
        self.__last_date = list(final_data.keys())[-1]
        self.__data = final_data

    def get_cpi(self, amount_date: date) -> float:
        """
        Returns CPI for given date compared to CPI in December 1981 (1).
        :param amount_date: CPI value's date.
        :return: CPI for given date compared to CPI in December 1981 (1).
        """
        if amount_date < self.__first_date or amount_date > self.__last_date:
            raise Exception(f'Date must not be before {self.__first_date} or after {self.__last_date}')
        proper_date = date(amount_date.year, amount_date.month, 1)
        return self.__data.get(proper_date)

    def calculate_value(self, amount: float, value_date: date, compared_date: date) -> float:
        value_date_cpi, compared_date_cpi = self.get_cpi(value_date), self.get_cpi(compared_date)
        return round(amount * (value_date_cpi / compared_date_cpi), 2)
