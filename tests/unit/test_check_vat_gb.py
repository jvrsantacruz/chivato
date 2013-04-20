#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

from chivato import validators


validator = validators.check_vat_gb

COUNTRY_CODE = 'GB'
COUNTRY_CODE2 = 'UK'

VALID_VAT_NUMBERS = [
    'GD123',
    'HA567',
    '123456782',
    '102675046',
    '100190874',
    '003232345',
    '1234567823',
    'GD888812326',
    'HA888856782',
    '242338087388',
    '001123456782',
    '0011234567823'
]

INVALID_VAT_NUMBERS = [
    'GD1299',
    '123556782',
    '102575046',
    '100590874',
    '003532345'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE2, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS] +
               [(COUNTRY_CODE2, number, False) for number in INVALID_VAT_NUMBERS])


class TestGreatBritainValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
