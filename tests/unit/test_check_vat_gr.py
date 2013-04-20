#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

import chivato


validator = chivato.check_vat_gr

COUNTRY_CODE = 'GR'
COUNTRY_CODE2 = 'EL'

VALID_VAT_NUMBERS = [
    '12345670',
    '123456783'
]

INVALID_VAT_NUMBERS = [
    '32345670',
    '423456783'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE2, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS] +
               [(COUNTRY_CODE2, number, False) for number in INVALID_VAT_NUMBERS])


class TestGreeceValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
