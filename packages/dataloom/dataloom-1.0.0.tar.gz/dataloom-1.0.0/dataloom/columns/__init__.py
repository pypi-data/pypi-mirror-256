from dataloom.types import (
    POSTGRES_SQL_TYPES,
    MYSQL_SQL_TYPES,
    SQLITE3_SQL_TYPES,
    MYSQL_SQL_TYPES_LITERAL,
    POSTGRES_SQL_TYPES_LITERAL,
    SQLITE3_SQL_TYPES_LITERAL,
    CASCADE_LITERAL,
    DIALECT_LITERAL,
    RELATIONSHIP_LITERAL,
)
from dataclasses import dataclass
from dataloom.exceptions import UnsupportedTypeException, UnsupportedDialectException


class CreatedAtColumn:
    def __init__(self):
        pass

    @property
    def created_at(self):
        return "{type} DEFAULT {value}".format(
            type=POSTGRES_SQL_TYPES["timestamp"], value="CURRENT_TIMESTAMP"
        )


class UpdatedAtColumn:
    def __init__(self):
        pass

    @property
    def updated_at(self):
        return "{type} DEFAULT {value}".format(
            type=POSTGRES_SQL_TYPES["timestamp"], value="CURRENT_TIMESTAMP"
        )


@dataclass
class TableColumn:
    name: str


class ForeignKeyColumn:
    def __init__(
        self,
        table,
        type: MYSQL_SQL_TYPES_LITERAL
        | POSTGRES_SQL_TYPES_LITERAL
        | SQLITE3_SQL_TYPES_LITERAL,
        maps_to: RELATIONSHIP_LITERAL = "1-N",
        required: bool = True,
        onDelete: CASCADE_LITERAL = "NO ACTION",
        onUpdate: CASCADE_LITERAL = "NO ACTION",
    ):
        self.table = table
        self.required = required
        self.onDelete = onDelete
        self.onUpdate = onUpdate
        self.type = type
        self.maps_to = maps_to

    def sql_type(self, dialect: DIALECT_LITERAL):
        if dialect == "postgres":
            if self.type in POSTGRES_SQL_TYPES:
                return (
                    f"{POSTGRES_SQL_TYPES[self.type]}({self.length})"
                    if self.length
                    else POSTGRES_SQL_TYPES[self.type]
                )
            else:
                types = POSTGRES_SQL_TYPES.keys()
            raise UnsupportedTypeException(
                f"Unsupported column type: {self.type} for dialect '{dialect}' supported types are ({', '.join(types)})"
            )

        elif dialect == "mysql":
            if self.type in MYSQL_SQL_TYPES:
                if (self.unique or self.default) and self.type == "text":
                    return f"{MYSQL_SQL_TYPES['varchar']}({self.length if self.length is not None else 255})"
                return (
                    f"{MYSQL_SQL_TYPES[self.type]}({self.length})"
                    if self.length
                    else MYSQL_SQL_TYPES[self.type]
                )
            else:
                types = MYSQL_SQL_TYPES.keys()
                raise UnsupportedTypeException(
                    f"Unsupported column type: {self.type} for dialect '{dialect}' supported types are ({', '.join(types)})"
                )
        elif dialect == "sqlite":
            if self.type in SQLITE3_SQL_TYPES:
                if self.length and self.type == "text":
                    return f"{SQLITE3_SQL_TYPES['varchar']}({self.length})"
                return (
                    f"{SQLITE3_SQL_TYPES[self.type]}({self.length})"
                    if self.length
                    else SQLITE3_SQL_TYPES[self.type]
                )
            else:
                types = SQLITE3_SQL_TYPES.keys()
                raise UnsupportedTypeException(
                    f"Unsupported column type: {self.type} for dialect '{dialect}' supported types are ({', '.join(types)})"
                )
        else:
            raise UnsupportedDialectException(
                "The dialect passed is not supported the supported dialects are: {'postgres', 'mysql', 'sqlite'}"
            )


