from typing_extensions import Literal, Any
from dataclasses import dataclass, field
from typing import Optional

OPERATOR_LITERAL = Literal["eq", "neq", "lt", "gt", "leq", "geq", "in", "notIn", "like"]
SLQ_OPERAND_LITERAL = Literal["AND", "OR"]
INCREMENT_DECREMENT_LITERAL = Literal["increment", "decrement"]
SQL_LOGGER_LITERAL = Literal["console", "file"]

CASCADE_LITERAL = Literal["NO ACTION", "CASCADE", "SET NULL"]
DIALECT_LITERAL = Literal["postgres", "mysql", "sqlite"]
RELATIONSHIP_LITERAL = Literal["1-1", "1-N", "N-1", "N-N"]


SLQ_OPERATORS = {
    "eq": "=",
    "neq": "!=",
    "lt": "<",
    "gt": ">",
    "leq": "<=",
    "geq": ">=",
    "in": "IN",
    "notIn": "NOT IN",
    "like": "LIKE",
}
SLQ_OPERAND = {
    "AND": "AND",
    "OR": "OR",
}


@dataclass(kw_only=True, repr=False)
class Filter:
    """
    Filter
    ------

    Constructor method for the Filter class.

    Parameters
    ----------
    column : str
        The name of the column to filter on.
    operator : "eq" |"neq" |"lt" |"gt" |"leq" |"geq" |"in" |"notIn" |"like"
        The operator to use for the filter.
    value : Any
        The value to compare against.
    join_next_filter_with : "AND" | "OR" | None, optional
        The SQL operand to join the next filter with. Default is "AND".

    Returns
    -------
    None
        This method does not return any value.

    See Also
    --------
    ColumnValue : Class for defining column values.
    Order : Class for defining order specifications.

    Examples
    --------
    >>> from dataloom import Filter, ColumnValue, Order, User
    ...
    ... # Creating a filter for users with id equals 1 or username equals 'miller'
    ... affected_rows = loom.update_one(
    ...     User,
    ...     filters=[
    ...         Filter(column="id", value=1, operator="eq", join_next_filter_with="OR"),
    ...         Filter(column="username", value="miller"),
    ...     ],
    ...     values=[
    ...         [
    ...             ColumnValue(name="username", value="Mario"),
    ...             ColumnValue(name="name", value="Mario"),
    ...         ]
    ...     ],
    ... )
    ... print(affected_rows)

    """

    column: str = field(repr=False)
    operator: OPERATOR_LITERAL = field(repr=False, default="eq")
    value: Any = field(repr=False)
    join_next_filter_with: Optional[SLQ_OPERAND_LITERAL] = field(default="AND")

    def __init__(
        self,
        column: str,
        value: Any,
        operator: OPERATOR_LITERAL = "eq",
        join_next_filter_with: Optional[SLQ_OPERAND_LITERAL] = "AND",
    ) -> None:
        """
        Filter
        ------

        Constructor method for the Filter class.

        Parameters
        ----------
        column : str
            The name of the column to filter on.
        operator : "eq" |"neq" |"lt" |"gt" |"leq" |"geq" |"in" |"notIn" |"like"
            The operator to use for the filter.
        value : Any
            The value to compare against.
        join_next_filter_with : "AND" | "OR" | None, optional
            The SQL operand to join the next filter with. Default is "AND".

        Returns
        -------
        None
            This method does not return any value.

        See Also
        --------
        ColumnValue : Class for defining column values.
        Order : Class for defining order specifications.

        Examples
        --------
        >>> from dataloom import Filter, ColumnValue, Order, User
        ...
        ... # Creating a filter for users with id equals 1 or username equals 'miller'
        ... affected_rows = loom.update_one(
        ...     User,
        ...     filters=[
        ...         Filter(column="id", value=1, operator="eq", join_next_filter_with="OR"),
        ...         Filter(column="username", value="miller"),
        ...     ],
        ...     values=[
        ...         [
        ...             ColumnValue(name="username", value="Mario"),
        ...             ColumnValue(name="name", value="Mario"),
        ...         ]
        ...     ],
        ... )
        ... print(affected_rows)

        """
        self.column = column
        self.value = value
        self.join_next_filter_with = join_next_filter_with
        self.operator = operator


