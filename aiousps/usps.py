from typing import Iterable, Union

import aiohttp
import xmltodict
from lxml import etree

from . import Address
from .constants import ApiQueryLimits, LABEL_ZPL, RequiredFields, SERVICE_PRIORITY, USPS_API_REVISION, USPS_BASE_URL, \
    USPS_ENCODING, UspsEndpoint
from .helpers import enumerated_chunker

CITY_STATE_LOOKUP_EMPTY_FIELDS = ('name', 'company', 'address_1', 'address_2', 'city', 'state', 'phone', 'zip4')


class USPSApiError(Exception):
    def __init__(self, *args, response=None):
        """Instantiate an USPSApiError
        :param *args: Arguments that get sent to `Exception.__init__`
        :param response: The response object from the USPS API, if relevant
        """
        super().__init__(*args)
        self.response = response


class USPSApi(object):

    def __init__(self, api_user_id: str, session: aiohttp.ClientSession, test: bool = False):
        """USPS API client.

        :param api_user_id: A user ID for the USPS API. More detail is available on the USPS website: https://www.usps.com/business/web-tools-apis/
        :param session: An aiohttp ClientSession object. Specifics for compatible session objects can be viewed in the `send_request` method.
        :param test: A boolean of whether this is a test run or not. Test runs will use API endpoints that don't write to the database.
        """
        self.api_user_id = api_user_id
        self.test = test
        self.test_endpoint = 'Certify' if test else ''
        self.session = session

    async def __aenter__(self):
        """Make this usable as a context manager too."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self.session.close()

    def get_endpoint(self, action: Union[UspsEndpoint, str]) -> str:
        """Get the endpoint value for an action.

        :param action: the action, either as a string of the action
        :returns a string containing the value to put into the `API' header.
        """
        if isinstance(action, UspsEndpoint):
            action = action.value
        else:
            try:
                action = UspsEndpoint[action.upper()].value
            except KeyError:
                raise ValueError(f'Invalid action: {action}')
        return action.format(test=self.test_endpoint)

    async def send_request(self, action: Union[UspsEndpoint, str], xml: etree.Element):
        """Make a request to the USPS API.

        :param action: The action to perform, based on the supported endpoints.
        :param xml: An XML tree containing the relevant structure.

        The USPS developer guide says "ISO-8859-1 encoding is the expected character set for the request."
        (see https://www.usps.com/business/web-tools-apis/general-api-developer-guide.htm)
        """
        api = self.get_endpoint(action)
        xml = etree.tostring(xml, encoding=USPS_ENCODING, pretty_print=self.test).decode(USPS_ENCODING)
        response = await self.session.post(
            url=USPS_BASE_URL,
            data={'API': api, 'XML': xml}
        )
        xml_response = await response.text(encoding=USPS_ENCODING)
        response = xmltodict.parse(xml_response)
        if 'Error' in response:
            raise USPSApiError(response['Error']['Description'], response=response)
        return response

    def _build_address_xml(
            self, addresses: Iterable[Address], request_type: str,
            empty_fields: Iterable[str], required_fields: Iterable[str] = (),
            chunk_length: int = ApiQueryLimits.ADDRESSES, prefix=''
    ) -> Iterable[etree.Element]:
        """Generate XML structure for a request

        :param addresses: An iterable of Address objects containing the request info
        :param request_type: String to use as the request tipe. E.g. 'ZipCodeLookupRequest'
        :param empty_fields: Fields that must not be filled (they will cause a server error)
        :param required_fields: Fields that must be filled
        :param chunk_length: Number of addresses to send at once.
        :param prefix: The prefix needed for the address fields in this lookup type.
        :return:
        """
        for chunk in enumerated_chunker(addresses, chunk_length):
            xml = etree.Element(request_type, {'USERID': self.api_user_id})
            revision = etree.SubElement(xml, 'Revision')
            revision.text = USPS_API_REVISION
            for i, addr in chunk:
                addr.assert_empty(*empty_fields)
                addr.assert_filled(*required_fields)
                _address = etree.SubElement(xml, 'Address', {'ID': str(i)})
                addr.add_to_xml(_address, prefix=prefix, required_fields=RequiredFields.ADDRESS_VALIDATE)
            yield xml

    async def validate_addresses(self, addresses: Iterable[Address]):
        """Validate an iterable of addresses.

        :param addresses: An iterable (list, tuple, generator, etc.) of Address objects with values matching the address validation API items: https://www.usps.com/business/web-tools-apis/address-information-api.htm#_Toc34052589
        :yields Dictionaries containing the parsed outputs. Keys include `@ID`, which corresponds to the enumerated value of the input address, starting with 0. Other values can be found under the Address subelement in the AddressValidateResponse on the USPS documentation: https://www.usps.com/business/web-tools-apis/address-information-api.htm#_Toc34052591

        The USPS API only accepts 5 addresses for validation at a time. Because of this, addresses here are chunked into groups of up to 5. remaining
        """
        # It's undocumented, but the USPS API will only validate 5 addresses
        # at a time. As such, we need to chunk the addresses into groups of
        # 5 and do calls for 5 addresses at a time.
        for xml in self._build_address_xml(addresses, 'AddressValidateRequest', ['name', 'phone']):
            response = await self.send_request(UspsEndpoint.VALIDATE, xml)
            address_responses = response['AddressValidateResponse']['Address']
            if isinstance(address_responses, list):
                for result in address_responses:
                    yield result
            else:
                yield address_responses

    async def lookup_zip_code(self, addresses: Iterable[Address]):
        for xml in self._build_address_xml(addresses, 'ZipCodeLookupRequest', ['name', 'phone'], ['address_2']):
            response = await self.send_request(UspsEndpoint.VALIDATE, xml)
            address_responses = response['ZipCodeLookupResponse']['Address']
            if isinstance(address_responses, list):
                for result in address_responses:
                    yield result
            else:
                yield address_responses

    async def lookup_city_state(self, addresses: Iterable[Address]):
        for xml in self._build_address_xml(addresses, 'CityStateLookup', CITY_STATE_LOOKUP_EMPTY_FIELDS, ['zip']):
            response = await self.send_request(UspsEndpoint.CITY_STATE_LOOKUP, xml)
            for result in response['CityStateLookupResponse']['Address']:
                yield result

    async def track(self, tracking_numbers: Iterable[str]):
        for chunk in enumerated_chunker(tracking_numbers, ApiQueryLimits.TRACKING):
            xml = etree.Element('TrackRequest', {'USERID': self.api_user_id})
            for _, tracking_number in chunk:
                etree.SubElement(xml, "TrackID", {"ID": tracking_number})
            response = await self.send_request(UspsEndpoint.TRACKING, xml)
            for result in response['TrackResults']:
                yield result
