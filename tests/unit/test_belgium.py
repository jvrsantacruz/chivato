#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

from chivato import validators

validator = validators.belgium

COUNTRY_CODE = 'BE'

VALID_VAT_NUMBERS = [
    '0123456749',
    '0897290877'
]

INVALID_VAT_NUMBERS = [
    '01234567490',
    '9123456749',
    '0A23456749',
    '0123456700'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS])


class TestBelgiumValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
