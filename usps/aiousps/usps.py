"""Async version of the USPS API."""

import json
try:
    import aiohttp
except ImportError:
    raise ImportError('async version of the USPS module requires aiohttp')
import xmltodict

from lxml import etree

from usps import USPSApi, USPSApiError


class AsyncUSPSApi(USPSApi):

    async def send_request(self, action, xml):
        # The USPS developer guide says "ISO-8859-1 encoding is the expected character set for the request."
        # (see https://www.usps.com/business/web-tools-apis/general-api-developer-guide.htm)
        xml = etree.tostring(xml, encoding='iso-8859-1',
                             pretty_print=self.test).decode()
        url = self.get_url(action, xml)
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            xml_response = await response.text(encoding='iso-8859-1')
        response = json.loads(json.dumps(xmltodict.parse(xml_response)))
        if 'Error' in response:
            raise USPSApiError(response['Error']['Description'])
        return response
