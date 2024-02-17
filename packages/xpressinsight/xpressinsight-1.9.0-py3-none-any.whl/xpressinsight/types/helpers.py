"""
    Xpress Insight Python package
    =============================

    This is an internal file of the 'xpressinsight' package. Do not import it directly.

    This material is the confidential, proprietary, unpublished property
    of Fair Isaac Corporation.  Receipt or possession of this material
    does not convey rights to divulge, reproduce, use, or allow others
    to use it without the specific written authorization of Fair Isaac
    Corporation and use must conform strictly to the license agreement.

    Copyright (c) 2020-2024 Fair Isaac Corporation. All rights reserved.
"""

import sys
from typing import Union, List, Type
import pandas as pd

from .. import entities as xi_entities
from ..entities import Hidden, Manage, BasicType, BASIC_TYPE_VALUE, BASIC_TYPE, BASIC_TYPE_MAP

if sys.version_info < (3, 9):
    from typing_extensions import Annotated
else:
    from typing import Annotated


#
#
#
#
#
def Scalar(
        default: BASIC_TYPE_VALUE = None,
        dtype: Type[BasicType[BASIC_TYPE_VALUE]] = None,
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
        #
) -> Type[BASIC_TYPE_VALUE]:
    #
    #
    """
    Creates an annotation for a *scalar* entity in an app.

    Examples
    --------
    Some examples of declaring scalar entities in the data model.

    >>> @xi.AppConfig(name="My First Insight Python App",
    ...               version=xi.AppVersion(0, 1, 2))
    ... class MyApp(xi.AppBase):
    ...
    ...     # Examples where data type is inferred from initial value
    ...     # Scalar "NumFactory" of type "xi.integer"; initial value 10
    ...     NumFactory: xi.types.Scalar(10)
    ...     # Scalar "IsOn" of type "xi.boolean"; initial value True
    ...     IsOn: xi.types.Scalar(True)
    ...
    ...     # Examples where data type is explicitly given and value will be initialized to a type-specific default
    ...     RealScalar: xi.types.Scalar(dtype=xi.real)      # default value 0.0
    ...     StringScalar: xi.types.Scalar(dtype=xi.string)  # default value ""

    Parameters
    ----------
    default : BASIC_TYPE_VALUE = None
        The initial value; if specified, must be a value of the appropriate type for the `dtype` of this entity (e.g.
        a `str` if `dtype` is `string`).
    dtype : Type[BasicType[BASIC_TYPE_VALUE]]
        The data type; one of `boolean`, `real`, `integer` or `string`.
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

    Notes
    -----
    This function returns an `Annotated` type containing the `Scalar` entity object; for example,
    if `xpressinsight` has been imported as `xi`, then `xi.types.Scalar(dtype=xi.integer)` is equivalent to
    `Annotated[int, xi.Scalar(dtype=xi.integer)]`.

    Parameters before `update_progress` can be specified positionally for reasons of backwards compatibility,
    but it's recommended that you always use named arguments if you're specifying parameters other than `default`,
    `dtype` and `alias`.

    See Also
    --------
    Scalar
    types.Param
    """
    entity = xi_entities.Scalar(
        default=default,
        dtype=dtype,
        alias=alias,
        format=format,
        hidden=hidden,
        manage=manage,
        read_only=read_only,
        transform_labels_entity=transform_labels_entity,
        update_after_execution=update_after_execution,
        update_progress=update_progress
    )
    return Annotated[BASIC_TYPE_MAP[entity.dtype], entity]


