#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

import chivato


validator = chivato.check_vat_ru

COUNTRY_CODE = 'RU'

VALID_VAT_NUMBERS = [
    '5505035011',
    '550501929014'
]

INVALID_VAT_NUMBERS = [
    '4505035011',
    '3505035011',
    'A505035011',
    'A5050350111',
    '55050192901'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS])


class TestRussiaValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
