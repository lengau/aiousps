import enum
from typing import Literal, Mapping

USPS_ENCODING = 'iso-8859-1'

LABEL_IMAGE = '4X6LABEL'
LABEL_ZPL = '4X6LABELZPL'

SERVICE_PRIORITY = 'PRIORITY'
SERVICE_PRIORITY_EXPRESS = 'PRIORITY EXPRESS'
SERVICE_FIRST_CLASS = 'FIRST CLASS'
SERVICE_PARCEL_SELECT = 'PARCEL SELECT GROUND'

USPS_BASE_URL = 'https://secure.shippingapis.com/ShippingAPI.dll'

class UspsEndpoint(enum.Enum):
    TRACKING = 'TrackV2{test}'
    LABEL = 'eVS{test}'
    VALIDATE = 'Verify'
    CITY_STATE_LOOKUP = 'CityStateLookup'
    ZIP_CODE_LOOKUP = 'ZipCodeLookup'
