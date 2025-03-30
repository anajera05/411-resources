from dataclasses import dataclass
import logging
import sqlite3
from typing import Any, List

from boxing.utils.sql_utils import get_db_connection
from boxing.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


@dataclass
class Boxer:
    """
    A class to create a boxer with associated attributes (id, name, weight, height, reach, age, and weight_class).

    Attributes:
        id (int): ID of the boxer
        name (str): Name of the boxer
        weight (int): Weight of the boxer in pounds
        height (int):  Height of the boxer in inches
        reach (float): Reach of the boxer in inches
        age (int): Age of the boxer
        weight_class (str): default as none but is calculated based on the Boxer's weight

    """
    id: int
    name: str
    weight: int
    height: int
    reach: float
    age: int
    weight_class: str = None

    def __post_init__(self):
        """Initializes the Boxer and calculates the weight class based on their weight using get_weight_class

        """
        self.weight_class = get_weight_class(self.weight)  # Automatically assign weight class
        logger.info("Successful assigned weight class for Boxer")


##################################################
# Create/Remove Boxer
##################################################


def create_boxer(name: str, weight: int, height: int, reach: float, age: int) -> None:
    """Creates a Boxer with the inputted args 

    Args:
        name (str): Name of the boxer
        weight (int): Weight of the boxer in pounds
        height (int):  Height of the boxer in inches
        reach (float): Reach of the boxer in inches
        age (int): Age of the boxer

    Raises:
        ValueError: If
            -Weight is less than 125 
            -Height is less than or equal to 0 
            -Reach is less than or equal to 0 
            -Age is younger than 18 or older than 40
            -Boxer with the inputted name already exists (names must be unique)
        sqlite3.Error: If there is any error when attempting to connect to the backend.

    """

    logger.info(f"Attempting to create Boxer: {name}, Age: {age}, Weight: {weight}, Height: {height}, Reach: {reach}")

    logger.info("Checking if weight is more than 125...")
    if weight < 125:
        logger.error(f"Invalid weight: {weight}. Must be at least 125.")
        raise ValueError(f"Invalid weight: {weight}. Must be at least 125.") 
    
    logger.info("Checking if height is at least 0...")
    if height <= 0:
        logger.error(f"Invalid height: {height}. Must be greater than 0.")
        raise ValueError(f"Invalid height: {height}. Must be greater than 0.")
    
    logger.info("Checking if reach is at least 0...")
    if reach <= 0:
        logger.error(f"Invalid reach: {reach}. Must be greater than 0.")
        raise ValueError(f"Invalid reach: {reach}. Must be greater than 0.")
    
    logger.info("Checking if age is between 18 and 40...")
    if not (18 <= age <= 40):
        logger.error(f"Invalid age: {age}. Must be between 18 and 40.")
        raise ValueError(f"Invalid age: {age}. Must be between 18 and 40.")

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if the boxer already exists (name must be unique)
            cursor.execute("SELECT 1 FROM boxers WHERE name = ?", (name,))
            if cursor.fetchone():
                raise ValueError(f"Boxer with name '{name}' already exists")

            cursor.execute("""
                INSERT INTO boxers (name, weight, height, reach, age)
                VALUES (?, ?, ?, ?, ?)
            """, (name, weight, height, reach, age))

            logger.info("Successfully created new Boxer")
            conn.commit()

    except sqlite3.IntegrityError:
        logger.error(f"Boxer with name '{name}' already exists")
        raise ValueError(f"Boxer with name '{name}' already exists")

    except sqlite3.Error as e:
        logger.error("Error has occurred during interaction with an SQLite database")
        raise e

