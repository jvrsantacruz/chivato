#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

from chivato import validators


validator = validators.check_vat_hr

COUNTRY_CODE = 'HR'

VALID_VAT_NUMBERS = [
    '12345678903',
    '24595836665',
    '23448731483'
]

INVALID_VAT_NUMBERS = [
    '42345678903',
    '24395836665',
    '23442731483'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS])


class TestCroatiaValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
