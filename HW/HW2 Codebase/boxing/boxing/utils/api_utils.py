import logging
import os
import requests

from boxing.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


RANDOM_ORG_URL = os.getenv("RANDOM_ORG_URL",
                           "https://www.random.org/decimal-fractions/?num=1&dec=2&col=1&format=plain&rnd=new")


def get_random() -> float:
    """
    Produces a random number from 0 to 1 through an API call.

    Returns:
        float: The resulting random number produced.

    Raises:
        ValueError: The response from the provided url was invalid.
        RuntimeError: The request to the provided url timed out or failed.
    """
    try:
        logger.info("Making a request to random.org for random number.")
        response = requests.get(RANDOM_ORG_URL, timeout=5)

        # Check if the request was successful
        logger.info("Checking if the request was successful.")
        response.raise_for_status()
        
        
        random_number_str = response.text.strip()
        logger.info(f"Response received: {random_number_str}")

        try:
            logger.info("Attempting to cast response to a float.")
            random_number = float(random_number_str)
        except ValueError:
            logger.error(f"Invalid response from random.org: {random_number_str} and wasn't able to cast response to float.")
            raise ValueError(f"Invalid response from random.org: {random_number_str}")

        logger.info(f"Succesfully produced a random number: {random_number}")
        return random_number

    except requests.exceptions.Timeout:
        logger.error("Request to random.org took too long.")
        raise RuntimeError("Request to random.org timed out.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request to random.org failed: {e}")
        raise RuntimeError(f"Request to random.org failed: {e}")