@dataclass(kw_only=True, repr=False)
class ColumnValue[T]:
    """
    ColumnValue
    -----------

    Constructor method for the ColumnValue class.

    Parameters
    ----------
    name : str
        The name of the column.
    value : Any
        The value to assign to the column.

    Returns
    -------
    None
        This method does not return any value.

    See Also
    --------
    Filter : Class for defining filters.
    Order : Class for defining order specifications.

    Examples
    --------
    >>> from dataloom import ColumnValue, Filter, Order
    ...
    ... # Model definitions
    ... class User(Model):
    ...     __tablename__: Optional[TableColumn] = TableColumn(name="users")
    ...     id = PrimaryKeyColumn(type="int", auto_increment=True)
    ...     name = Column(type="text", nullable=False)
    ...     username = Column(type="varchar", unique=True, length=255)
    ...
    ... class Post(Model):
    ...     __tablename__: Optional[TableColumn] = TableColumn(name="posts")
    ...     id = PrimaryKeyColumn(type="int", auto_increment=True)
    ...     title = Column(type="text", nullable=False)
    ...     content = Column(type="text", nullable=False)
    ...     userId = ForeignKeyColumn(User, maps_to="1-N", type="int", required=False, onDelete="CASCADE", onUpdate="CASCADE")
    ...
    ... # Updating the username and name columns for the user with ID 1
    ... affected_rows = loom.update_one(
    ...     User,
    ...     filters=Filter(column="id", value=1),
    ...     values=[
    ...         [
    ...             ColumnValue(name="username", value="Mario"),
    ...             ColumnValue(name="name", value="Mario"),
    ...         ]
    ...     ],
    ... )
    ... print(affected_rows)

    """

    name: str = field(repr=False)
    value: T = field(repr=False)

    def __init__(self, name: str, value: T) -> None:
        """
        ColumnValue
        -----------

        Constructor method for the ColumnValue class.

        Parameters
        ----------
        name : str
            The name of the column.
        value : Any
            The value to assign to the column.

        Returns
        -------
        None
            This method does not return any value.

        See Also
        --------
        Filter : Class for defining filters.
        Order : Class for defining order specifications.

        Examples
        --------
        >>> from dataloom import ColumnValue, Filter, Order
        ...
        ... # Model definitions
        ... class User(Model):
        ...     __tablename__: Optional[TableColumn] = TableColumn(name="users")
        ...     id = PrimaryKeyColumn(type="int", auto_increment=True)
        ...     name = Column(type="text", nullable=False)
        ...     username = Column(type="varchar", unique=True, length=255)
        ...
        ... class Post(Model):
        ...     __tablename__: Optional[TableColumn] = TableColumn(name="posts")
        ...     id = PrimaryKeyColumn(type="int", auto_increment=True)
        ...     title = Column(type="text", nullable=False)
        ...     content = Column(type="text", nullable=False)
        ...     userId = ForeignKeyColumn(User, maps_to="1-N", type="int", required=False, onDelete="CASCADE", onUpdate="CASCADE")
        ...
        ... # Updating the username and name columns for the user with ID 1
        ... affected_rows = loom.update_one(
        ...     User,
        ...     filters=Filter(column="id", value=1),
        ...     values=[
        ...         [
        ...             ColumnValue(name="username", value="Mario"),
        ...             ColumnValue(name="name", value="Mario"),
        ...         ]
        ...     ],
        ... )
        ... print(affected_rows)

        """
        self.name = name
        self.value = value


