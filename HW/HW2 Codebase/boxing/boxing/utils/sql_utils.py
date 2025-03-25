from contextlib import contextmanager
import logging
import os
import sqlite3

from boxing.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


# load the db path from the environment with a default value
DB_PATH = os.getenv("DB_PATH", "/app/sql/boxing.db")


def check_database_connection():
    """
    Checks if a connection to the SQLite database can be established.

    Raises:
        Exception: If there is a problem connecting to the database or executing the query.
    """
    try:
        logger.info("Attempting to conenct to the SQLite database.")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Execute a simple query to verify the connection is active
        cursor.execute("SELECT 1;")
        conn.close()
        logger.info("Successfully connected to backend database.")
    except sqlite3.Error as e:
        logger.error("Was not able to connect to the database.")
        error_message = f"Database connection error: {e}"
        raise Exception(error_message) from e

def check_table_exists(tablename: str):
    """
    Checks if the inputted tablename exists in the sqlite database.

    Args:
        tablename (str): The name of the table to search for in the database.
    
    Raises:
        Exception: If the table doesn't exist or there was an error when checking.
        sqlite3.Error: If there is an error when checking the table.
    """
    try:
        logger.info("Attempting to connect to the database.")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Use parameterized query to avoid SQL injection
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (tablename,))
        result = cursor.fetchone()

        conn.close()
        logger.info("Successfully connected to the database.")
        if result is None:
            logger.warning(f"Table '{tablename}' does not exist in the database.")
            error_message = f"Table '{tablename}' does not exist."
            raise Exception(error_message)

    except sqlite3.Error as e:
        error_message = f"Table check error for '{tablename}': {e}"
        logger.warning(error_message)
        raise Exception(error_message) from e

@contextmanager
def get_db_connection():
    """
    Establishes a connection to the sqlite database.

    Raises:
        sqlite3.Error: If there is any error when attempting to connect to the backend.
    """
    conn = None
    try:
        logger.info(f"Attempts to connect to database at {DB_PATH}.")
        conn = sqlite3.connect(DB_PATH)
        yield conn
    except sqlite3.Error as e:
        logger.warning(f"Issue with connecting to the database backend at {DB_PATH}")
        raise e
    finally:
        if conn:
            conn.close()
            logger.warning(f"Connection to databse closed.")
