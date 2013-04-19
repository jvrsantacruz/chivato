#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

import chivato


validator = chivato.check_vat_de

COUNTRY_CODE = 'DE'

VALID_VAT_NUMBERS = [
    '123456788',
    '123456770'
]

INVALID_VAT_NUMBERS = [
    '12345678',
    'A23456788',
    '000000088',
    '123456789'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS])


class TestGermanyValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
