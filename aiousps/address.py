from dataclasses import dataclass
from typing import Optional

from lxml import etree

from aiousps import helpers


@dataclass
class Address(object):
    address_1: str
    address_2: Optional[str]
    city: str
    state: str
    zip: Optional[str] = None
    zip4: Optional[str] = None
    name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None

    def add_to_xml(self, root: etree.Element, prefix: str = ''):
        if self.name:
            name = etree.SubElement(root, prefix + 'Name')
            name.text = self.name

        if self.company:
            company = etree.SubElement(root, prefix + 'FirmName')
            company.text = self.company

        if self.address_1:
            address_1 = etree.SubElement(root, prefix + 'Address1')
            address_1.text = self.address_1

        if self.address_2:
            address_2 = etree.SubElement(root, prefix + 'Address2')
            address_2.text = self.address_2

        if self.city:
            city = etree.SubElement(root, prefix + 'City')
            city.text = self.city

        if self.state:
            state = etree.SubElement(root, prefix + 'State')
            state.text = self.state

        if self.zip:
            zip = etree.SubElement(root, prefix + 'Zip5')
            zip.text = self.zip

        if self.zip4:
            zip4 = etree.SubElement(root, prefix + 'Zip4')
            zip4.text = self.zip4

        if self.phone:
            phone = etree.SubElement(root, prefix + 'Phone')
            phone.text = self.phone or ''

        return root

    def assert_empty(self, *fields):
        """Check that the given fields are empty.

        :param fields: Strings containing field names, such as `name`, `address_1`, etc.
        :raises ValueError if a field that should be empty is not.
        :raises AttributeError if at least one field listed is not an attribute of the class.
        """
        non_empty_fields = helpers.find_nonmatching_fields(self, lambda x: not x, *fields)
        if non_empty_fields:
            fields_str = ', '.join(non_empty_fields)
            raise ValueError(f'Erroneous fields filled: {fields_str}')

    def assert_filled(self, *fields):
        """Check that the given fields are filled.  In this case, that means a boolean evaluation of `True`.

        :param fields: Strings containing field names.
        :raises ValueError if a field that should be filled is not.
        :raises AttributeError if at least one field listed is not an attribute of the class.
        """
        empty_fields = helpers.find_nonmatching_fields(self, bool, *fields)
        if empty_fields:
            fields_str = ', '.join(empty_fields)
            raise ValueError(f'Mandatory fields not filled: {fields_str}')
