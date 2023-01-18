# inflation-calculator
Calculates Polish złoty's value in given date including inflation and gets CPI in Poland for given date.

Example:
```
>>> from inflation import InflationCalculator
>>> from datetime import date
>>> calc = InflationCalculator()
>>> dates = date(2022, 12, 1), date(1981, 12, 1)
>>> calc.calculate_value(100, dates[0], dates[1])
31.9
>>> calc.get_cpi(dates[0])
0.3190467757735141
```