def delete_boxer(boxer_id: int) -> None:
    """Deletes a boxer that has been created
    
    Args:
        boxer_id (int): ID of the boxer to be removed
  
    Raises:
        ValueError: If Boxer ID is not found
        sqlite3.Error: If there is any error when attempting to connect to the backend.

    """ 
    logger.info(f"Recieved request to delete boxer {boxer_id}")
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM boxers WHERE id = ?", (boxer_id,))
            if cursor.fetchone() is None:
                logger.warning(f"Boxer with ID {boxer_id} not found.")
                raise ValueError(f"Boxer with ID {boxer_id} not found.")

            cursor.execute("DELETE FROM boxers WHERE id = ?", (boxer_id,))

            logger.info("Successfully deleted Boxer")
            conn.commit()

    except sqlite3.Error as e:
        logger.error("Error has occurred during interaction with an SQLite database")
        raise e
    

##################################################
# Retrive Stats on Boxer(s)
##################################################


def get_leaderboard(sort_by: str = "wins") -> List[dict[str, Any]]:
    """Gets leaderboard of created boxers based on how many wins they have or their win percentage 

    Args:
        sort_by (str, optional): Defaults to "wins"
            -"wins" - sorts the leaderboard based on the amount of wins each created boxer has 
            -"wins_pct" - sorts the leaderboard based on the winners win percentage (wins * 1.0 / fights)
  
    Returns: 
        List[dict[str, Any]]: a list of dictictionaries (representing the boxers) with each key = string and each value = any type in order based on sort_by (wins or wins_pct)

    Raises:
        ValueError: If sort_by is not "wins" or "wins_pct" 
        sqlite3.Error: If there is any error when attempting to connect to the backend.
    """     
    logger.info(f"Recieved request to return leaderboard of Boxers based on {sort_by}")
    
    query = """
        SELECT id, name, weight, height, reach, age, fights, wins,
               (wins * 1.0 / fights) AS win_pct
        FROM boxers
        WHERE fights > 0
    """

    if sort_by == "win_pct":
        logger.info("will sort by win percentage")
        query += " ORDER BY win_pct DESC"

    elif sort_by == "wins":
        logger.info("will sort by number of wins")
        query += " ORDER BY wins DESC"

    else:
        logger.error(f"Invalid sort_by parameter: {sort_by}")
        raise ValueError(f"Invalid sort_by parameter: {sort_by}")

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

        leaderboard = []
        for row in rows:
            boxer = {
                'id': row[0],
                'name': row[1],
                'weight': row[2],
                'height': row[3],
                'reach': row[4],
                'age': row[5],
                'weight_class': get_weight_class(row[2]),  # Calculate weight class
                'fights': row[6],
                'wins': row[7],
                'win_pct': round(row[8] * 100, 1)  # Convert to percentage
            }
            leaderboard.append(boxer)

        logger.info("Successfully created leaderboard")
        return leaderboard

    except sqlite3.Error as e:
        logger.error("Error has occurred during interaction with an SQLite database")
        raise e


def get_boxer_by_id(boxer_id: int) -> Boxer:
    """Retrives Boxer information of the inputted ID

    Args:
        boxer_id (int): a possible ID for a boxer 

    Returns: 
        Boxer: a existing Boxer with the inputted ID

    Raises: 
        ValueError: If Boxer ID is not found
        sqlite3.Error: If there is any error when attempting to connect to the backend.
    """ 
    logger.info(f"Retriving Boxer {boxer_id}")

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, weight, height, reach, age
                FROM boxers WHERE id = ?
            """, (boxer_id,))

            row = cursor.fetchone()

            if row:
                boxer = Boxer(
                    id=row[0], name=row[1], weight=row[2], height=row[3],
                    reach=row[4], age=row[5]
                )
                logger.info(f"Successfully retrieved boxer {boxer_id}")
                return boxer
            else:        
                logger.warning(f"Boxer with ID {boxer_id} not found.")
                raise ValueError(f"Boxer with ID {boxer_id} not found.")

    except sqlite3.Error as e:
        logger.error("Error has occurred during interaction with an SQLite database")
        raise e


def get_boxer_by_name(boxer_name: str) -> Boxer:
    """Retrives Boxer information of the inputted name

    Args:
        boxer_name (str): a possible name for a boxer 

    Returns: 
        Boxer: a existing Boxer with the inputted name

    Raises: 
        ValueError: If Boxer name is not found
        sqlite3.Error: If there is any error when attempting to connect to the backend.
    """ 
    logger.info(f"Retriving Boxer {boxer_name}")
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, weight, height, reach, age
                FROM boxers WHERE name = ?
            """, (boxer_name,))

            row = cursor.fetchone()

            if row:
                boxer = Boxer(
                    id=row[0], name=row[1], weight=row[2], height=row[3],
                    reach=row[4], age=row[5]
                )
                logger.info(f"Successfully retrieved boxer {boxer_name}")
                return boxer
            else:
                logger.warning(f"Boxer '{boxer_name}' not found.")
                raise ValueError(f"Boxer '{boxer_name}' not found.")

    except sqlite3.Error as e:
        logger.error("Error has occurred during interaction with an SQLite database")
        raise e


