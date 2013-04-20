#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

from chivato import validators


validator = validators.slovakia

COUNTRY_CODE = 'SK'

VALID_VAT_NUMBERS = [
    '0012345675',
    '0012345678',
    '531231123',
    '6306151234',
    '2021853504'
]

INVALID_VAT_NUMBERS = [
    '1112345675',
    '0212345678',
    '531331123',
    '6306451234',
    '2121855514'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS])


class TestSlovakiaValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
