from dataclasses import dataclass
from typing import Collection, Optional

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

    def add_to_xml(self, root: etree.Element, prefix: str = '', required_fields: Collection[str] = ()):
        if self.name or 'Name' in required_fields:
            self._add_item_to_xml(root, prefix + 'Name', self.name)
        if self.company or 'FirmName' in required_fields:
            self._add_item_to_xml(root, prefix + 'FirmName', self.company)
        if self.address_1 or 'Address1' in required_fields:
            self._add_item_to_xml(root, prefix + 'Address1', self.address_1)
        if self.address_2 or 'Address2' in required_fields:
            self._add_item_to_xml(root, prefix + 'Address2', self.address_2)
        if self.city or 'City' in required_fields:
            self._add_item_to_xml(root, prefix + 'City', self.city)
        if self.state or 'State' in required_fields:
            self._add_item_to_xml(root, prefix + 'State', self.state)
        if self.zip or 'Zip5' in required_fields:
            self._add_item_to_xml(root, prefix + 'Zip5', self.zip)
        if self.zip4 or 'Zip4' in required_fields:
            self._add_item_to_xml(root, prefix + 'Zip4', self.zip4)
        if self.phone or 'Phone' in required_fields:
            self._add_item_to_xml(root, prefix + 'Phone', self.phone)

        return root
    
    @staticmethod
    def _add_item_to_xml(parent: etree.Element, tag: str, text: Optional[str] = None):
        """Add an item to an XML element with a given name and possible text.
        
        :param parent: The parent XML element to add as a subelement.
        :param tag: The tag name for the subelement
        :param text: Any text to put into the tag.
        """
        child = etree.SubElement(parent, tag)
        if text is not None:
            child.text = text
        return child
            

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
