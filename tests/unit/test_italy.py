#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

from chivato import validators


validator = validators.italy

COUNTRY_CODE = 'IT'


VALID_VAT_NUMBERS = [
    '12345670017',
    '00118439991'
]

INVALID_VAT_NUMBERS = [
    '45670017',
    '14345670017',
    '05118439991',
    '00118439993',
    '001T8439993'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS])


class TestItalyValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
