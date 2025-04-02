import logging
import math
from typing import List

from boxing.models.boxers_model import Boxer, update_boxer_stats
from boxing.utils.logger import configure_logger
from boxing.utils.api_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


class RingModel:
    """
    Class that defines interactions among boxers such as fights and adding and removing boxers from the ring. 

    """
    def __init__(self):
        """This is the constructor to initialize an empty list of boxers. 

        """
        logger.info("Initializing a list of boxers in the ring...")
        self.ring: List[Boxer] = []
        logger.info("Successfully made a new empty list of boxers.")

    def fight(self) -> str:
        """ Simulates a fight between two boxers in the ring by comparing their skills,
        and then the boxers' statistics are udpated and the ring is cleared after the fight.

        Returns:
            str: The name of the boxer who won the fight.

        Raises:
            ValueError: If there are fewer than two boxers in the ring.

        """
        logger.info("Attempting to make two boxers fight.")
        if len(self.ring) < 2:
            logger.info(f"There must be two boxers to start a fight. There is only {len(self.ring)} boxer(s).")
            raise ValueError("There must be two boxers to start a fight.")

        logger.info("Retrieving boxers currently in the ring...")
        boxer_1, boxer_2 = self.get_boxers()
        logger.info("Successfully retrieved boxers currently in the ring.")

        logger.info("Retrieving the skills of boxers...")
        skill_1 = self.get_fighting_skill(boxer_1)
        skill_2 = self.get_fighting_skill(boxer_2)
        logger.info(f"Successfully retrieved the two boxers and their respective skills levels: {skill_1} and {skill_2}.")

        # Compute the absolute skill difference
        # And normalize using a logistic function for better probability scaling
        logger.info("Calculating the skill difference and normalizing...")
        delta = abs(skill_1 - skill_2)
        normalized_delta = 1 / (1 + math.e ** (-delta))
        logger.info(f"Successfully calculated the normalized difference: {normalized_delta}")

        logger.info("Requesting a random number through random.org API...")
        random_number = get_random()
        logger.info(f"Random number successfully fetched from API: {random_number}")

        logger.info("Calculating winner and loser...")
        if random_number < normalized_delta:
            winner = boxer_1
            loser = boxer_2
        else:
            winner = boxer_2
            loser = boxer_1
        logger.info(f"Calculated the winner using skill difference and probability. {winner} won and {loser} lost.")
        
        logger.info("Updated stats for boxers in backend after fight...")
        update_boxer_stats(winner.id, 'win')
        update_boxer_stats(loser.id, 'loss')
        logger.info(f"Updated the stats successfully for both boxers.")

        logger.info("Clearing the current ring after fight...")
        self.clear_ring()
        logger.info("Cleared the current ring.")
        logger.info(f"Returning the winner: {winner.name}")
        return winner.name

    def clear_ring(self):
        """This clears all the boxers that are in the ring.

        """
        logger.info("Checking if there is a ring...")
        if not self.ring:
            logger.warning("There are no boxers in the ring, so none were cleared.")
            return
        
        logger.info("Clearing the ring...")
        self.ring.clear()
        logger.info("Boxers were successfully cleared from the ring.")

    def enter_ring(self, boxer: Boxer):
        """Adds a boxer to the ring.

        Args:
            boxer (Boxer): The boxer that we are adding to the ring.

        Raises:
            TypeError: If the boxer is not an instance of the Boxer class.
            ValueError: If the ring is already full (i.e., contains 2 boxers).

        """
        logger.info("Checking if boxer is the correct type of Boxer...")
        if not isinstance(boxer, Boxer):
            logger.error(f"Invalid type attempted to enter the ring. Expected 'Boxer', got '{type(boxer).__name__}.'")
            raise TypeError(f"Invalid type: Expected 'Boxer', got '{type(boxer).__name__}'")

        logger.info("Checking if ring is full...")
        if len(self.ring) >= 2:
            logger.warning(f"The ring is full, so we cannot add any more boxers. There are currently {len(self.ring)} boxers in the ring.")
            raise ValueError("Ring is full, cannot add more boxers.")

        logger.info("Adding boxer to the list....")
        self.ring.append(boxer)
        logger.info(f"A boxer was successfully added to the ring. There are now {len(self.ring)} boxers in the ring.")

    def get_boxers(self) -> List[Boxer]:
        """Gets the current list of boxers in the ring.

        Returns:
            List[Boxer]: A list of boxers currently in the ring. 

        """
        logger.info("Checking if there is a ring...")
        if not self.ring:
            logger.warning("There are no boxers in the ring.")
            pass
        else:
            pass
        logger.info("Returning list of boxers...")
        return self.ring

    def get_fighting_skill(self, boxer: Boxer) -> float:
        """ Calculates the skill of a boxer taking into their age, name, weight, and reach arbitrarily.

        Args:
            boxer (Boxer): The boxer whose skill we are calculating.
        
        Returns:
            float: The skill of the corresponding boxer represented as a float.

        """
        # Arbitrary calculations
        logger.info("Performing arbitrary skill calculations...")
        age_modifier = -1 if boxer.age < 25 else (-2 if boxer.age > 35 else 0)
        skill = (boxer.weight * len(boxer.name)) + (boxer.reach / 10) + age_modifier
        logger.info(f"Set the skill level to {skill}.")

        return skill
