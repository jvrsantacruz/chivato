#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_, has_length

from chivato import validators

from nose.tools import raises


validator = validators.Spain()

COUNTRY_CODE = 'ES'

VALID_VAT_NUMBERS = [
    'A58818501'
]

INVALID_VAT_NUMBERS = [
    '32074371F'
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


VALID_VAT = 'A58818501'
INVALID_VAT = 'A5881850'


class TestSpainValidatorParsing(object):
    def test_parse_valid_vat_returns_fields(self):
        fields = validator.parse(VALID_VAT)

        assert_that(fields, has_length(3), VALID_VAT)

    def test_parse_valid_vat_returns_single_letter_company_kind(self):
        fields = validator.parse(VALID_VAT)

        kind = fields[0]

        assert_that(kind.isalpha())
        assert_that(kind, has_length(1), kind)

    def test_parse_valid_vat_returns_seven_digit_number(self):
        fields = validator.parse(VALID_VAT)

        number = fields[1]

        assert_that(number.isdigit())
        assert_that(number, has_length(7), number)

    def test_parse_valid_vat_returns_a_control_char(self):
        fields = validator.parse(VALID_VAT)

        control = fields[2]

        assert_that(control, has_length(1), control)

    @raises(ValueError)
    def test_parse_raises_value_error_on_invalid_numbers(self):
        validator.parse(INVALID_VAT)


class TestSpainValidatorControlCode(object):
    def test_control_character_calculation(self):
        for kind, number, control in [('A', '5881850', '1'),
                                      ('K', '5881850', 'A'),
                                      ('B', '7777850', '4'),
                                      ('P', '7777850', 'D')]:
            yield self.calculate, kind, number, control

    def calculate(self, kind, number, expected):
        control = validator.control_char(kind, number)

        assert_that(control, is_(expected), number)

    def test_control_character_returns_letter_if_kind_not_in_digit_only(self):
        control = validator.control_char(1, '1111111', digit_only=[])

        assert_that(control.isalpha())

    def test_control_character_returns_letter_if_kind_in_digit_only(self):
        control = validator.control_char(1, '1111111', digit_only=[1])

        assert_that(control.isdigit())
