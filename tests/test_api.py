"""Unit tests for API"""
from unittest import mock

import pytest
from hypothesis import given
from hypothesis import strategies
from lxml import etree

from aiousps import USPSApi, USPSApiError, UspsEndpoint
from tests.constants import SAMPLE_VALIDATION_ADDRESSES, SAMPLE_VALIDATION_SERIALIZATIONS


@given(first_arg=strategies.text(), response=strategies.text())
def test_exception(first_arg, response):
    actual = USPSApiError(first_arg, response=response)

    assert repr(actual) == f'USPSApiError({first_arg!r})'
    assert actual.response == response


@given(
    uid=strategies.text(),
)
@pytest.mark.parametrize(
    ['test', 'endpoint_value'], [
        (True, 'Certify'),
        (False, '')
    ]
)
def test_init(test, endpoint_value, uid):
    api = USPSApi(uid, mock.AsyncMock(), test)

    assert api.api_user_id == uid
    assert api.test == test
    assert api.test_endpoint == endpoint_value


@pytest.fixture
def api():
    return USPSApi('xxxxxxx', mock.AsyncMock(), False)


@pytest.fixture
def test_api():
    return USPSApi('xxxxxxx', mock.AsyncMock(), True)


class TestGetEndpoints:
    UNCHANGED_ENDPOINTS = [  # string version on left, enum on right.
        ('validate', 'Verify'), (UspsEndpoint.VALIDATE, 'Verify'),
        ('city_state_lookup', 'CityStateLookup'), (UspsEndpoint.CITY_STATE_LOOKUP, 'CityStateLookup'),
        ('zip_code_lookup', 'ZipCodeLookup'), (UspsEndpoint.ZIP_CODE_LOOKUP, 'ZipCodeLookup'),
    ]
    TEST_ENDPOINTS = [
        ('tracking', 'TrackV2Certify'), (UspsEndpoint.TRACKING, 'TrackV2Certify'),
        ('label', 'eVSCertify'), (UspsEndpoint.LABEL, 'eVSCertify'),
    ]
    PRODUCTION_ENDPOINTS = [
        ('tracking', 'TrackV2'), (UspsEndpoint.TRACKING, 'TrackV2'),
        ('label', 'eVS'), (UspsEndpoint.LABEL, 'eVS'),
    ]

    @pytest.mark.parametrize(['endpoint', 'expected'], UNCHANGED_ENDPOINTS + TEST_ENDPOINTS)
    def test_get_testing_endpoints(self, test_api, endpoint, expected):
        actual = test_api.get_endpoint(endpoint)
        assert expected == actual

    @pytest.mark.parametrize(['endpoint', 'expected'], UNCHANGED_ENDPOINTS + PRODUCTION_ENDPOINTS)
    def test_get_real_endpoints(self, api, endpoint, expected):
        actual = api.get_endpoint(endpoint)
        assert expected == actual


class TestCloseSession:
    @pytest.mark.asyncio
    async def test_context_manager(self, api):
        async with api as api:
            pass
        api.session.close.assert_called_once_with()

    @pytest.mark.asyncio
    async def test_close(self, api):
        await api.close()
        api.session.close.assert_called_once_with()


class TestSendRequest:
    # TODO: Test the send_request method.
    pass


@pytest.mark.parametrize(
    ['addresses', 'xml_serializations'], [
        (SAMPLE_VALIDATION_ADDRESSES, SAMPLE_VALIDATION_SERIALIZATIONS)
    ]
)
def test_build_validate_xml(api, addresses, xml_serializations):
    builder = api._build_address_xml(addresses, 'AddressValidateRequest', [])
    actual = [etree.tostring(i) for i in builder]
    for actual_item, expected in zip(actual, xml_serializations):
        assert actual_item == expected
