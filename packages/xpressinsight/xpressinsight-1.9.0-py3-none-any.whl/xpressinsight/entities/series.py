"""
    Xpress Insight Python package
    =============================

    This is an internal file of the 'xpressinsight' package. Do not import it directly.
    Define the Series entity type.

    This material is the confidential, proprietary, unpublished property
    of Fair Isaac Corporation.  Receipt or possession of this material
    does not convey rights to divulge, reproduce, use, or allow others
    to use it without the specific written authorization of Fair Isaac
    Corporation and use must conform strictly to the license agreement.

    Copyright (c) 2020-2024 Fair Isaac Corporation. All rights reserved.
"""

from typing import Optional, Union, List, Tuple, Mapping

import pandas as pd

from .basic_types import BASIC_TYPE
from .entity import Entity, Hidden, Manage, EntityBase
from .index import Index, validate_index_names, get_index_tuple, get_index_level_names
from ..type_checking import validate_list


class Series(Entity):
    """
    The configuration of a *Series* entity, a declaration of a pandas `Series` data structure. Use the helper function
    `xpressinsight.types.Series` to declare a Series entity in an app, rather than instantiating
    `xpressinsight.Series` directly.

    Notes
    -----
    In older versions of `xpressinsight`, it was possible to use the `Series` as the annotation for an entity.
    This syntax is now deprecated and should not be used in new apps; it will not be supported in Python 3.12 and
    above.

    See Also
    --------
    types.Series
    """

    __series_name: Optional[str]

    #
    #
    #
    #
    def __init__(
            self,
            index: Union[str, List[str]] = None,
            dtype: BASIC_TYPE = None,
            #
            alias: str = "",
            format: str = "",  #
            hidden: Hidden = Hidden.FALSE,
            manage: Manage = Manage.INPUT,
            read_only: bool = False,
            transform_labels_entity: str = "",
            update_after_execution: bool = False,
            *,
            update_progress: bool = False,
            entity_name: str = None,
            series_name: str = None,
            index_types: List[BASIC_TYPE] = None
            #
    ):
        """
        Initializes `Series`.

        Parameters
        ----------
        index : Union[str, List[str]]
            The name of the index to use, or list of names for multiple indices. Where entity is used in an app
            definition, the same index may appear in the list multiple times.
        dtype : BASIC_TYPE
            The data type.
        alias : str = ""
            Used to provide an alternative name for an entity in the UI.
            The value is used in place of the entity name where appropriate in the UI.
        format : str = ""
            The formatting string used for displaying numeric values.
        hidden : Hidden = Hidden.FALSE
            Indicates whether the UI should hide the entity where appropriate.
        manage : Manage = Manage.INPUT
            How and whether Insight handles an entity. Defines how the system manages the entity data.
        read_only : bool = False
            Whether an entity is readonly. Specifies that the value(s) of the entity cannot be modified. See also
            `hidden`.
        transform_labels_entity : str = ""
            The name of an entity in the schema from which to read labels for values of this entity.
            The type of the index set of the labels entity must match the data type of this entity.
            The data type of the labels entity can be any primitive type.
        update_after_execution : bool = False
            Whether the value of the entity in the scenario is updated with the value of
            the corresponding model entity at the end of the scenario execution.
            If `True` the value of the entity is updated to correspond with the model entity after execution.
        update_progress : bool = False
            Whether the value of the entity in the scenario is sent on progress updates.
            If `True` the value of the entity will be written back to the Insight repository when
            :fct-ref:`insight.send_progress_update` is called from an execution mode where the `send_progress`
            attribute is `True`.
        entity_name : str = None
            The entity name. If not given, the name of the class attribute will be used instead.
            Only valid for entities in a `ScenarioData`-decorated class.
        series_name : str = None
            The name to use for the values in the resultant series. If not given, the entity name will
            be used.
            Only valid for entities in a `ScenarioData`-decorated class.
        index_types : List[BASIC_TYPE] = None
            The names of the columns to use for the index(es) in the resultant series. If not given, names derived from
            the index entities in the other scenario will be used. If given, the names must be unique and there must be
            one for each index column.
            Only valid for entities in a `ScenarioData`-decorated class.

        Notes
        -----
        Parameters before `update_progress` can be specified positionally for reasons of backwards compatibility,
        but it's recommended that you always use named arguments if you're specifying parameters other than `index`,
        `dtype` and `alias`.
        """

        #
        #
        self.__series_name = series_name

        super().__init__(
            dtype=dtype,
            #
            alias=alias,
            format=format,
            hidden=hidden,
            manage=manage,
            read_only=read_only,
            transform_labels_entity=transform_labels_entity,
            update_after_execution=update_after_execution,
            update_progress=update_progress,
            entity_name=entity_name
            #
        )

        self.__index_names: Optional[Tuple[str, ...]] = validate_index_names(self, 'index', index)\
            if index else None
        self.__index_types: Optional[Tuple[BASIC_TYPE, ...]] =\
            validate_list(self, 'index_types', BASIC_TYPE, 'BASIC_TYPE', index_types)\
            if index_types else None
        self.__index: Optional[Tuple[Index, ...]] = None

    def _init_app_entity(self, entities: Mapping[str, EntityBase]):
        if self.__index is not None:
            raise RuntimeError(f'The {type(self).__name__} "{self.name}" has already been initialized.')

        if self.__index_names is not None:
            self.__index = get_index_tuple(self, self.__index_names, entities)

    def _check_valid_app_entity(self):
        super()._check_valid_app_entity()

        #
        if not self.index_names:
            raise TypeError(f'Series entity "{self.name}" must have index names.')

        #
        if self.__index_types:
            raise TypeError(f'Series entity "{self.name}" must not set the "index_types" attribute.')

        #
        if self.__series_name:
            raise TypeError(f'Series entity "{self.name}" must not set the "series_name" attribute.')

    def _check_valid_scenario_data_entity(self):
        super()._check_valid_scenario_data_entity()

        #
        if self.__index_names and self.__index_types and len(self.__index_names) != len(self.__index_types):
            raise TypeError(f'Series entity "{self.name}" must not specify different numbers of index names '
                            'and types.')

    @property
    def type_hint(self) -> type:
        """
        The target Python type for values in this Insight entity - e.g. the Python target type of an
        `xpressinsight.Series` is a `pandas.Series`.
        """
        return pd.Series

    @property
    def index(self) -> Optional[Tuple[Index, ...]]:
        """ Index entities for this series. """
        return self.__index

    @property
    def index_names(self) -> Optional[Tuple[str, ...]]:
        """ Index names for this series. """
        return self.__index_names

    @property
    def unique_index_names(self) -> Optional[List[str]]:
        """
        Index names, modified so that each is unique. Where an entity is indexed multiple times by the same index,
        duplicate names will be decorated with their index (e.g. ".2", ".3"). This will correspond to the labels
        of the indexes in the Pandas Series.
        """
        return get_index_level_names(self.index_names) if self.index_names else None

    @property
    def index_types(self) -> Optional[Tuple[BASIC_TYPE, ...]]:
        """ Index types for this series. """
        if self.__index_types:
            return self.__index_types

        if self.index:
            #
            #
            dtypes: List[BASIC_TYPE] = []
            for ind in self.index:
                if not ind.dtype:
                    raise ValueError(f"No type configured for index entity {ind.name}")

                dtypes.append(ind.dtype)

            return tuple(dtypes)

        return None

    @property
    def series_name(self) -> Optional[str]:
        """ Name to be used for this Pandas series. """
        return self.__series_name if self.__series_name else self.name
