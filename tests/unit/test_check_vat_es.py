#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

import chivato


validator = chivato.check_vat_es

COUNTRY_CODE = 'ES'

VALID_VAT_NUMBERS = [
    'A12345674',
    'P1234567D',
    'K1234567L',
    'R9600075G',
    'W4003922D',
    'V99218067',
    'U99216632',
    'J99216582',
    'U99216426',
    '12345678Z',
    'X5277343Q',
    'Y5277343F',
    'Z5277343K',
    'A12345690'
]

INVALID_VAT_NUMBERS = [
    '1234567890',
    'AB3456789',
    'A12345679',
    'WA003922D',
    'W4003922A',
    'ZA277343K',
    'Z5277343A',
    '1A345678Z',
    '12345678A'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS])


class TestSpainValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