def get_weight_class(weight: int) -> str:
    """finds weight class based on a weight

    Args:
        weight (int): weight of a boxer to be classified 

    Returns: 
        str: the weight class based on the inputted weight 
            -if weight >= 203 -> 'HEAVYWEIGHT'
            -if weight >= 166 -> 'MIDDLEWEIGHT'
            -if weight >= 133 -> 'LIGHTWEIGHT'
            -if weight >= 125 -> 'FEATHERWEIGHT'

    Raises: 
        ValueError: If the weight is less than 125 (minimum weight)
    """ 
    logger.info(f"Calculating weight class of {weight}")

    if weight >= 203:
        weight_class = 'HEAVYWEIGHT'
    elif weight >= 166:
        weight_class = 'MIDDLEWEIGHT'
    elif weight >= 133:
        weight_class = 'LIGHTWEIGHT'
    elif weight >= 125:
        weight_class = 'FEATHERWEIGHT'
    else:
        logger.error(f"Invalid weight: {weight}. Weight must be at least 125.")
        raise ValueError(f"Invalid weight: {weight}. Weight must be at least 125.")

    logger.info(f"Successfully calculated {weight_class} for weight {weight}")   
    return weight_class


##################################################
# Change Stats of a Boxer
##################################################


def update_boxer_stats(boxer_id: int, result: str) -> None:
    """updates boxers stats based on the result (win or lose)

    Args:
        boxer_id (int): The ID of the boxer that needs their stats updated 
        result (str): result of fight 
            -"win": increases number of fights by one and number of wins by one 
            -"lose": increases number of fights by one

    Raises: 
        ValueError: If
            -result is not "win" or "lose"
            -the inputted ID is not found
        sqlite3.Error: If there is any error when attempting to connect to the backend.
    """ 
    logger.info(f"Recieved request to update Boxer {boxer_id} stats to reflect a {result}")

    if result not in {'win', 'loss'}:
        logger.error(f"Invalid result: {result}. Expected 'win' or 'loss'.")
        raise ValueError(f"Invalid result: {result}. Expected 'win' or 'loss'.")

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM boxers WHERE id = ?", (boxer_id,))
            if cursor.fetchone() is None:
                logger.warning(f"Boxer with ID {boxer_id} not found.")
                raise ValueError(f"Boxer with ID {boxer_id} not found.")

            if result == 'win':
                cursor.execute("UPDATE boxers SET fights = fights + 1, wins = wins + 1 WHERE id = ?", (boxer_id,))
            else:  # result == 'loss'
                cursor.execute("UPDATE boxers SET fights = fights + 1 WHERE id = ?", (boxer_id,))

            logger.info(f"Successfully updated Boxer stats to reflect a {result}")
            conn.commit()

    except sqlite3.Error as e:
        logger.error("Error has occurred during interaction with an SQLite database")        
        raise e
