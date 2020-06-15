"""Helper functions for aiousps"""
import itertools
from typing import Any, Callable

try:
    from lxml import etree
except ImportError:
    from xml import etree


def enumerated_chunker(iterable, n_items):
    """A simple chunker that yields a list of up to `n_items` enumerated items from an iterator.

    :param iterable: An iterable to chunk.
    :param n_items: The number of items in each chunk.
    :yields A list of tuples, containing (item_number, item) from the iterable, beginning at 0.
    """
    iterator = enumerate(iterable)
    while True:
        chunk = list(itertools.islice(iterator, n_items))
        if not chunk:
            return
        yield chunk


def find_nonmatching_fields(item: Any, match_fn: Callable[[Any], bool], *fields):
    """Check that the given fields of an object match the output of a function.

    :param item: Any object with attributes to check.
    :param match_fn: A callable function. Each attribute named in `fields` will be passed in sequentially.
        Should return True if match succeeds or False if match fails.
    :param fields: Field names from the object to return
    :return: A list of fields that don't match.
    :raise: AttributeError if any of the fields does not exist.

    Example use: If you don't care which fields don't match, you can simply run:
        if not find_nonmatching_fields(item, my_fn, 'field_a', 'field_b'):
            # do thing if all fields match.
    """
    non_matching_fields = []
    non_existent_fields = []
    for field in fields:
        try:
            field_value = getattr(item, field)
        except AttributeError:
            non_existent_fields.append(field)
            continue
        if not match_fn(field_value):
            non_matching_fields.append(field)
    if non_existent_fields:
        fields_str = ', '.join(non_existent_fields)
        raise AttributeError(f'{item.__class__.__name__} does not contain fields: {fields_str}')
    return non_matching_fields
