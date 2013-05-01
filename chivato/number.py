#-*- coding: utf-8 -*-

from . import validators


class Number(object):
    """VAT Number parsing and validation """

    VALIDATORS = {
        'al': validators.albania,        'ar': validators.argentina,
        'at': validators.austria,        'be': validators.belgium,
        'bg': validators.bulgaria,       'cl': validators.chile,
        'co': validators.colombia,       'cy': validators.cyprus,
        'cz': validators.czech_republic, 'de': validators.germany,
        'dk': validators.denmark,        'ee': validators.estonia,
        'el': validators.greece,         'es': validators.Spain(),
        'fi': validators.finland,        'fr': validators.france,
        'gb': validators.united_kingdom, 'gr': validators.greece,
        'hr': validators.croatia,        'hu': validators.hungary,
        'ie': validators.ireland,        'it': validators.italy,
        'lt': validators.lithuania,      'lu': validators.luxembourg,
        'lv': validators.latvia,         'mt': validators.malta,
        'nl': validators.netherlands,    'pl': validators.poland,
        'pt': validators.portugal,       'ro': validators.romania,
        'ru': validators.russia,         'se': validators.sweden,
        'si': validators.slovenia,       'sk': validators.slovakia,
        'sm': validators.san_marino,     'ua': validators.ukraine,
        'uk': validators.united_kingdom
    }

    def validate(self, number, country=None, default=None):
        if not country:
            country, number = self.parse(number)

        if not country:
            country = default

        if not country:
            raise ValueError(u'Missing country code for "{}"'.format(number))

        validator = self.validator(number, country)

        return validator(number)

    def parse(self, number):
        code, vat = number[:2], number[2:]
        return (code, vat) if code.isalpha() else (None, number)

    def validator(self, number, country, validators=VALIDATORS):
        validator = validators.get(country.lower())

        if validator is None:
            raise ValueError(u'Unknown country code: "{}"'.format(country))

        return validator
