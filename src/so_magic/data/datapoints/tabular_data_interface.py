"""This module defines the TabularDataInterface interface."""
from typing import Union, Iterable
from abc import ABC, abstractmethod


__all__ = ['TabularDataInterface']


class TabularDataInterface(ABC):
    """Data points that have tabular structure and are loaded in memory.

    Classes implementing this interface represent Data points that can be represented
    as a table of rows an columns. One can imagine that each row (or column) represents a single observation
    (single data point) and each column (or row) one single attribute out of possibly many attributes.

    Classes implementing this interface have the ability to report on various
    elements and properties (eg rows, columns) of the underlying table-like data-structure.
    """

    @property
    @abstractmethod
    def columns(self) -> Iterable:
        """List of the column identifiers."""
        raise NotImplementedError

    @property
    @abstractmethod
    def rows(self) -> Iterable:
        """List of the row identifiers."""
        raise NotImplementedError

    @abstractmethod
    def column(self, identifier: Union[str, int]) -> Iterable:
        """Get the data inside a column of the table.

        Args:
            identifier (Union[str, int]): a primitive identifier to distinguish between the columns

        Returns:
            Iterable: the data contained in the table's requested column
        """
        raise NotImplementedError

    @abstractmethod
    def row(self, identifier: Union[str, int]) -> Iterable:
        """Get the data inside a row of the table.

        Args:
            identifier (Union[str, int]): a primitive identifier to distinguish between the rows

        Returns:
            Iterable: the data contained in the table's requested row
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def nb_columns(self) -> int:
        """The number of the table's columns.

        Returns:
            int: the number of columns
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def nb_rows(self) -> int:
        """The number of the table's rows.

        Returns:
            int: the number of rows
        """
        raise NotImplementedError

    @abstractmethod
    def iterrows(self) -> Iterable:
        """Iterate over the table's rows."""
        raise NotImplementedError

    @abstractmethod
    def itercolumns(self) -> Iterable:
        """Iterate over the table's columns."""
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        """The table's length as the number of rows."""
        raise NotImplementedError

    @abstractmethod
    def __iter__(self) -> Iterable:
        """Iterate over the table's rows."""
        raise NotImplementedError
