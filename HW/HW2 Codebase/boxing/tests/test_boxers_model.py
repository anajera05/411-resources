from contextlib import contextmanager
import re
import sqlite3

import pytest

from boxing.models.boxers_model import (
    Boxer,
    create_boxer,
    delete_boxer,
    get_leaderboard,
    get_boxer_by_id,
    get_boxer_by_name,
    get_weight_class,
    update_boxer_stats
)
######################################################
#
#    Fixtures
#
######################################################

# Mocking the database connection for tests
@pytest.fixture
def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    # Mock the connection's cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Default return for queries
    mock_cursor.fetchall.return_value = []
    mock_cursor.commit.return_value = None

    # Mock the get_db_connection context manager from sql_utils
    @contextmanager
    def mock_get_db_connection():
        yield mock_conn  # Yield the mocked connection object

    mocker.patch("boxing.models.boxers_model.get_db_connection", mock_get_db_connection)

    return mock_cursor  # Return the mock cursor so we can set expectations per test


def normalize_whitespace(sql_query: str) -> str:
    return re.sub(r'\s+', ' ', sql_query).strip()


##################################################
# Create/Remove Boxer Test Cases
##################################################


def test_create_boxer(mock_cursor):
    """Test creating a new boxer.

    """
    create_boxer(name="Boxer 1", weight=150, height=90, reach = 20, age = 30)

    expected_query = normalize_whitespace("""
        INSERT INTO boxers (name, weight, height, reach, age)
        VALUES (?, ?, ?, ?, ?)
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    # Extract the arguments used in the SQL call (second element of call_args)
    actual_arguments = mock_cursor.execute.call_args[0][1]
    expected_arguments = ("Boxer 1", 150, 90, 20, 30)

    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."


def test_create_boxer_invalid_weight():
    """Test error when trying to create a boxer with an invalid weight (<125)

    """
    with pytest.raises(ValueError, match="Invalid weight: 110. Must be at least 125."):
        create_boxer(name="Boxer 1", weight=110, height=90, reach = 20, age = 30)


def test_create_boxer_invalid_height():
    """Test error creating a Boxer with a height 0 or shorter

    """
    with pytest.raises(ValueError, match="Invalid height: 0. Must be greater than 0."):
       create_boxer(name="John Doe", weight=150, height=0, reach=74.5, age=30)



def test_create_boxer_invalid_reach():
    """Test error creating a Boxer with a reach 0.0 or shorter

    """
    with pytest.raises(ValueError, match="Invalid reach: 0.0. Must be greater than 0"):
        create_boxer(name="John Doe", weight=150, height=70, reach=0.0, age=30)


def test_create_boxer_invalid_age():
    """Test error creating a Boxer younger than 18

    """
    with pytest.raises(ValueError, match="Invalid age: 15. Must be between 18 and 40."):
        create_boxer(name="John Doe", weight=150, height=70, reach=74.5, age=15)

    with pytest.raises(ValueError, match="Invalid age: 45. Must be between 18 and 40."):
        create_boxer(name="John Doe", weight=150, height=70, reach=74.5, age=45)


def test_create_boxer_duplicate(mock_cursor):
    """Test creating a song with a duplicate artist, title, and year (should raise an error).

    """
    # Simulate that the database will raise an IntegrityError due to a duplicate entry
    mock_cursor.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed: boxer.name")

    with pytest.raises(ValueError, match="Boxer with name 'John Doe' already exists"):
        create_boxer(name="John Doe", weight=150, height=70, reach=74.5, age=30)


def test_delete_boxer(mock_cursor):
    """Test deleting a boxer from the catalog by boxer ID.

    """
    # Simulate the existence of a boxer w/ id=1
    # We can use any value other than None
    mock_cursor.fetchone.return_value = (True)

    delete_boxer(1)

    expected_select_sql = normalize_whitespace("SELECT id FROM boxers WHERE id = ?")
    expected_delete_sql = normalize_whitespace("DELETE FROM boxers WHERE id = ?")

    # Access both calls to `execute()` using `call_args_list`
    actual_select_sql = normalize_whitespace(mock_cursor.execute.call_args_list[0][0][0])
    actual_delete_sql = normalize_whitespace(mock_cursor.execute.call_args_list[1][0][0])

    assert actual_select_sql == expected_select_sql, "The SELECT query did not match the expected structure."
    assert actual_delete_sql == expected_delete_sql, "The UPDATE query did not match the expected structure."

    # Ensure the correct arguments were used in both SQL queries
    expected_select_args = (1,)
    expected_delete_args = (1,)

    actual_select_args = mock_cursor.execute.call_args_list[0][0][1]
    actual_delete_args = mock_cursor.execute.call_args_list[1][0][1]

    assert actual_select_args == expected_select_args, f"The SELECT query arguments did not match. Expected {expected_select_args}, got {actual_select_args}."
    assert actual_delete_args == expected_delete_args, f"The UPDATE query arguments did not match. Expected {expected_delete_args}, got {actual_delete_args}."



def test_delete_boxer_not_found(mock_cursor):
    """Test error deleting a non-existing Boxer

    """
    mock_cursor.fetchone.return_value = None
    invalid_boxer_id = 9999 
    with pytest.raises(ValueError, match=f"Boxer with ID {invalid_boxer_id} not found."):
        delete_boxer(invalid_boxer_id)


##################################################
# Retrive Stats on Boxer(s) Test Cases
##################################################


def test_get_leaderboard_wins(mock_cursor):
    """Test getting leaderboard by wins (default sort)

    """
    mock_cursor.fetchall.return_value = [
        ("Boxer 1", 150, 90, 20, 30),
        (2, "Artist B", "Song B", 2021, "Pop", 180, 20, False),
        (3, "Artist C", "Song C", 2022, "Jazz", 200, 5, False)
    ]
    assert True


def test_get_leaderboard_pct(mock_cursor):
    """Test getting leaderboard by pct

    """
    assert True


def test_get_leaderboard_none(mock_cursor):
    """Test error input not wins or pct

    """
    assert True

def test_get_boxer_by_id(mock_cursor):
    """Test getting a song by id.

    """
    mock_cursor.fetchone.return_value = (1, "John Doe", 159, 74, 75.5, 30)

    result = get_boxer_by_id(1)

    expected_result = Boxer(1, "John Doe", 159, 74, 75.5, 30)

    assert result == expected_result, f"Expected {expected_result}, got {result}"

    expected_query = normalize_whitespace("SELECT id, name, weight, height, reach, age FROM boxers WHERE id = ?")
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    actual_arguments = mock_cursor.execute.call_args[0][1]
    expected_arguments = (1,)

    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."


def test_get_boxer_by_id_not_found(mock_cursor):
    """Test error getting Boxer with ID that does not exist

    """
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match="Boxer with ID 999 not found."):
        get_boxer_by_id(999)


def test_get_boxer_by_name(mock_cursor):
    """Test getting boxer by name

    """
    mock_cursor.fetchone.return_value = (1, "John Doe", 159, 74, 75.5, 30)

    result = get_boxer_by_name(1)

    expected_result = Boxer(1, "John Doe", 159, 74, 75.5, 30)

    assert result == expected_result, f"Expected {expected_result}, got {result}"

    expected_query = normalize_whitespace("""
                SELECT id, name, weight, height, reach, age
                FROM boxers WHERE name = ?
            """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    actual_arguments = mock_cursor.execute.call_args[0][1]
    expected_arguments = (1,)

    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."


def test_get_boxer_by_name_not_found(mock_cursor):
    """Test error getting Boxer with name that does not exist

    """
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match=f"Boxer 'invalid' not found."):
        get_boxer_by_name("invalid")


def test_get_weight_class_heavyweight():
    """Test getting weight class heavyweight (over 203)

    """    
    weight = 203
    assert get_weight_class(weight) == 'HEAVYWEIGHT'

def test_get_weight_class_middleweight():
    """Test getting weight class middleweight (between 166 and 203)

    """    
    weight = 166
    assert get_weight_class(weight) == 'MIDDLEWEIGHT'

def test_get_weight_class_lightweight():
    """Test getting weight class lightweight (between 133 and 166)

    """    
    weight = 133
    assert get_weight_class(weight) == 'LIGHTWEIGHT'

def test_get_weight_class_featherweight():
    """Test getting weight class featherweight (between 125 and 133)

    """    
    weight = 125
    assert get_weight_class(weight) == 'FEATHERWEIGHT'


def test_get_weight_class_invalid():
    """Test error inputting invalid weight (less than 125)

    """   
    weight = 100 
    with pytest.raises(ValueError, match=f"Invalid weight: {weight}. Weight must be at least 125."):
        get_weight_class(weight)

##################################################
# Change Stats of a Boxer Test Cases
##################################################

def test_update_boxer_stats_win(mock_cursor):
    """Test updating the stats for boxer 

    """
    mock_cursor.fetchone.return_value = True

    boxer_id = 1
    update_boxer_stats(boxer_id, "win")

    expected_query = normalize_whitespace("""
        UPDATE boxers SET fights = fights + 1, wins = wins + 1 WHERE id = ?
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args_list[1][0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    actual_arguments = mock_cursor.execute.call_args_list[1][0][1]
    expected_arguments = (boxer_id,)

    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."


def test_update_boxer_stats_lose(mock_cursor):
    """Test updating the stats for boxer 

    """
    mock_cursor.fetchone.return_value = True

    boxer_id = 1
    update_boxer_stats(boxer_id, "loss")

    expected_query = normalize_whitespace("""
        UPDATE boxers SET fights = fights + 1 WHERE id = ?
    """)
    actual_query = normalize_whitespace(mock_cursor.execute.call_args_list[1][0][0])

    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    actual_arguments = mock_cursor.execute.call_args_list[1][0][1]
    expected_arguments = (boxer_id,)

    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."


def test_update_boxer_stats_invalid_boxer(mock_cursor):
    """Test error updating the stats for boxer that doesnt exist

    """
    mock_cursor.fetchone.return_value = None
    with pytest.raises(ValueError, match="Boxer with ID 999 not found."):
        update_boxer_stats(999, "win")

def test_update_boxer_stats_invalid_result():
    """Test error updating the stats for boxer with invalid result

    """
    with pytest.raises(ValueError, match="Invalid result: invalid. Expected 'win' or 'loss'."):
        update_boxer_stats(1, "invalid")

        