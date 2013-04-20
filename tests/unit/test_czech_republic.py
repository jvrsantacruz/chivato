#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

from chivato import validators


validator = validators.czech_republic

COUNTRY_CODE = 'CZ'

VALID_VAT_NUMBERS = [
    '12345679',
    '10001000',
    '10000101',
    '612345670',
    '991231123',
    '6306150004',
    '6306150004'
]

INVALID_VAT_NUMBERS = [
    '1234567',
    'A2345679',
    '92345679',
    '12345670',
    '612345679',
    '541231123',
    '791231123',
    '990031123',
    '991331123',
    '995031123',
    '996331123',
    '990200123',
    '995229123',
    '965200123',
    '960230123',
    '990400123',
    '990431123',
    '990100123',
    '990132123',
    '5306150004',
    '6300150004',
    '6313150004',
    '6350150004',
    '6363150004',
    '6302000004',
    '6302290004',
    '6402000004',
    '6402310004',
    '6304000004',
    '6304310004',
    '6301000004',
    '6301320004',
    '6306150000'
]

VAT_NUMBERS = ([(COUNTRY_CODE, number, True) for number in VALID_VAT_NUMBERS] +
               [(COUNTRY_CODE, number, False) for number in INVALID_VAT_NUMBERS])


class TestCzechRepublicValidator(object):
    def test_valid_codes_are_accepted(self):
        for number in VALID_VAT_NUMBERS:
            yield self.validation, number, True

    def validation(self, number, expected_result):
        validation_result = validator(number)

        assert_that(validation_result, is_(expected_result), number)