class PrimaryKeyColumn:
    def __init__(
        self,
        type: MYSQL_SQL_TYPES_LITERAL
        | POSTGRES_SQL_TYPES_LITERAL
        | SQLITE3_SQL_TYPES_LITERAL,
        length: int | None = None,
        auto_increment: bool = False,
        nullable: bool = False,
        unique: bool = True,
        default=None,
    ):
        self.type = type
        self.length = length
        self.auto_increment = auto_increment
        self.default = default
        self.nullable = nullable
        self.unique = unique

    @property
    def default_constraint(self):
        return (
            "DEFAULT {default}".format(
                default=(
                    self.default
                    if isinstance(self.default, bool)
                    else f"'{self.default}'"
                )
            )
            if self.default is not None
            else ""
        )

    @property
    def unique_constraint(self):
        return "UNIQUE" if self.unique else ""

    @property
    def nullable_constraint(self):
        return "NOT NULL" if not self.nullable else "NULL"

    def sql_type(self, dialect: DIALECT_LITERAL):
        if dialect == "postgres":
            if self.type in POSTGRES_SQL_TYPES:
                if self.auto_increment:
                    return "BIGSERIAL"
                return (
                    f"{POSTGRES_SQL_TYPES[self.type]}({self.length})"
                    if self.length
                    else POSTGRES_SQL_TYPES[self.type]
                )
            else:
                types = POSTGRES_SQL_TYPES.keys()
            raise UnsupportedTypeException(
                f"Unsupported column type: {self.type} for dialect '{dialect}' supported types are ({', '.join(types)})"
            )

        elif dialect == "mysql":
            if self.type in MYSQL_SQL_TYPES:
                if (self.unique or self.default) and self.type == "text":
                    return f"{MYSQL_SQL_TYPES['varchar']}({self.length if self.length is not None else 255})"
                return (
                    f"{MYSQL_SQL_TYPES[self.type]}({self.length})"
                    if self.length
                    else MYSQL_SQL_TYPES[self.type]
                )
            else:
                types = MYSQL_SQL_TYPES.keys()
                raise UnsupportedTypeException(
                    f"Unsupported column type: {self.type} for dialect '{dialect}' supported types are ({', '.join(types)})"
                )
        elif dialect == "sqlite":
            if self.type in SQLITE3_SQL_TYPES:
                return SQLITE3_SQL_TYPES[self.type]
            else:
                types = SQLITE3_SQL_TYPES.keys()
                raise UnsupportedTypeException(
                    f"Unsupported column type: {self.type} for dialect '{dialect}' supported types are ({', '.join(types)})"
                )
        else:
            raise UnsupportedDialectException(
                "The dialect passed is not supported the supported dialects are: {'postgres', 'mysql', 'sqlite'}"
            )


class Column:
    def __init__(
        self,
        type: MYSQL_SQL_TYPES_LITERAL
        | POSTGRES_SQL_TYPES_LITERAL
        | SQLITE3_SQL_TYPES_LITERAL,
        nullable: bool = True,
        unique: bool = False,
        length: int | None = None,
        auto_increment: bool = False,
        default=None,
    ):
        self.type = type
        self.nullable = nullable
        self.unique = unique
        self.length = length
        self.auto_increment = auto_increment
        self.default = default

        self._data = {}

    def __str__(self) -> str:
        return ""

    @property
    def nullable_constraint(self):
        return "NOT NULL" if not self.nullable else ""

    @property
    def unique_constraint(self):
        return "UNIQUE" if self.unique else ""

    @property
    def default_constraint(self):
        return (
            "DEFAULT {default}".format(
                default=(
                    self.default
                    if isinstance(self.default, bool)
                    else f"'{self.default}'"
                )
            )
            if self.default is not None
            else ""
        )

    def sql_type(self, dialect: DIALECT_LITERAL):
        if dialect == "postgres":
            if self.type in POSTGRES_SQL_TYPES:
                return (
                    f"{POSTGRES_SQL_TYPES[self.type]}({self.length})"
                    if self.length
                    else POSTGRES_SQL_TYPES[self.type]
                )
            else:
                types = POSTGRES_SQL_TYPES.keys()
            raise UnsupportedTypeException(
                f"Unsupported column type: {self.type} for dialect '{dialect}' supported types are ({', '.join(types)})"
            )

        elif dialect == "mysql":
            if self.type in MYSQL_SQL_TYPES:
                if (self.unique or self.default) and self.type == "text":
                    return f"{MYSQL_SQL_TYPES['varchar']}({self.length if self.length is not None else 255})"
                return (
                    f"{MYSQL_SQL_TYPES[self.type]}({self.length})"
                    if self.length
                    else MYSQL_SQL_TYPES[self.type]
                )
            else:
                types = MYSQL_SQL_TYPES.keys()
                raise UnsupportedTypeException(
                    f"Unsupported column type: {self.type} for dialect '{dialect}' supported types are ({', '.join(types)})"
                )
        elif dialect == "sqlite":
            if self.type in SQLITE3_SQL_TYPES:
                return SQLITE3_SQL_TYPES[self.type]
            else:
                types = SQLITE3_SQL_TYPES.keys()
                raise UnsupportedTypeException(
                    f"Unsupported column type: {self.type} for dialect '{dialect}' supported types are ({', '.join(types)})"
                )
        else:
            raise UnsupportedDialectException(
                "The dialect passed is not supported the supported dialects are: {'postgres', 'mysql', 'sqlite'}"
            )
