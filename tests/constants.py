"""Constants used for tests. These contain a lot of test values."""

from hypothesis import strategies

from aiousps import Address

XML_SAFE_CHARACTER_CLASSES = (
    'Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Mn', 'Mc', 'Me', 'Nd', 'Nl', 'No',
    'Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po', 'Sm', 'Sc', 'Sk', 'So',
    'Zs', 'Zl', 'Zp',
)
XML_SAFE_CHARACTER_STRATEGY = strategies.characters(whitelist_categories=XML_SAFE_CHARACTER_CLASSES)

SAMPLE_ADDRESSES = (  # These addresses are based on the sample addresses given in the USPS API documentation.
    Address('', '6406 Ivy Lane', 'Greenbelt', 'MD'),
    Address('', '6406 Ivy Lane', 'Greenbelt', 'MD', '20770', name='Name', company='Company', phone='+1-555-555-5555'),
    Address('', '8 Wildwood Drive', 'Old Lyme', 'CT'),
    Address('', '8 Wildwood Drive', 'Old Lyme', 'CT', '06371', name='Name', company='Company', phone='+1-555-555-5555'),
    Address('', '1390 Market Street', 'Houston', 'TX', '77058', '1234'),
    Address('', '1390 Market Street', 'Houston', 'TX', '77058', '1234', name='Name', company='Company',
            phone='+1-555-555-5555'),
    Address('', '1390 Market Street', '', '', '77058'),
    Address('', '1390 Market Street', '', '', '77058', name='Name', company='Company', phone='+1-555-555-5555'),
    # The following addresses are additional addresses made to make sure we're correctly serializing all addresses.
    Address('1 Main Street', 'Apartment 1', 'New York', 'NY')
)

SERIALIZED_ADDRESSES = (
    b'<?xml version=\'1.0\' encoding=\'iso-8859-1\'?>\n<TestRequest USERID="xxxxxxx"><Address2>6406 Ivy Lane</Address2><City>Greenbelt</City><State>MD</State></TestRequest>',
    b'<?xml version=\'1.0\' encoding=\'iso-8859-1\'?>\n<TestRequest USERID="xxxxxxx"><Name>Name</Name><FirmName>Company</FirmName><Address2>6406 Ivy Lane</Address2><City>Greenbelt</City><State>MD</State><Zip5>20770</Zip5><Phone>+1-555-555-5555</Phone></TestRequest>',
    b'<?xml version=\'1.0\' encoding=\'iso-8859-1\'?>\n<TestRequest USERID="xxxxxxx"><Address2>8 Wildwood Drive</Address2><City>Old Lyme</City><State>CT</State></TestRequest>',
    b'<?xml version=\'1.0\' encoding=\'iso-8859-1\'?>\n<TestRequest USERID="xxxxxxx"><Name>Name</Name><FirmName>Company</FirmName><Address2>8 Wildwood Drive</Address2><City>Old Lyme</City><State>CT</State><Zip5>06371</Zip5><Phone>+1-555-555-5555</Phone></TestRequest>',
    b'<?xml version=\'1.0\' encoding=\'iso-8859-1\'?>\n<TestRequest USERID="xxxxxxx"><Address2>1390 Market Street</Address2><City>Houston</City><State>TX</State><Zip5>77058</Zip5><Zip4>1234</Zip4></TestRequest>',
    b'<?xml version=\'1.0\' encoding=\'iso-8859-1\'?>\n<TestRequest USERID="xxxxxxx"><Name>Name</Name><FirmName>Company</FirmName><Address2>1390 Market Street</Address2><City>Houston</City><State>TX</State><Zip5>77058</Zip5><Zip4>1234</Zip4><Phone>+1-555-555-5555</Phone></TestRequest>',
    b'<?xml version=\'1.0\' encoding=\'iso-8859-1\'?>\n<TestRequest USERID="xxxxxxx"><Address2>1390 Market Street</Address2><Zip5>77058</Zip5></TestRequest>',
    b'<?xml version=\'1.0\' encoding=\'iso-8859-1\'?>\n<TestRequest USERID="xxxxxxx"><Name>Name</Name><FirmName>Company</FirmName><Address2>1390 Market Street</Address2><Zip5>77058</Zip5><Phone>+1-555-555-5555</Phone></TestRequest>',
    b'<?xml version=\'1.0\' encoding=\'iso-8859-1\'?>\n<TestRequest USERID="xxxxxxx"><Address1>1 Main Street</Address1><Address2>Apartment 1</Address2><City>New York</City><State>NY</State></TestRequest>',
)

CREATE_XML_VALUES = tuple(zip(SAMPLE_ADDRESSES, [''] * 9, SERIALIZED_ADDRESSES))

SAMPLE_VALIDATION_ADDRESSES = (
    Address('', '6406 Ivy Lane', 'Greenbelt', 'MD'),
    Address('', '6406 Ivy Lane', 'Greenbelt', 'MD', '20770', company='Name'),
    Address('6406 Ivy Lane', '', 'Greenbelt', 'MD'),
    Address('', '8 Wildwood Drive', 'Old Lyme', 'CT'),
    Address('', '1390 Market Street', 'Houston', 'TX', '77058', '1234', company='Company'),
    Address('', '1390 Market Street', '', '', '77058', company='Company'),
    Address('1 Main Street', 'Apartment 1', 'New York', 'NY'),
    Address('Suite K', '29851 Adventura', '', 'CA', '92688')
)

SAMPLE_VALIDATION_SERIALIZATIONS = [
    b'<AddressValidateRequest USERID="xxxxxxx"><Revision>1</Revision>'
    b'<Address ID="0"><FirmName/><Address1></Address1><Address2>6406 Ivy Lane</Address2><City>Greenbelt</City><State>MD</State><Zip5/><Zip4/></Address>'
    b'<Address ID="1"><FirmName>Name</FirmName><Address1></Address1><Address2>6406 Ivy Lane</Address2><City>Greenbelt</City><State>MD</State><Zip5>20770</Zip5><Zip4/></Address>'
    b'<Address ID="2"><FirmName/><Address1>6406 Ivy Lane</Address1><Address2></Address2><City>Greenbelt</City><State>MD</State><Zip5/><Zip4/></Address>'
    b'<Address ID="3"><FirmName/><Address1></Address1><Address2>8 Wildwood Drive</Address2><City>Old Lyme</City><State>CT</State><Zip5/><Zip4/></Address>'
    b'<Address ID="4"><FirmName>Company</FirmName><Address1></Address1><Address2>1390 Market Street</Address2><City>Houston</City><State>TX</State><Zip5>77058</Zip5><Zip4>1234</Zip4></Address>'
    b'</AddressValidateRequest>',

    b'<AddressValidateRequest USERID="xxxxxxx"><Revision>1</Revision>'
    b'<Address ID="5"><FirmName>Company</FirmName><Address1></Address1><Address2>1390 Market Street</Address2><City></City><State></State><Zip5>77058</Zip5><Zip4/></Address>'
    b'<Address ID="6"><FirmName/><Address1>1 Main Street</Address1><Address2>Apartment 1</Address2><City>New York</City><State>NY</State><Zip5/><Zip4/></Address>'
    b'<Address ID="7"><FirmName/><Address1>Suite K</Address1><Address2>29851 Adventura</Address2><City></City><State>CA</State><Zip5>92688</Zip5><Zip4/></Address>'
    b'</AddressValidateRequest>'
]
