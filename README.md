# trader_python

**Аргументи запуску файлу:**
- RATE – отримання поточного курсу (USD/UAH)
- AVAILABLE - отримання залишків за рахунками
- BUY XXX - покупка xxx доларів. За відсутності гирвень для покупки виводить повідомлення типу UNAVAILABLE, REQUIRED BALANCE UAH 2593.00, AVAILABLE 1000.00
- SELL XXX - продаж доларів. У разі відсутності доларів для продажу виводить повідомлення типу UNAVAILABLE, REQUIRED BALANCE USD 200.00, AVAILABLE 135.00
- BUY ALL – купівля доларів на всі можливі гривні.
- SELL ALL - продаж всіх доларів.
- NEXT – отримати наступний курс
- RESTART - розпочати гру з початку (з початковими умовами)
- HISTORY - історія операцій

**Приклад використання:**

>>>python trader.py NEXT

>>>python trader.py SELL 100

>>>py trader.py NEXT (for Windows)
 
