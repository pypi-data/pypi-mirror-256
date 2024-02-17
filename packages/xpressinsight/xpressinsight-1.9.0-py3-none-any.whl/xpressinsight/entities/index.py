"""
    Xpress Insight Python package
    =============================

    This is an internal file of the 'xpressinsight' package. Do not import it directly.
    Define the Index entity type.

    This material is the confidential, proprietary, unpublished property
    of Fair Isaac Corporation.  Receipt or possession of this material
    does not convey rights to divulge, reproduce, use, or allow others
    to use it without the specific written authorization of Fair Isaac
    Corporation and use must conform strictly to the license agreement.

    Copyright (c) 2020-2024 Fair Isaac Corporation. All rights reserved.
"""

from typing import Any, Tuple, Mapping, List, Iterable, Set, Optional

import pandas as pd

from .basic_types import BASIC_TYPE, boolean, integer, string, real, check_type_np
from .entity import Entity, EntityBase
from ..type_checking import validate_list


def check_index_type_value(value: Any, expected_dtype: Optional[BASIC_TYPE], name: str):
    """ Check the value of an Index entity is as expected."""
    if not isinstance(value, pd.Index):
        raise TypeError(f"""
        Problem with {name}:
            Expected: pandas.Index
            Actual: {type(value)}.
        """)

    if value.size == 0:
        return

    if expected_dtype == integer:
        #
        if not pd.api.types.is_integer_dtype(value.dtype):
            msg = f"""
            All values in {name} must be integers, but the data type is: {value.dtype}.
            """
            raise TypeError(msg)

        check_type_np(value.values, integer, name)

    elif expected_dtype == real:
        check_type_np(value.values, real, name)

    elif expected_dtype == string:
        check_type_np(value.values, string, name)

    elif expected_dtype == boolean:
        if not pd.api.types.is_bool_dtype(value):
            msg = f"""
            All values in {name} must be Booleans.
            """
            raise TypeError(msg)

    elif expected_dtype:
        raise ValueError(f"Unrecognized dtype: {expected_dtype}")


class Index(Entity):
    """
    The configuration of an *index* entity. Use the helper function `xpressinsight.types.Index` to declare an index
    entity in an app, rather than instantiating `xpressinsight.Index` directly.

    Notes
    -----
    In older versions of `xpressinsight`, it was possible to use the `Index` as the annotation for an entity.
    This syntax is now deprecated and should not be used in new apps; it will not be supported in Python 3.12 and
    above.

    See Also
    --------
    types.Index
    Series
    DataFrame
    """

    @property
    def type_hint(self) -> type:
        """
        The target Python type for values in this Insight entity - e.g. the Python target type of an
        `xpressinsight.Series` is a `pandas.Series`.
        """
        return pd.Index

    def check_type(self, value: Any, name: str):
        """ Check type of given value is correct for this entity; 'name' argument is entity name to use in error
        message. """
        check_index_type_value(value, self.dtype, name)


def validate_index_names(parent_obj: EntityBase, attr_name: str, index: Any) -> Tuple[str, ...]:
    """ Validate and normalize list of names of Indexes -> convert it to immutable tuple """
    return validate_list(parent_obj, attr_name, str, 'string', index)


def get_index_tuple(parent_obj: EntityBase, index_names: Tuple[str, ...], entities: Mapping[str, EntityBase]) ->\
        Tuple[Index, ...]:
    """ Get a Tuple of Index objects from a single or tuple of index entity names. """
    result: List[Index] = []

    for index_name in index_names:
        index = entities.get(index_name, None)

        if isinstance(index, Index):
            result.append(index)
        else:
            if index is None:
                raise KeyError(f'Invalid index "{index_name}" for xpressinsight.{type(parent_obj).__name__} '
                               f'"{parent_obj.name}". Entity "{index_name}" not declared.')
            raise KeyError(f'Invalid index "{index_name}" for xpressinsight.{type(parent_obj).__name__} '
                           f'"{parent_obj.name}". Entity "{index_name}" is a {type(index)}, but must be an '
                           f'xpressinsight.Index.')

    return tuple(result)


def get_index_level_names(index_entity_names: Iterable[str]) -> List[str]:
    """
    Generate a unique name for each index level. The level name for an index will be the name of the index entity
    unless the same index entity is used in multiple levels, in which case duplicate names will be decorated with the
    level number (e.g. ".2", ".3").
    """
    levels_with_names: List[str] = []
    names_used_so_far: Set[str] = set()

    for name in index_entity_names:
        if name in names_used_so_far:
            name_with_level = f"{name}.{len(levels_with_names) + 1}"
        else:
            name_with_level = name

        levels_with_names.append(name_with_level)
        names_used_so_far.add(name_with_level)

    return levels_with_names
