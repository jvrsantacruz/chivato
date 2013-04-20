#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

import chivato


validator = chivato.check_vat_se

COUNTRY_CODE = 'SE'

VALID_VAT_NUMBERS = [
    '123456789701',
    '556728341001'
]

INVALID_VAT_NUMBERS = [
    '1243456789701',
    '5740444347071',
    '5577344444037'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS])


class TestSwedenValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
