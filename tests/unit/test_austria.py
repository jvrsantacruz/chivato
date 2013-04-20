#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

from chivato import validators

validator = validators.austria

COUNTRY_CODE = 'AT'

VALID_VAT_NUMBERS = [
    'U12345675'
]

INVALID_VAT_NUMBERS = [
    'U123456789',
    'A12345675',
    'UA2345675',
    'U12345678'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS])


class TestAustriaValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
