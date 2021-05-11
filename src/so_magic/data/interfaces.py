"""Defines interfaces related to various operations on table-like data."""
from abc import abstractmethod, ABC
from typing import Union, Iterable


__all__ = ['TabularIterator', 'TabularRetriever', 'TabularMutator']


class TabularRetriever(ABC):
    """Operations on table-like data.

    Classes implementing this interface gain the ability to perform various operations
    on data structures that resemble a table (have indexable columns, rows, etc):

    most importantly they can slice through the data (retrieve specific row or column)
    """
    @abstractmethod
    def column(self, identifier: Union[str, int], data) -> Iterable:
        """Slice though the data (table) and get the specified column's values.

        Args:
            identifier (Union[str, int]): unique identifier/index of column
            data (object): the data to slice through

        Returns:
            Iterable: the values contained in the column requested
        """
        raise NotImplementedError

    @abstractmethod
    def row(self, identifier, data):
        """Slice though the data (table) and get the specified row's values.

        Args:
            identifier (Union[str, int]): unique identifier/index of row
            data (object): the data to slice through

        Returns:
            Iterable: the values contained in the row requested
        """
        raise NotImplementedError

    @abstractmethod
    def nb_columns(self, data) -> int:
        """Get the number of columns that the data (table) have.

        Args:
            data (object): the data (table) to count its columns

        Returns:
            int: the number of the (data) table's columns
        """
        raise NotImplementedError

    @abstractmethod
    def nb_rows(self, data) -> int:
        """Get the number of rows that the data (table) have.

        Args:
            data (object): the data (table) to count its rows

        Returns:
            int: the number of the (data) table's rows
        """
        raise NotImplementedError

    @abstractmethod
    def get_numerical_attributes(self, data) -> Iterable:
        r"""Get the data's attributes that represent numerical values.

        Returns the attributes that fall under the Numerical Variables: either
        Ratio or Interval type of variables.

        Two type of numerical variables are supported:

        Ratio variable:
        numerical variable where all operations are supported (+, -, \*, /) and true zero is defined; eg weight.

        Interval variable:
        numerical variable where differences are interpretable; supported operations: [+, -]; no true zero;
        eg temperature in centigrade (ie Celsius).

        Args:
            data (object): the data from which to retrieve the numerical attributes

        Returns:
            Iterable: the numerical attributes found
        """
        raise NotImplementedError


class TabularIterator(ABC):
    """Iterate over the rows or columns of a table-lie data structure.

    Classes implementing this interface gain the ability to iterate over the values
    found in the rows or the columns of a table-like data structure.
    They can also iterate over the columns indices/identifiers.
    """
    @abstractmethod
    def iterrows(self, data) -> Iterable:
        """Iterate over the (data) table's rows.

        Get an iterable over the table's rows.

        Args:
            data (object): the (data) table to iterate over its rows

        Returns:
            Iterable: the rows of the (data) table
        """
        raise NotImplementedError

    @abstractmethod
    def itercolumns(self, data) -> Iterable:
        """Iterate over the (data) table's columns.

        Get an iterable over the table's columns.

        Args:
            data (object): the (data) table to iterate over its columns

        Returns:
            Iterable: the columns of the (data) table
        """
        raise NotImplementedError

    @abstractmethod
    def columnnames(self, data) -> Union[Iterable[str], Iterable[int]]:
        """Iterate over data (table) column indices/identifiers.

        Args:
            data (object): the (data) table to iterate over its columns indices/identifiers

        Returns:
            Union[Iterable[str], Iterable[int]]: the column indices/identifiers of the (data) table
        """
        raise NotImplementedError


class TabularMutator(ABC):
    """Mutate (alter) the contents of a table-like data structure.

    Classes implementing this interface supply their instances the ability to alter the
    contents of a table-like data structure.
    """
    @abstractmethod
    def add_column(self, *args, **kwargs):
        """Add a new column to table-like data.

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError
