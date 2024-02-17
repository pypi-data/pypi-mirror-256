"""
    Xpress Insight Python package
    =============================

    This is an internal file of the 'xpressinsight' package. Do not import it directly.
    Implement various entity-related utility functions.

    This material is the confidential, proprietary, unpublished property
    of Fair Isaac Corporation.  Receipt or possession of this material
    does not convey rights to divulge, reproduce, use, or allow others
    to use it without the specific written authorization of Fair Isaac
    Corporation and use must conform strictly to the license agreement.

    Copyright (c) 2024-2024 Fair Isaac Corporation. All rights reserved.
"""
from typing import Union, Any, Iterable

import pandas as pd

from .scalar import Scalar, Param
from .index import Index, get_index_level_names, check_index_type_value
from .series import Series
from .data_frame import DataFrame, Column
from .entity import UnexpectedEntityTypeError, Entity, EntityBase
from .basic_types import check_type_np, BasicType, BASIC_PANDAS_DTYPE_MAP


def get_empty_index_for_entity(entity: Union[Series, DataFrame]) -> pd.Index:
    """ Creates an empty pandas Index or MultiIndex with dtype and name information. """
    index_list = [
        pd.Index([], dtype=BASIC_PANDAS_DTYPE_MAP[index_type], name=level_name)
        for (level_name, index_type) in zip(get_index_level_names(entity.index_names), entity.index_types)
    ]

    if len(index_list) == 1:
        pd_index = index_list[0]
    else:
        pd_index = pd.MultiIndex.from_product(index_list)

    return pd_index


def check_type(
        value: Any, entity: EntityBase, columns: Iterable[Column] = None
):
    """ Verify that 'value' is the same type as given by 'entity'. """

    if isinstance(entity, (Scalar, Param, Series)):
        if entity.dtype and not issubclass(entity.dtype, BasicType):
            raise TypeError(f'dtype of entity "{entity.name}" must be a subclass of BasicType.')

    if isinstance(entity, (Scalar, Param)):
        entity.check_type(value)

    elif isinstance(entity, Index):
        entity.check_type(value, entity.name)

    elif isinstance(entity, (Series, DataFrame)):
        if isinstance(entity, Series) and not isinstance(value, pd.Series):
            raise TypeError(f"""
            Problem with entity "{entity.name}":
                Expected: pandas Series
                Actual: {type(value)}.
            """)

        if isinstance(entity, DataFrame) and not isinstance(value, pd.DataFrame):
            raise TypeError(f"""
            Problem with entity "{entity.name}":
                Expected: pandas DataFrame
                Actual: {type(value)}.
            """)

        #
        if entity.index_names and len(entity.index_names) != value.index.nlevels:
            raise TypeError(f'Problem with entity "{entity.name}": dimension of index set is {value.index.nlevels} '
                            f'but expecting {len(entity.index_names)}.')

        if entity.index_types:
            index_names = entity.index_names or ["unnamed" for _typ in entity.index_types]

            for idx_id, (idx_name, idx_dtype) in enumerate(zip(index_names, entity.index_types)):
                check_index_type_value(value.index.get_level_values(idx_id), idx_dtype,
                                       f'index {idx_id} ("{idx_name}") of entity "{entity.name}"')

        #
        if isinstance(entity, Series):
            if entity.dtype:
                check_type_np(value.values, entity.dtype, entity.name)

        elif isinstance(entity, DataFrame):
            #
            #
            for column in (columns or entity.columns):
                if column.name not in value.columns:
                    raise TypeError(f"Missing column '{column.name}' in DataFrame '{entity.name}'")

                if column.dtype:
                    check_type_np(
                        value.loc[:, column.name].values,
                        column.dtype,
                        f"{entity.name}.{column.name}"
                    )

    else:
        raise UnexpectedEntityTypeError(entity)


def get_non_composed_entities(entities: Iterable[EntityBase]) -> Iterable[Entity]:
    """ Given a sequence of entities, return the non-composed entities contained within.
        Ie if the entities list contains an entity E, the result will contain the columns of E if E is a DataFrame,
        or E if it is not.
    """
    non_composed_entities = []
    for entity in entities:
        if isinstance(entity, DataFrame):
            non_composed_entities.extend(entity.columns)
        else:
            non_composed_entities.append(entity)
    return non_composed_entities


def get_non_composed_entities_from_names(entities: Iterable[EntityBase], names: Iterable[str]) -> Iterable[Entity]:
    """ Find entity objects for the given names from the given entities. Only non-composed entities will be returned
        (ie no DataFrames). For each name, entities will be chosen as follows:
        If name matches name attribute of a non-DataFrame entity, return this.
        If name matches a DataFrame entity, return all Columns in that entity.
        If name matches entity name of a Column entity, return that column.
        If name does not match any entity, raise a ValueError
    """
    #
    #
    names_remaining = set(names)

    #
    selected_entities = []
    for entity in entities:
        #
        if entity.name in names_remaining:
            names_remaining.remove(entity.name)

            #
            if isinstance(entity, DataFrame):
                selected_entities.extend(entity.columns)
            else:
                selected_entities.append(entity)

        elif isinstance(entity, DataFrame):
            #
            for col in entity.columns:
                if col.entity_name in names_remaining:
                    names_remaining.remove(col.entity_name)
                    selected_entities.append(col)

    #
    if names_remaining:
        raise ValueError(f'The following {"entities were" if len(names_remaining)>1 else "entity was"} not found: ' +
                         ', '.join([f'"{n}"' for n in sorted(names_remaining)]))

    return selected_entities
