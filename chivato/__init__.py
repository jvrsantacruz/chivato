#-*- coding: utf-8 -*-

__version__ = '0.0.1'

from . import staticdata, number


def countries():
    '''Return the list of country codes that have check function'''
    return staticdata.COUNTRIES


def check_vat(vat):
    return number.Number().validate(vat)
