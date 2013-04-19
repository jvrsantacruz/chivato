#-*- coding: utf-8 -*-

from hamcrest import assert_that, is_

import chivato


VALID_COUNTRY_CODE = u'AT'
NORMALIZED_COUNTRY_CODE = u'at'
VALID_NUMBER = u'U12345675'
VALID_VAT = VALID_COUNTRY_CODE + VALID_NUMBER
INVALID_VAT_TYPE = 123456


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
