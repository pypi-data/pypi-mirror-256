"""
    Xpress Insight Python package
    =============================

    This is an internal file of the 'xpressinsight' package. Do not import it directly.
    Define the DataFrame entity type and associated classes.

    This material is the confidential, proprietary, unpublished property
    of Fair Isaac Corporation.  Receipt or possession of this material
    does not convey rights to divulge, reproduce, use, or allow others
    to use it without the specific written authorization of Fair Isaac
    Corporation and use must conform strictly to the license agreement.

    Copyright (c) 2020-2024 Fair Isaac Corporation. All rights reserved.
"""

from copy import deepcopy
from typing import Optional, Type, Union, List, Tuple, Mapping

import pandas as pd

from .basic_types import BasicType, BASIC_TYPE_VALUE, SCALAR_DEFAULT_VALUES, BASIC_TYPE, check_basic_type_value
from .entity import Entity, Hidden, Manage, EntityBase
from .index import Index, validate_index_names, get_index_tuple, get_index_level_names
from ..type_checking import validate_list


class Column(Entity):
    """
    Represent a single column within a *DataFrame* entity. Outside the Python model (e.g. VDL, Tableau),
    the column will be represented as a separate entity whose name combines the names of the DataFrame and the Column,
    concatenated by an underscore, i.e. `MyDataFrame_MyColumnName`

    Examples
    --------
    Example of declaring two columns `NumDays` and `NumMonths` which will contain integer values within a DataFrame.

    >>> YearInfoFrame: xi.types.DataFrame(index='Years', columns=[
    ...     xi.types.Column("NumDays", dtype=xi.integer,
    ...                     alias="Number of days"),
    ...     xi.types.Column("NumMonths", dtype=xi.integer,
    ...                     alias="Number of years"),
    ... ])

    When accessing the Insight data model from outside the Python app (for example, in VDL or Tableau views, or using
    the Insight REST API), this DataFrame is represented as two entities, `YearInfoFrame_NumDays` and
    `YearInfoFrame_NumMonths`. If values are inserted into these individual column entities outside the Python
    app, it's possible their indexes may not be consistent (e.g. `YearInfoFrame_NumDays` having values for 2003, 2004
    and 2005 while `YearInfoFrame_NumMonths` has values for just 2003 and 2005). In this case, the empty cells in
    each column will be filled in with a default value when the DataFrame is loaded back into Python.

    See Also
    --------
    types.DataFrame
    """

    #
    #
    #
    #
    def __init__(
            self,
            name: str,
            dtype: Optional[Type[BasicType[BASIC_TYPE_VALUE]]],
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
            default: BASIC_TYPE_VALUE = None,
            entity_name: str = None
            #
    ):
        """
        Initializes `Column`.

        Parameters
        ----------
        name : str
            The name of the column.
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
        default : Union[str, bool, int, float] = None
            The value to insert into any cells of this column that do not have a value when the DataFrame
            is loaded from the Insight scenario; optional. If specified, must be a value of the appropriate type for
            the `dtype` of this entity (e.g. a `str` if `dtype` is `string`).
        entity_name : str = None
            The entity name. If not given, the name of the class attribute will be used instead.
            Only valid for entities in a `ScenarioData`-decorated class.

        Notes
        -----
        Parameters before `update_progress` can be specified positionally for reasons of backwards compatibility,
        but it's recommended that you always use named arguments if you're specifying parameters other than `name`,
        `dtype` and `alias`.
        """
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
        #
        self.name = name

        if default is None and dtype is not None:
            default = SCALAR_DEFAULT_VALUES[dtype]
            assert default is not None

        if default is not None:
            check_basic_type_value(dtype, default, name)

        self.__default = default

        self.__data_frame: Optional[EntityBase] = None

    def _init_column(self, data_frame: EntityBase):
        """
        Initializes the column to be part of the given frame.
        """
        if self.__data_frame is not None:
            raise TypeError(f'Column "{self.name}" is already part of a frame')

        self.__data_frame = data_frame

    @property
    def type_hint(self) -> type:
        """
        The target Python type for values in this Insight entity - e.g. the Python target type of an
        `xpressinsight.Series` is a `pandas.Series`.
        """
        #
        raise TypeError("A Column does not have a type hint")

    @property
    def default(self) -> Union[str, bool, int, float]:
        """
        The value used to fill empty cells in this column when the DataFrame is loaded from the Insight
        scenario.
        """
        return self.__default

    @property
    def _default_entity_name(self) -> str:
        return f"{self.__data_frame.name}_{self.name}"


