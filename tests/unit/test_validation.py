#-*- coding: utf-8 -*-
''' Unit test for chivato '''

from hamcrest import assert_that, is_

import chivato

from . import *


VAT_NUMBERS = (
    test_check_vat_at.VAT_NUMBERS +
    test_check_vat_al.VAT_NUMBERS +
    test_check_vat_ar.VAT_NUMBERS +
    test_check_vat_be.VAT_NUMBERS +
    test_check_vat_bg.VAT_NUMBERS +
    test_check_vat_cl.VAT_NUMBERS +
    test_check_vat_co.VAT_NUMBERS +
    test_check_vat_cy.VAT_NUMBERS +
    test_check_vat_cz.VAT_NUMBERS +
    test_check_vat_de.VAT_NUMBERS +
    test_check_vat_dk.VAT_NUMBERS +
    test_check_vat_ee.VAT_NUMBERS +
    test_check_vat_es.VAT_NUMBERS +
    test_check_vat_fi.VAT_NUMBERS +
    test_check_vat_fr.VAT_NUMBERS +
    test_check_vat_gb.VAT_NUMBERS +
    test_check_vat_gr.VAT_NUMBERS +
    test_check_vat_hr.VAT_NUMBERS +
    test_check_vat_hu.VAT_NUMBERS +
    test_check_vat_ie.VAT_NUMBERS +
    test_check_vat_it.VAT_NUMBERS +
    [
        ('LT', '123456715', True),
        ('LT', '123456789011', True),
        ('LU', '12345613', True),
        ('LV', '41234567891', True),
        ('LV', '15066312345', True),
        ('MT', '12345634', True),
        ('NL', '123456782B90', True),
        ('PL', '1234567883', True),
        ('PT', '123456789', True),
        ('RO', '24736200', True),
        ('RO', '1234567897', True),
        ('RO', '1630615123457', True),
        ('RO', '-7793957', False),
        ('RU', '5505035011', True),
        ('RU', '550501929014', True),
        ('SE', '123456789701', True),
        ('SE', '556728341001', True),
        ('SI', '12345679', True),
        ('SK', '0012345675', True),
        ('SK', '0012345678', True),
        ('SK', '531231123', True),
        ('SK', '6306151234', True),
        ('SK', '2021853504', True),
        ('SM', '12345', True),
        ('UA', '12345678', True),
        ('', '12456789', False),
    ])


class TestValidation(object):
    def test_vat_numbers(self):
        for code, number, expected_result in VAT_NUMBERS:
            yield self.validation, code + number, expected_result

    def validation(self, vat_number, expected_result):
        validation_result = chivato.check_vat(vat_number)

        assert_that(validation_result, is_(expected_result), vat_number)

    def test_countries(self):
        chivato.countries()
