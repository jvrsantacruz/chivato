#-*- coding: utf-8 -*-

__version__ = '0.0.1'

from . import staticdata, validators


def countries():
    ''' Return the list of country codes that have check function '''
    return staticdata.COUNTRIES


VALIDATORS = {
    'al': validators.check_vat_al, 'ar': validators.check_vat_ar,
    'at': validators.check_vat_at, 'be': validators.check_vat_be,
    'bg': validators.check_vat_bg, 'cl': validators.check_vat_cl,
    'co': validators.check_vat_co, 'cy': validators.check_vat_cy,
    'cz': validators.check_vat_cz, 'de': validators.check_vat_de,
    'dk': validators.check_vat_dk, 'ee': validators.check_vat_ee,
    'el': validators.check_vat_el, 'es': validators.check_vat_es,
    'fi': validators.check_vat_fi, 'fr': validators.check_vat_fr,
    'gb': validators.check_vat_gb, 'gr': validators.check_vat_gr,
    'hr': validators.check_vat_hr, 'hu': validators.check_vat_hu,
    'ie': validators.check_vat_ie, 'it': validators.check_vat_it,
    'lt': validators.check_vat_lt, 'lu': validators.check_vat_lu,
    'lv': validators.check_vat_lv, 'mt': validators.check_vat_mt,
    'nl': validators.check_vat_nl, 'pl': validators.check_vat_pl,
    'pt': validators.check_vat_pt, 'ro': validators.check_vat_ro,
    'ru': validators.check_vat_ru, 'se': validators.check_vat_se,
    'si': validators.check_vat_si, 'sk': validators.check_vat_sk,
    'sm': validators.check_vat_sm, 'ua': validators.check_vat_ua,
    'uk': validators.check_vat_uk
}


def parse_vat(vat):
    code, number = vat[:2], vat[2:]
    return code.lower(), number


def check_vat(vat, parser=parse_vat, validators=VALIDATORS):
    '''
    Check VAT number.
    '''
    code, number = parser(vat)

    checker = validators.get(code)

    if checker is None:
        return False

    return checker(number)
