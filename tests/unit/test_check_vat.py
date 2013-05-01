#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_
from doublex import Spy, called, ANY_ARG

from chivato.number import Number


VALID_COUNTRY_CODE = u'AT'
NORMALIZED_COUNTRY_CODE = u'at'
VALID_NUMBER = u'U12345675'
VALID_VAT = VALID_COUNTRY_CODE + VALID_NUMBER
INVALID_VAT_TYPE = 123456

was = is_


class TestParseVat(object):

    parse_vat = Number().parse

    def test_returns_code_and_number(self):
        code, number = self.parse_vat(VALID_VAT)

    def test_parses_code_to_normalized_country_code(self):
        code, number = self.parse_vat(VALID_VAT)

        assert_that(code, is_(VALID_COUNTRY_CODE))

    def test_parses_number(self):
        code, number = self.parse_vat(VALID_VAT)

        assert_that(number, is_(VALID_NUMBER))

    def test_parses_str(self):
        code, number = self.parse_vat(str(VALID_VAT))

    def test_parses_unicode(self):
        code, number = self.parse_vat(VALID_VAT)

    """ not quite yet, as it breaks Python3 compatibility
    from nose.tools import raises
    @raises(TypeError)
    def test_raises_TypeError_with_non_string_values(self):
        code, number = chivato.parse_vat(INVALID_VAT_TYPE)
    """


class TestValidate(object):

    number = Number()

    def test_function(self):
        validation_result = self.number.validate(VALID_VAT)

        assert_that(validation_result)

    def test_uses_parser_to_parse_input(self):
        with Spy() as spy:
            parse_return = [NORMALIZED_COUNTRY_CODE, VALID_NUMBER]
            spy.parser(ANY_ARG).returns(parse_return)
        self.number.parse = spy.parser

        self.number.validate(VALID_VAT)

        assert_that(spy.parser, was(called().with_args(VALID_VAT)))

    def test_uses_chooses_right_validator(self):
        with Spy() as validators:
            validators.get(ANY_ARG).returns(lambda number: None)

        self.number.validator(VALID_NUMBER, VALID_COUNTRY_CODE, validators=validators)

        assert_that(validators.get,
                    was(called().with_args(NORMALIZED_COUNTRY_CODE)))
