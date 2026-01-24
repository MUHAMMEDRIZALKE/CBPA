# 0001_currency_tabel_migration.py
#  This script is used to populate the currency table with data from pycountry
#  and babel libraries.

import pycountry
from babel.numbers import get_currency_precision, get_currency_symbol

from app.db.session import SessionLocal
from app.models.currency import Currency

currencies = []
for currency in pycountry.currencies:
    currencies.append(Currency(
        name=currency.name,
        code=currency.alpha_3,
        symbol=get_currency_symbol(currency.alpha_3, locale='en_US'),
        numeric_code=getattr(currency, "numeric", None), 
        minor_unit=get_currency_precision(currency.alpha_3)
    ))

with SessionLocal() as db:
    db.bulk_save_objects(currencies)
    db.commit()