@dataclass(kw_only=True, repr=False)
class Order:
    """
    Order
    -----

    Constructor method for the Order class.

    Parameters
    ----------
    column : str
        The name of the column to order by.
    order : Literal['ASC', 'DESC'], optional
        The order direction. Default is "ASC" (ascending).

    Returns
    -------
    None
        This method does not return any value.

    See Also
    --------
    Include : Class for defining included models.
    Filter : Class for defining filters.
    ColumnValue : Class for defining column values.

    Examples
    --------
    >>> from dataloom import Order, Include, Model
    ...
    ... class User(Model):
    ...     __tablename__: Optional[TableColumn] = TableColumn(name="users")
    ...     id = PrimaryKeyColumn(type="int", auto_increment=True)
    ...     name = Column(type="text", nullable=False)
    ...     username = Column(type="varchar", unique=True, length=255)
    ...
    ... class Post(Model):
    ...     __tablename__: Optional[TableColumn] = TableColumn(name="posts")
    ...     id = PrimaryKeyColumn(type="int", auto_increment=True)
    ...     title = Column(type="text", nullable=False)
    ...     content = Column(type="text", nullable=False)
    ...     userId = ForeignKeyColumn(User, maps_to="1-N", type="int", required=False, onDelete="CASCADE", onUpdate="CASCADE")
    ...
    ... # Including posts for a user with ID 1 and ordering by ID in descending order
    ... # and then by createdAt in descending order
    ... users = loom.find_many(
    ...     User,
    ...     pk=1,
    ...     include=[Include(Post, limit=2, offset=0, maps_to="1-N")],
    ...     order=[Order(column="id", order="DESC"), Order(column="createdAt", order="DESC")]
    ... )

    """

    column: str = field(repr=False)
    order: Literal["ASC", "DESC"] = field(repr=False, default="ASC")

    def __init__(self, column: str, order: Literal["ASC", "DESC"] = "ASC") -> None:
        """
        Order
        -----

        Constructor method for the Order class.

        Parameters
        ----------
        column : str
            The name of the column to order by.
        order : Literal['ASC', 'DESC'], optional
            The order direction. Default is "ASC" (ascending).

        Returns
        -------
        None
            This method does not return any value.

        See Also
        --------
        Include : Class for defining included models.
        Filter : Class for defining filters.
        ColumnValue : Class for defining column values.

        Examples
        --------
        >>> from dataloom import Order, Include, Model
        ...
        ... class User(Model):
        ...     __tablename__: Optional[TableColumn] = TableColumn(name="users")
        ...     id = PrimaryKeyColumn(type="int", auto_increment=True)
        ...     name = Column(type="text", nullable=False)
        ...     username = Column(type="varchar", unique=True, length=255)
        ...
        ... class Post(Model):
        ...     __tablename__: Optional[TableColumn] = TableColumn(name="posts")
        ...     id = PrimaryKeyColumn(type="int", auto_increment=True)
        ...     title = Column(type="text", nullable=False)
        ...     content = Column(type="text", nullable=False)
        ...     userId = ForeignKeyColumn(User, maps_to="1-N", type="int", required=False, onDelete="CASCADE", onUpdate="CASCADE")
        ...
        ... # Including posts for a user with ID 1 and ordering by ID in descending order
        ... # and then by createdAt in descending order
        ... users = loom.find_many(
        ...     User,
        ...     pk=1,
        ...     include=[Include(Post, limit=2, offset=0, maps_to="1-N")],
        ...     order=[Order(column="id", order="DESC"), Order(column="createdAt", order="DESC")]
        ... )

        """
        self.column = column
        self.order = order


@dataclass(kw_only=True, repr=False)
class Include[Model]:
    """
    Include
    -------

    Constructor method for the Include class.

    Parameters
    ----------
    model : Model
        The model to be included when eger fetching records.
    order : list[Order], optional
        The list of order specifications for sorting the included data. Default is an empty list.
    limit : int | None, optional
        The maximum number of records to include. Default is 0 (no limit).
    offset : int | None, optional
        The number of records to skip before including. Default is 0 (no offset).
    select : list[str] | None, optional
        The list of columns to include. Default is None (include all columns).
    maps_to : RELATIONSHIP_LITERAL, optional
        The relationship type between the current model and the included model. Default is "1-N" (one-to-many).

    Returns
    -------
    None
        This method does not return any value.

    See Also
    --------
    Order: Class for defining order specifications.
    Filter : Class for defining filters.
    ColumnValue : Class for defining column values.

    Examples
    --------
    >>> from dataloom import Include, Model, Order
    ...
    ... # Including posts for a user with ID 1
    ... mysql_loom.find_by_pk(
    ...     User, pk=1, include=[Include(Post, limit=2, offset=0, select=["id", "title"], maps_to="1-N")]
    ... )

    """

    model: Model = field(repr=False)
    order: list[Order] = field(repr=False, default_factory=list)
    limit: Optional[int] = field(default=0)
    offset: Optional[int] = field(default=0)
    select: Optional[list[str]] = field(default_factory=list)
    maps_to: RELATIONSHIP_LITERAL = field(default="1-N")

    def __init__(
        self,
        model: Model,
        order: list[Order] = [],
        limit: Optional[int] = 0,
        offset: Optional[int] = 0,
        select: Optional[list[str]] = [],
        maps_to: RELATIONSHIP_LITERAL = "1-N",
    ):
        """
        Include
        -------

        Constructor method for the Include class.

        Parameters
        ----------
        model : Model
            The model to be included when eger fetching records.
        order : list[Order], optional
            The list of order specifications for sorting the included data. Default is an empty list.
        limit : int | None, optional
            The maximum number of records to include. Default is 0 (no limit).
        offset : int | None, optional
            The number of records to skip before including. Default is 0 (no offset).
        select : list[str] | None, optional
            The list of columns to include. Default is None (include all columns).
        maps_to : RELATIONSHIP_LITERAL, optional
            The relationship type between the current model and the included model. Default is "1-N" (one-to-many).

        Returns
        -------
        None
            This method does not return any value.

        See Also
        --------
        Order: Class for defining order specifications.
        Filter : Class for defining filters.
        ColumnValue : Class for defining column values.

        Examples
        --------
        >>> from dataloom import Include, Model, Order
        ...
        ... # Including posts for a user with ID 1
        ... loom.find_by_pk(
        ...     User, pk=1, include=[Include(Post, limit=2, offset=0, select=["id", "title"], maps_to="1-N")]
        ... )

        """

        self.select = select
        self.model = model
        self.order = order
        self.limit = limit
        self.offset = offset
        self.maps_to = maps_to


