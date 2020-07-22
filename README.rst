==============
async USPS API
==============

|python| |build| |coverage| |license|

-------------------

This is a simple async Python wrapper for the USPS API. It was forked from the `usps-api <https://github.com/BuluBox/usps-api>`_ project to make an async version. Instead of having to deal with XML, use this library and receive well formatted dictionaries back for tracking shipments, creating shipments, and validating addresses.

------------
Installation
------------

NOTE: ``aiousps`` is not yet published on pypi, so you'll have to install from source.

To install usps-api, use pip::

    pip install aiousps

Or to install from source::

    python setup.py install

-------------
Configuration
-------------

Note: In order to use any of these APIs, you need to register with USPS and get a `USERID <https://www.usps.com/business/web-tools-apis/welcome.htm>`_. For the create_shipment endpoint, you will also need to request further permissions by emailing uspstechnicalsupport@mailps.custhelp.com about Label API access.

The USPS developer guide is available at https://www.usps.com/business/web-tools-apis/general-api-developer-guide.htm

-----
Usage
-----


Track Shipments
---------------

.. code-block:: python

    from usps import USPSApi

    usps = USPSApi('XXXXXXXXXXXX')
    track = usps.track('00000000000000000000')
    print(track.result)


Create Shipment
---------------

The ``create_shipment`` function needs a to and from address, weight (in ounces), service type and label type. Service types and lable types can be found in ``usps/constants.py``. Defaults are ``SERVICE_PRIORITY`` and ``LABEL_ZPL``.

.. code-block:: python

    from usps import USPSApi, Address
    from usps import SERVICE_PRIORITY, LABEL_ZPL

    to_address = Address(
        name='Tobin Brown',
        address_1='1234 Test Ave.',
        city='Test',
        state='NE',
        zipcode='55555'
    )

    from_address = Address(
        name='Tobin Brown',
        address_1='1234 Test Ave.',
        city='Test',
        state='NE',
        zipcode='55555'
    )
    weight = 12  # weight in ounces

    usps = USPSApi('XXXXXXXXXXXX', test=True)
    label = usps.create_label(to_address, from_address, weight, SERVICE_PRIORITY, LABEL_ZPL)
    print(label.result)

Validate Address
----------------

.. code-block:: python

    from usps import USPSApi, Address

    address = Address(
        name='Tobin Brown',
        address_1='1234 Test Ave.',
        city='Test',
        state='NE',
        zipcode='55555'
    )
    usps = USPSApi('XXXXXXXXXXXX', test=True)
    validation = usps.validate_address(address)
    print(validation.result)

-------  
License
-------

MIT. See `LICENSE`_ for more details.


.. _LICENSE: https://github.com/Brobin/usps-api/blob/master/LICENSE

.. |license| image:: https://img.shields.io/github/license/Brobin/django-seed.svg?style=flat-square
    :target: https://github.com/Brobin/django-seed/blob/master/LICENSE
    :alt: MIT License

.. |coverage| image:: https://coveralls.io/repos/github/Brobin/usps-api/badge.svg?branch=master
    :target: https://coveralls.io/github/Brobin/usps-api?branch=master
    :alt: Code Coverage

.. |python| image:: https://img.shields.io/pypi/pyversions/usps-api.svg?style=flat-square
    :target: https://pypi.python.org/pypi/usps-api
    :alt: Python 3.5, 3.6, 3.7, 3.8

.. |build| image:: https://travis-ci.org/lengau/aiousps.svg?branch=master