#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

from chivato import validators


validator = validators.check_vat_bg

COUNTRY_CODE = 'BG'

VALID_VAT_NUMBERS = [
    '1234567892',
    '175074752',
    '131202360',
    '040683212',
    '1001000000'
]

INVALID_VAT_NUMBERS = [
    '12345678921',
    'A234567892',
    '2234567892',
    '0000003000',
    '1234567890'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS])


class TestBulgariaValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
