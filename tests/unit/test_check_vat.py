#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_
from doublex import Spy, called, ANY_ARG

import chivato


VALID_COUNTRY_CODE = u'AT'
NORMALIZED_COUNTRY_CODE = u'at'
VALID_NUMBER = u'U12345675'
VALID_VAT = VALID_COUNTRY_CODE + VALID_NUMBER
INVALID_VAT_TYPE = 123456

was = is_


class TestParseVat(object):
    def test_returns_code_and_number(self):
        code, number = chivato.parse_vat(VALID_VAT)

    def test_parses_code_to_normalized_country_code(self):
        code, number = chivato.parse_vat(VALID_VAT)

        assert_that(code, is_(NORMALIZED_COUNTRY_CODE))

    def test_parses_number(self):
        code, number = chivato.parse_vat(VALID_VAT)

        assert_that(number, is_(VALID_NUMBER))

    def test_parses_str(self):
        code, number = chivato.parse_vat(str(VALID_VAT))

    def test_parses_unicode(self):
        code, number = chivato.parse_vat(VALID_VAT)

    """ not quite yet, as it breaks Python3 compatibility
    from nose.tools import raises
    @raises(TypeError)
    def test_raises_TypeError_with_non_string_values(self):
        code, number = chivato.parse_vat(INVALID_VAT_TYPE)
    """


class TestCheckVat(object):
    def test_function(self):
        validation_result = chivato.check_vat(VALID_VAT)

        assert_that(validation_result)

    def test_uses_parser_to_parse_input(self):
        with Spy() as spy:
            spy.parser(ANY_ARG).returns(
                [NORMALIZED_COUNTRY_CODE, VALID_NUMBER]
            )

        chivato.check_vat(VALID_VAT, parser=spy.parser)

        assert_that(spy.parser, was(called().with_args(VALID_VAT)))

    def test_uses_chooses_right_validator(self):
        with Spy() as validators:
            validators.get(ANY_ARG).returns(lambda number: None)

        chivato.check_vat(VALID_VAT, validators=validators)

        assert_that(validators.get,
                    was(called().with_args(NORMALIZED_COUNTRY_CODE)))
