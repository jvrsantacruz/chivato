#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

from chivato import validators


validator = validators.check_vat_cy

COUNTRY_CODE = 'CY'


VALID_VAT_NUMBERS = [
    '12345678F'
]

INVALID_VAT_NUMBERS = [
    '2345678F',
    'A2345678F',
    '12345678A'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS])


class TestCyprusValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
