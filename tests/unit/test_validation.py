#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

import chivato

from . import *


VAT_NUMBERS = (
    test_austria.VAT_NUMBERS +
    test_albania.VAT_NUMBERS +
    test_argentina.VAT_NUMBERS +
    test_belgium.VAT_NUMBERS +
    test_bulgaria.VAT_NUMBERS +
    test_chile.VAT_NUMBERS +
    test_colombia.VAT_NUMBERS +
    test_cyprus.VAT_NUMBERS +
    test_czech_republic.VAT_NUMBERS +
    test_germany.VAT_NUMBERS +
    test_denmark.VAT_NUMBERS +
    test_estonia.VAT_NUMBERS +
    test_spain.VAT_NUMBERS +
    test_finland.VAT_NUMBERS +
    test_france.VAT_NUMBERS +
    test_united_kingdom.VAT_NUMBERS +
    test_greece.VAT_NUMBERS +
    test_croatia.VAT_NUMBERS +
    test_hungary.VAT_NUMBERS +
    test_ireland.VAT_NUMBERS +
    test_italy.VAT_NUMBERS +
    test_lithuania.VAT_NUMBERS +
    test_luxembourg.VAT_NUMBERS +
    test_latvia.VAT_NUMBERS +
    test_malta.VAT_NUMBERS +
    test_netherlands.VAT_NUMBERS +
    test_poland.VAT_NUMBERS +
    test_portugal.VAT_NUMBERS +
    test_romania.VAT_NUMBERS +
    test_russia.VAT_NUMBERS +
    test_sweden.VAT_NUMBERS +
    test_slovenia.VAT_NUMBERS +
    test_slovakia.VAT_NUMBERS +
    test_san_marino.VAT_NUMBERS +
    test_ukraine.VAT_NUMBERS +
    [
        ('', '12456789', False),
        ('1' * 50, '12456789', False),
        ('11', '12456789', False),
        ('NON', '12456789', False),
    ])


class TestValidation(object):
    def test_vat_numbers(self):
        for code, number, expected_result in VAT_NUMBERS:
            yield self.validation, code + number, expected_result

    def validation(self, vat_number, expected_result):
        validation_result = chivato.check_vat(vat_number)

        assert_that(validation_result, is_(expected_result), vat_number)

    def test_countries(self):
        chivato.countries()