POSTGRES_SQL_TYPES = {
    "int": "INTEGER",
    "smallint": "SMALLINT",
    "bigint": "BIGINT",
    "serial": "SERIAL",
    "bigserial": "BIGSERIAL",
    "smallserial": "SMALLSERIAL",
    "float": "REAL",
    "double precision": "DOUBLE PRECISION",
    "numeric": "NUMERIC",
    "text": "TEXT",
    "varchar": "VARCHAR",
    "char": "CHAR",
    "boolean": "BOOLEAN",
    "date": "DATE",
    "time": "TIME",
    "timestamp": "TIMESTAMP",
    "interval": "INTERVAL",
    "uuid": "UUID",
    "json": "JSON",
    "jsonb": "JSONB",
    "bytea": "BYTEA",
    "array": "ARRAY",
    "inet": "INET",
    "cidr": "CIDR",
    "macaddr": "MACADDR",
    "tsvector": "TSVECTOR",
    "point": "POINT",
    "line": "LINE",
    "lseg": "LSEG",
    "box": "BOX",
    "path": "PATH",
    "polygon": "POLYGON",
    "circle": "CIRCLE",
    "hstore": "HSTORE",
}

POSTGRES_SQL_TYPES_LITERAL = Literal[
    "int",
    "smallint",
    "bigint",
    "serial",
    "bigserial",
    "smallserial",
    "float",
    "double precision",
    "numeric",
    "text",
    "varchar",
    "char",
    "boolean",
    "date",
    "time",
    "timestamp",
    "interval",
    "uuid",
    "json",
    "jsonb",
    "bytea",
    "array",
    "inet",
    "cidr",
    "macaddr",
    "tsvector",
    "point",
    "line",
    "lseg",
    "box",
    "path",
    "polygon",
    "circle",
    "hstore",
]

MYSQL_SQL_TYPES = {
    "int": "INT",
    "smallint": "SMALLINT",
    "bigint": "BIGINT",
    "float": "FLOAT",
    "double": "DOUBLE",
    "numeric": "DECIMAL",
    "text": "TEXT",
    "varchar": "VARCHAR",
    "char": "CHAR",
    "boolean": "BOOLEAN",
    "date": "DATE",
    "time": "TIME",
    "timestamp": "TIMESTAMP",
    "json": "JSON",
    "blob": "BLOB",
}
MYSQL_SQL_TYPES_LITERAL = Literal[
    "int",
    "smallint",
    "bigint",
    "float",
    "double",
    "numeric",
    "text",
    "varchar",
    "char",
    "boolean",
    "date",
    "time",
    "timestamp",
    "json",
    "blob",
]

SQLITE3_SQL_TYPES = {
    "int": "INTEGER",
    "smallint": "SMALLINT",
    "bigint": "BIGINT",
    "float": "REAL",
    "double precision": "DOUBLE",
    "numeric": "NUMERIC",
    "text": "TEXT",
    "varchar": "VARCHAR",
    "char": "CHAR",
    "boolean": "BOOLEAN",
    "date": "DATE",
    "time": "TIME",
    "timestamp": "TIMESTAMP",
    "json": "JSON",
    "blob": "BLOB",
}

SQLITE3_SQL_TYPES_LITERAL = Literal[
    "int",
    "smallint",
    "bigint",
    "float",
    "double precision",
    "numeric",
    "text",
    "varchar",
    "char",
    "boolean",
    "date",
    "time",
    "timestamp",
    "json",
    "blob",
]
