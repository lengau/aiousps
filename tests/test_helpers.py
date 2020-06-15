"""Tests for helper functions."""
import itertools
import string
from typing import Any, Collection, List, Tuple
from unittest import mock

import pytest
from hypothesis import given, strategies

from aiousps.helpers import enumerated_chunker, find_nonmatching_fields

ENUMERATED_CHUNKER_TEST_VALUES = [
    [range(10), 3, list(enumerate(range(10)))],
    [range(19, 100), 13, list(enumerate(range(19, 100)))],
    [range(150, 300), 1, list(enumerate(range(150, 300)))],
    [['a', 'b', 'c'], 2, [(0, 'a'), (1, 'b'), (2, 'c')]]
]
ELLIPSIS_ATTRS = dir(...)
VALID_FIELD_INITIAL_CHARACTERS = string.ascii_letters + '_'


@pytest.mark.parametrize(['iterable', 'n_items', 'expected'], ENUMERATED_CHUNKER_TEST_VALUES)
def test_enumerated_chunker_pairs_expected(iterable, n_items, expected):
    actual = enumerated_chunker(iterable, n_items)
    flattened = list(itertools.chain.from_iterable(actual))
    assert expected == flattened


@pytest.mark.parametrize(['collection', 'n_items', 'expected'], ENUMERATED_CHUNKER_TEST_VALUES)
def test_enumerated_chunker_chunk_length(collection: Collection, n_items: int, expected: List[Tuple[int, Any]]):
    actual = list(enumerated_chunker(collection, n_items))

    lengths = list(map(len, actual))
    assert max(lengths) == n_items
    assert min(lengths) == len(collection) % n_items or n_items


class TestFindNonmatchingFields:
    """Tests for `find_nonmatching_fields` class."""
    PYTHON_VALID_FIELD_STRATEGY = strategies.text(
        strategies.sampled_from(string.ascii_letters + '_'),
        min_size=1,
    )

    @given(fields=strategies.lists(PYTHON_VALID_FIELD_STRATEGY))
    def test_success_on_useless_test(self, fields):
        mock_item = mock.Mock()

        actual = find_nonmatching_fields(mock_item, lambda _: True, *fields)

        assert actual == []

    @given(fields=strategies.lists(PYTHON_VALID_FIELD_STRATEGY.filter(lambda x: x not in ELLIPSIS_ATTRS), min_size=1,
                                   max_size=10))
    def test_multiple_attributeerrors(self, fields):
        fake_item = ...
        fields_regex = ', '.join(['.+'] * len(fields))
        error_regex = f'ellipsis does not contain fields: {fields_regex}'

        with pytest.raises(AttributeError, match=error_regex) as e:
            find_nonmatching_fields(fake_item, lambda _: True, *fields)

    @given(fields=strategies.lists(PYTHON_VALID_FIELD_STRATEGY, min_size=1))
    def test_failure_returns_expected_message(self, fields):
        mock_item = mock.Mock()

        actual = find_nonmatching_fields(mock_item, lambda _: False, *fields)

        assert actual == fields
