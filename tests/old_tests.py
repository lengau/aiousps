"""Old tests from the original usps-api. These should be considered deprecated and should be replaced with new tests."""

import asyncio

import mock

from lxml import etree

from unittest import TestCase

from aiousps.address import Address
from aiousps.usps import USPSApi, USPSApiError


class USPSApiTestCase(TestCase):

    def setUp(self):
        self.usps = USPSApi('XXXXXXXXXXXX', tests=True)

    def test_get_url(self):
        self.assertEqual(
            self.usps.get_url('tracking', 'tests'),
            'https://secure.shippingapis.com/ShippingAPI.dll?API=TrackV2Certify&XML=test'
        )
        self.assertEqual(
            self.usps.get_url('label', 'tests'),
            'https://secure.shippingapis.com/ShippingAPI.dll?API=eVSCertify&XML=test'
        )
        self.assertEqual(
            self.usps.get_url('validate', 'tests'),
            'https://secure.shippingapis.com/ShippingAPI.dll?API=Verify&XML=test'
        )
        usps = USPSApi('XXXXXXXXXXXX', tests=False)
        self.assertEqual(
            usps.get_url('tracking', 'tests'),
            'https://secure.shippingapis.com/ShippingAPI.dll?API=TrackV2&XML=test'
        )
        self.assertEqual(
            usps.get_url('label', 'tests'),
            'https://secure.shippingapis.com/ShippingAPI.dll?API=eVS&XML=test'
        )
        self.assertEqual(
            usps.get_url('validate', 'tests'),
            'https://secure.shippingapis.com/ShippingAPI.dll?API=Verify&XML=test'
        )

    @mock.patch('aiohttp.ClientSession')
    def test_send_request_error(self, session_class_mock):
        session_mock = session_class_mock.return_value.__aenter__.return_value
        response_mock = session_mock.get.return_value
        response_mock.text.return_value = b'<Error><Description>Test Error</Description></Error>'
        with self.assertRaises(USPSApiError):
            asyncio.run(
                self.usps.send_request('tracking', etree.Element('asdf')))

    @mock.patch('aiohttp.ClientSession')
    def test_send_request_valid(self, session_class_mock):
        session_mock = session_class_mock.return_value.__aenter__.return_value
        response_mock = session_mock.get.return_value
        response_mock.text.return_value = b'<Valid>tests</Valid>'
        response = asyncio.run(
            self.usps.send_request('tracking', etree.Element('asdf')))
        self.assertEqual(response, {'Valid': 'tests'})

    @mock.patch('aiousps.aiousps.AddressValidate.__init__')
    @mock.patch('aiousps.aiousps.TrackingInfo.__init__')
    @mock.patch('aiousps.aiousps.ShippingLabel.__init__')
    def test_wrapper_methods(self, address_mock, track_mock, ship_mock):
        address_mock.return_value = None
        track_mock.return_value = None
        ship_mock.return_value = None

        self.usps.validate_address()
        self.usps.track()
        self.usps.create_label()

        address_mock.assert_called()
        track_mock.assert_called()
        ship_mock.assert_called()


class AddressTestCase(TestCase):

    def test_address_xml(self):
        address = Address('Test', '123 Test St.', 'Test', 'NE', '55555')
        root = etree.Element('Test')
        address.add_to_xml(root, prefix='')

        elements = [
            'Name', 'Firm', 'Address1', 'Address2', 'City', 'State',
            'Zip5', 'Zip4', 'Phone'
        ]
        for child in root:
            self.assertTrue(child.tag in elements)


class AddressValidateTestCase(TestCase):
    pass


class TrackingInfoTestCase(TestCase):
    pass


class ShippingLabelTestCase(TestCase):
    pass

