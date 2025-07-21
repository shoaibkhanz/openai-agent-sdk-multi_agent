from agents import function_tool
import duckdb
from utils.utils import load_data
from configs.config import TRANSACTIONS_PATH


@function_tool
def get_metadata_from_table() -> tuple[list[str], list[str]]:
    """
    Retrieve unique values from the 'types' and 'category' columns of the transactions dataset.

    This function loads the transactions data from the configured path and extracts
    all unique values from both the 'types' and 'category' columns. This metadata
    is useful for understanding the available transaction types and categories
    before performing analysis or filtering operations.

    Returns:
        tuple[list[str], list[str]]: A tuple containing two lists:
            - First list: All unique values from the 'types' column
            - Second list: All unique values from the 'category' column

    Example:
        >>> types, categories = get_metadata_from_table()
        >>> print(f"Available types: {types}")
        >>> print(f"Available categories: {categories}")
        Available types: ['debit', 'credit',]
        Available categories: ['groceries', 'utilities', 'entertainment', ...]

    Note:
        - The function assumes the dataset contains 'types' and 'category' columns
        - Returns all values including duplicates as they appear in the dataset
        - Useful for understanding the data structure before writing SQL queries
    """
    data = load_data(TRANSACTIONS_PATH)
    types = data["type"].unique().tolist()
    categories = data["category"].unique().tolist()
    return types, categories


@function_tool
def get_table_columns() -> list[str]:
    """
    Retrieve the column names from the transactions dataset.

    This function loads the transactions data from the configured path and
    returns a list of all column names available in the dataset. This is
    useful for understanding the structure of the data before writing SQL queries.

    Returns:
        list[str]: A list containing all column names from the transactions dataset.

    Example:
        >>> columns = get_table_columns()
        >>> print(columns)
        ['transaction_id', 'amount', 'date', 'category', ...]
    """
    data = load_data(TRANSACTIONS_PATH)
    columns = data.columns.to_list()
    return columns


@function_tool
def execute_sql(sql_query: str, table_name: str = "transactions") -> str:
    """
    Execute a SQL query against the transactions dataset making sure its compatible with DuckDB SQL.

    This function takes a SQL query string, cleans it by removing any markdown
    code block formatting, and executes it against the loaded transactions data
    using DuckDB. The result is returned as a formatted string representation
    of the resulting DataFrame.

    Args:
        sql_query (str): The SQL query to execute. Can include markdown code
                        block formatting (```sql and ```) which will be automatically
                        stripped before execution.

    Returns:
        str: The query result formatted as a string table, or an error message
             if the query execution fails.

    Example:
        >>> result = execute_sql("SELECT COUNT(*) FROM transactions")
        >>> print(result)
        "   COUNT(*)\n0     1000"

        >>> result = execute_sql("```sql\nSELECT * FROM transactions LIMIT 5\n```")
        >>> print(result)  # Returns first 5 rows as formatted string

    Note:
        - The function automatically loads the transactions data from the configured path
        - SQL queries should reference the table as 'transactions'
        - Any SQL formatting from markdown code blocks is automatically removed
        - Errors in query execution are caught and returned as descriptive error messages
    """
    try:
        data = load_data(TRANSACTIONS_PATH)  # noqa: F841

        # we use duckdb to create a table
        duckdb.sql(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM data")
        sql_query = sql_query.strip()
        sql_query = sql_query.replace("```sql", "").replace("```", "")

        # execute the SQL query
        result = duckdb.sql(sql_query).df()

        # return the result as string
        return result.to_string()
    except Exception as e:
        return f"Error accessing data: {str(e)}"


@function_tool
def addition(x: float, y: float) -> float:
    """
    Add two numbers.

    Args:
        x (float): The first number.
        y (float): The second number.

    Returns:
        float: The sum of the two numbers.
    """
    return float(x) + float(y)


@function_tool
def subtraction(x: float, y: float) -> float:
    """
    Subtract the second number from the first.

    Args:
        x (float): The number to subtract from.
        y (float): The number to be subtracted.

    Returns:
        float: The result of the subtraction.
    """
    return float(x) - float(y)


@function_tool
def division(x: float, y: float) -> float:
    """
    Divide the first number by the second.

    Args:
        x (float): Numerator.
        y (float): Denominator.

    Returns:
        float: The quotient.

    Raises:
        ZeroDivisionError: If y is zero.
    """
    return float(x) / float(y)


@function_tool
def multiplication(x: float, y: float) -> float:
    """
        Multiply two numbers.

        Args:
            x (float): The first number.
            y (float): The second number.
    ,ModelSettings
        Returns:
            float: The product of the two numbers.
    """
    return float(x) * float(y)


@function_tool
def percent_change(x: float, y: float) -> float:
    """
    Calculate the percent change between two values.

    Args:
        x (float): The initial value.
        y (float): The new/final value.

    Returns:
        float: The percent change from x to y.
    """
    if x == 0:
        raise ValueError("Initial value x cannot be zero for percent change.")
    return ((float(y) - float(x)) / abs(float(x))) * 100