#
#
#
#
def Param(
        default: BASIC_TYPE_VALUE = None,
        dtype: Type[BasicType[BASIC_TYPE_VALUE]] = None
) -> Type[BASIC_TYPE_VALUE]:
    #
    #
    """
    Creates an annotation for a *parameter* entity. Parameters can be used to configure an Xpress Insight app. When
    parameters are declared, their name, data type, and default value must be specified. Parameters are typically
    read-only.

    Examples
    --------
    Some examples of declaring parameter entities in the data model.

    >>> @xi.AppConfig(name="My First Insight Python App",
    ...               version=xi.AppVersion(0, 1, 2))
    ... class MyApp(xi.AppBase):
    ...
    ...     # examples where data type is inferred from the initial value
    ...     # Param "P" of type "xi.integer" with initial value 100
    ...     P: xi.types.Param(100)
    ...     # Param "DEBUG" of type "xi.boolean" with initial value False
    ...     DEBUG: xi.types.Param(False)
    ...     # Param "PI" of type "xi.real" with initial value 3.14
    ...     PI: xi.types.Param(3.14)
    ...     # Param "STR_PARAM" of type xi.string with a initial value
    ...     STR_PARAM: xi.types.Param('My String Param')
    ...
    ...     # examples where data type is explicitly given and value will be initialized to a type-specific default
    ...     BOOL_PARAM: xi.types.Param(dtype=xi.boolean)  # default value False
    ...     INT_PARAM: xi.types.Param(dtype=xi.integer)  # default value 0
    ...     REAL_PARAM: xi.types.Param(dtype=xi.real)  # default value 0.0
    ...     STRING_PARAM: xi.types.Param(dtype=xi.string)  # default value ""

    Parameters
    ----------
    default : BASIC_TYPE_VALUE
        The default value; if specified, must be of the appropriate value for the `dtype` of this entity (e.g.
        a `str` if `dtype` is `string`).
    dtype : Type[BasicType[BASIC_TYPE_VALUE]]
        The data type; one of `boolean`, `real`, `integer` or `string`.

    Notes
    -----
    This function returns an `Annotated` type containing the `Param` entity object; for example,
    if `xpressinsight` has been imported as `xi`, then `xi.types.Param(dtype=xi.integer)` is equivalent to
    `Annotated[int, xi.Param(dtype=xi.integer)]`.

    See Also
    --------
    Param
    types.Scalar
    """
    entity = xi_entities.Param(
        default=default,
        dtype=dtype
    )
    return Annotated[BASIC_TYPE_MAP[entity.dtype], entity]


#
#
#
#
#
def Index(
        dtype: BASIC_TYPE,
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
        #
) -> Type[pd.Index]:
    #
    #
    """
    Creates an annotation for an *index* entity in an app. To be used in conjunction with `xpressinsight.types.Series`
    or `xpressinsight.types.DataFrame` entities.

    Examples
    --------
    Example creating an index of integer values with an alias.

    >>> Indices: xi.types.Index(dtype=xi.integer, alias='Array Indices')

    Parameters
    ----------
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

    Notes
    -----
    This function returns an `Annotated` type containing the `Index` entity object; for example,
    if `xpressinsight` has been imported as `xi`, then `xi.types.Index(dtype=xi.integer)` is equivalent to
    `Annotated[pandas.Index, xi.Index(dtype=xi.integer)]`.

    Parameters before `update_progress` can be specified positionally for reasons of backwards compatibility,
    but it's recommended that you always use named arguments if you're specifying parameters other than
    `dtype` and `alias`.

    See Also
    --------
    types.Series
    types.DataFrame
    Index
    """
    entity = xi_entities.Index(
        dtype=dtype,
        alias=alias,
        format=format,
        hidden=hidden,
        manage=manage,
        read_only=read_only,
        transform_labels_entity=transform_labels_entity,
        update_after_execution=update_after_execution,
        update_progress=update_progress
    )
    return Annotated[pd.Index, entity]


#
#
#
#
#
def Series(
        index: Union[str, List[str]],
        dtype: BASIC_TYPE,
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
) -> Type[pd.Series]:
    #
    #
    """
    Creates an annotation for a *Series* entity in an app, a declaration of a pandas `Series` datastructure.
    Every series must have at least one index.

    Examples
    --------
    Example of creating a `Result` series containing floating-point values, and is managed by Insight as a result
    entity.
    It is indexed by `Indices`, which must have been declared previously.

    >>> Indices: xi.types.Index(...) # previous declaration
    ... Result: xi.types.Series(index=['Indices'], dtype=xi.real,
    ...                   manage=xi.Manage.RESULT, alias='Result Array')


    Parameters
    ----------
    index : Union[str, List[str]]
        The name of the index to use, or list of names for multiple indices. The same index may appear in the list
        multiple times.
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

    Notes
    -----
    This function returns an `Annotated` type containing the `Series` entity object; for example,
    if `xpressinsight` has been imported as `xi`, then `xi.types.Series(index='idx', dtype=xi.integer)` is equivalent to
    `Annotated[pandas.Series, xi.Series(index='idx', dtype=xi.integer)]`.

    Parameters before `update_progress` can be specified positionally for reasons of backwards compatibility,
    but it's recommended that you always use named arguments if you're specifying parameters other than
    `dtype` and `alias`.

    See Also
    --------
    types.Index
    Series
    """
    entity = xi_entities.Series(
        index=index,
        dtype=dtype,
        alias=alias,
        format=format,
        hidden=hidden,
        manage=manage,
        read_only=read_only,
        transform_labels_entity=transform_labels_entity,
        update_after_execution=update_after_execution,
        update_progress=update_progress
    )
    return Annotated[pd.Series, entity]


class Column(xi_entities.Column):
    #
    #
    """
    Represent a single column within a *DataFrame* entity in an app. Outside the Python model (e.g. VDL, Tableau),
    the column will be represented as a separate entity whose name combines the names of the DataFrame and the Column,
    concatenated by an underscore, i.e. `MyDataFrame_MyColumnName`.

    Examples
    --------
    Example of declaring two columns `NumDays` and `NumMonths` which will contain integer values within a DataFrame.

    >>> YearInfoFrame: xi.types.DataFrame(index='Years', columns=[
    ...     xi.types.Column("NumDays", dtype=xi.integer)
    ...     xi.types.Column("NumMonths", dtype=xi.integer)
    ... ])

    The entity name of the column is assumed to be the DataFrame name and column name, joined by an underscore
    (e.g. `YearInfoFrame_NumDays` and `YearInfoFrame_NumMonths` in the above example), unless a different value is
    passed in the `entity_name` attribute.
    """

    #
    #
    #
    def __init__(
            self,
            name: str,
            dtype: Type[BasicType[BASIC_TYPE_VALUE]],
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
            #
    ):
        """
        Initializes `Column` in a DataFrame in an app.

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
        """
        super().__init__(
            name=name,
            dtype=dtype,
            alias=alias,
            format=format,
            hidden=hidden,
            manage=manage,
            read_only=read_only,
            transform_labels_entity=transform_labels_entity,
            update_after_execution=update_after_execution,
            update_progress=update_progress,
            default=default
        )


#
#
#
#
def DataFrame(
        index: Union[str, List[str]],
        columns: Union[xi_entities.Column, List[xi_entities.Column]]
) -> Type[pd.DataFrame]:
    #
    #
    """
        Creates an annotation for a *DataFrame* entity in an app.

        Examples
        --------
        Example declaring a data frame `MixedTable` which has three columns.

        >>> MixedTable: xi.types.DataFrame(index='Years', columns=[
        ...     xi.types.Column("IntCol", dtype=xi.integer, default=-1,
        ...                     alias="Input Integer Column"),
        ...     xi.types.Column("StrCol", dtype=xi.string,
        ...                     alias="Input String Column",
        ...                     update_after_execution=True),
        ...     xi.types.Column("ResultCol", dtype=xi.real,
        ...                     alias="Result Real Column",
        ...                     manage=xi.Manage.RESULT)
        ... ])

        Parameters
        ----------
        index : Union[str, List[str]]
            The name of the index to use, or list of names for multiple indices. The same index may appear in the list
            multiple times.
        columns : Union[Column, List[Column]])
            The columns which make up this data frame.

        Notes
        -----
        This function returns an `Annotated` type containing the `DataFrame` entity object; for example,
        if `xpressinsight` has been imported as `xi`, then
        `xi.types.DataFrame(index='idx', columns=[xi.types.Column("c1", dtype=xi.integer)])` is equivalent to
        `Annotated[pandas.DataFrame, xi.DataFrame(index='idx', columns=[xi.Column("c1", dtype=xi.integer)])]`.

        See Also
        --------
        Column
        types.Index
        """
    entity = xi_entities.DataFrame(
        index=index,
        columns=columns
    )
    return Annotated[pd.DataFrame, entity]
