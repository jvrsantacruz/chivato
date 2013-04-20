#-*- coding: utf-8 -*-

__version__ = '0.0.1'

from . import staticdata, validators


def countries():
    '''Return the list of country codes that have check function'''
    return staticdata.COUNTRIES


VALIDATORS = {
    'al': validators.albania,        'ar': validators.argentina,
    'at': validators.austria,        'be': validators.belgium,
    'bg': validators.bulgaria,       'cl': validators.chile,
    'co': validators.colombia,       'cy': validators.cyprus,
    'cz': validators.czech_republic, 'de': validators.germany,
    'dk': validators.denmark,        'ee': validators.estonia,
    'el': validators.greece,         'es': validators.spain,
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


def parse_vat(vat):
    code, number = vat[:2], vat[2:]
    return code.lower(), number


def check_vat(vat, parser=parse_vat, validators=VALIDATORS):
    code, number = parser(vat)

    checker = validators.get(code)

    if checker is None:
        return False

    return checker(number)