class DataFrame(EntityBase):
    """
    The configuration of a *DataFrame* entity. Use the helper function `xpressinsight.types.DataFrame` to declare a
    DataFrame entity in an app, rather than instantiating `xpressinsight.DataFrame` directly.

    Notes
    -----
    In older versions of `xpressinsight`, it was possible to use the `DataFrame` as the annotation for an entity.
    This syntax is now deprecated and should not be used in new apps; it will not be supported in Python 3.12 and
    above.

    See Also
    --------
    types.DataFrame
    types.Index
    Column
    """

    def __init__(
            self,
            index: Optional[Union[str, List[str]]],
            columns: Union[Column, List[Column]],
            *,
            index_types: List[Type[BasicType]] = None
    ):
        """
        Initializes `DataFrame`.

        Parameters
        ----------
        index : Optional[Union[str, List[str]]] = None
            The name of the index to use, or list of names for multiple indices. The same index may appear in the list
            multiple times.
            Required for entities in an `AppConfig`-decorated class, optional in a `ScenarioData`-decorated
            class.
        columns : Union[Column, List[Column]]
            The columns which make up this data frame.
        index_types : Optional[List[Type[BasicType]]] = None
            The types of the columns to use for the index(es) in the resultant series.
            Only valid for entities in an `ScenarioData`-decorated class, where it is optional.
        """
        super().__init__()
        self.__index_names: Tuple[str, ...] = validate_index_names(self, 'index', index)\
            if index is not None else None
        self.__index: Optional[Tuple[Index, ...]] = None
        self.__index_types: Optional[Tuple[BASIC_TYPE, ...]] =\
            validate_list(self, 'index_types', BASIC_TYPE, 'BASIC_TYPE', index_types)\
            if index_types is not None else None
        self.__columns: Tuple[Column, ...] = validate_list(self, 'columns', Column,
                                                      'xpressinsight.Column', deepcopy(columns))
        for col in self.__columns:
            col._init_column(self)

    def _init_app_entity(self, entities: Mapping[str, EntityBase]):
        if self.__index is not None:
            raise RuntimeError(f'The {type(self).__name__} "{self.name}" has already been initialized.')

        if self.__index_names is not None:
            self.__index = get_index_tuple(self, self.__index_names, entities)

    def _check_valid_app_entity(self):
        super()._check_valid_app_entity()

        #
        if not self.index_names:
            raise TypeError(f'DataFrame entity "{self.name}" must have index names.')

        #
        if self.__index_types:
            raise TypeError(f'DataFrame entity "{self.name}" must not set the "index_types" attribute.')

        for col in self.columns:
            col._check_valid_app_entity()

    def _check_valid_scenario_data_entity(self):
        super()._check_valid_scenario_data_entity()

        #
        if self.__index_names and self.__index_types and len(self.__index_names) != len(self.__index_types):
            raise TypeError(f'DataFrame entity "{self.name}" must not specify different numbers of index '
                            'names and types.')

        for col in self.columns:
            col._check_valid_scenario_data_entity()

    @property
    def type_hint(self) -> type:
        """
        The target Python type for values in this Insight entity - e.g. the Python target type of an
        `xpressinsight.Series` is a `pandas.Series`.
        """
        return pd.DataFrame

    @property
    def index(self) -> Optional[Tuple[Index, ...]]:
        """ Index entities for this DataFrame. """
        return self.__index

    @property
    def index_names(self) -> Optional[Tuple[str, ...]]:
        """ Names of index columns for this DataFrame. """
        return self.__index_names

    @property
    def unique_index_names(self) -> Optional[List[str]]:
        """
        Index names, modified so that each is unique. Where an entity is indexed multiple times by the same index,
        duplicate names will be decorated with their index (e.g. ".2", ".3"). This will correspond to the labels
        of the indexes in the Pandas DataFrame.
        """
        return get_index_level_names(self.index_names) if self.index_names else None

    @property
    def index_types(self) -> Optional[Tuple[BASIC_TYPE, ...]]:
        """ Types of index columns for this DataFrame. """
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
    def columns(self) -> Tuple[Column, ...]:
        """ Columns in this DataFrame. """
        return self.__columns

    @property
    def update_progress(self) -> bool:
        """ Check whether DataFrame has any columns where the `update_progress` attribute is `True`. """
        return any(column.update_progress for column in self.columns)

    def is_managed(self, manage: Manage) -> bool:
        """ Check whether the DataFrame has a column that is managed as the given management type. """
        return any(column.is_managed(manage) for column in self.columns)
