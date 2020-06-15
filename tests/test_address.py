"""Tests for Address object"""
import re
import string

import pytest
from hypothesis import given
from lxml import etree

from aiousps import constants
from .constants import *


@given(
    name=strategies.text(XML_SAFE_CHARACTER_STRATEGY),
    company=strategies.text(XML_SAFE_CHARACTER_STRATEGY),
    address_1=strategies.text(XML_SAFE_CHARACTER_STRATEGY),
    address_2=strategies.text(XML_SAFE_CHARACTER_STRATEGY),
    city=strategies.text(XML_SAFE_CHARACTER_STRATEGY),
    state=strategies.text(XML_SAFE_CHARACTER_STRATEGY),
    zipcode=strategies.text(XML_SAFE_CHARACTER_STRATEGY),
    zipcode_ext=strategies.text(XML_SAFE_CHARACTER_STRATEGY),
    phone=strategies.text(XML_SAFE_CHARACTER_STRATEGY),
    prefix=strategies.text(
        strategies.sampled_from(string.ascii_letters + string.digits + '_'),
        min_size=1
    ).filter(
        lambda x: re.fullmatch(r'([_a-z][\w]?|[a-w_yz][\w]{2,}|[_a-z][a-l_n-z\d][\w]+|[_a-z][\w][a-k_m-z\d][\w]*)', x,
                               re.IGNORECASE)
    ),
)
def test_create_xml_works(name, company, address_1, address_2, city, state, zipcode, zipcode_ext, phone, prefix):
    address = Address(name, company, address_1, address_2, city, state, zipcode, zipcode_ext, phone)
    root = etree.Element('TestRoot')

    address.add_to_xml(root, prefix=prefix)


@pytest.fixture
def xml_root():
    return etree.Element('TestRequest', {'USERID': 'xxxxxxx'})


@pytest.mark.parametrize(
    ('address', 'prefix', 'expected'), CREATE_XML_VALUES
)
def test_create_xml_expected_text(address, xml_root, prefix, expected):
    address.add_to_xml(xml_root, prefix)
    actual = etree.tostring(xml_root, encoding=constants.USPS_ENCODING)

    assert expected == actual


@pytest.mark.parametrize(
    ('address', 'fields'),
    [
        (Address('', '', '', ''), ('address_1', 'address_2', 'city', 'state')),
        (Address('', '', '', 'blah'), ('address_1', 'address_2', 'city')),
    ]
)
def test_assert_empty_success(address, fields):
    address.assert_empty(*fields)


@pytest.mark.parametrize(
    ('address', 'fields', 'filled'),
    [
        (Address('a', '', '', ''), ('address_1', 'address_2', 'city', 'state'), 'address_1'),
        (Address('', 'a', '', ''), ('address_1', 'address_2', 'city', 'state'), 'address_2'),
        (Address('', '', 'a', ''), ('address_1', 'address_2', 'city', 'state'), 'city'),
        (Address('', '', '', 'a'), ('address_1', 'address_2', 'city', 'state'), 'state'),
        (Address('a', 'a', '', ''), ('address_1', 'address_2', 'city', 'state'), 'address_1, address_2'),
        (Address('a', '', 'a', ''), ('address_1', 'address_2', 'city', 'state'), 'address_1, city'),
        (Address('a', '', '', 'a'), ('address_1', 'address_2', 'city', 'state'), 'address_1, state'),
        (Address('a', 'a', 'a', ''), ('address_1', 'address_2', 'city', 'state'), 'address_1, address_2, city'),
        (Address('a', 'a', '', 'a'), ('address_1', 'address_2', 'city', 'state'), 'address_1, address_2, state'),
        (Address('a', '', 'a', 'a'), ('address_1', 'address_2', 'city', 'state'), 'address_1, city, state'),
        (Address('a', 'a', 'a', 'a'), ('address_1', 'address_2', 'city', 'state'), 'address_1, address_2, city, state'),
    ]
)
def test_assert_empty_fail(address, fields, filled):
    with pytest.raises(ValueError, match=f'Erroneous fields filled: {filled}'):
        address.assert_empty(*fields)
