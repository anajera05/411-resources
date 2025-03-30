from dataclasses import asdict

import pytest

from boxing.models.boxers_model import Boxer

@pytest.fixture()
def boxer_model():
    """Fixture to provide a new Boxer instance for each test."""
    return Boxer().create_boxer("John Doe", 150, 70, 74.5, 30)

@pytest.fixture()
def boxer_model2():
    """Fixture to provide a new Boxer instance for each test."""
    return Boxer().create_boxer("Mark Scout", 200, 75, 78.3, 27)


##################################################
# Create/Remove Boxer Test Cases
##################################################


def test_create_boxer():
    """Test creating a Boxer

    """
    Boxer().create_boxer("John Doe", 120, 70, 74.5, 30)
    assert boxer_model.id == 1


def test_create_boxer_invalid_weight():
    """Test error creating a Boxer with a weight below 125

    """
    with pytest.raises(ValueError, match="Invalid weight: 120. Must be at least 125."):
        Boxer().create_boxer(name="John Doe", weight=120, height=70, reach=74.5, age=30)


def test_create_boxer_invalid_height():
    """Test error creating a Boxer with a height 0 or shorter

    """
    with pytest.raises(ValueError, match="Invalid height: 0. Must be greater than 0."):
       Boxer().create_boxer(name="John Doe", weight=150, height=0, reach=74.5, age=30)



def test_create_boxer_invalid_reach():
    """Test error creating a Boxer with a reach 0.0 or shorter

    """
    with pytest.raises(ValueError, match="Invalid reach: 0.0. Must be greater than 0.0"):
        Boxer().create_boxer(name="John Doe", weight=150, height=70, reach=0.0, age=30)


def test_create_boxer_invalid_age_young():
    """Test error creating a Boxer younger than 18

    """
    with pytest.raises(ValueError, match="Invalid age: 15. Must be between 18 and 40."):
        Boxer().create_boxer(name="John Doe", weight=150, height=70, reach=74.5, age=15)


def test_create_boxer_invalid_age_old():
    """Test error creating a Boxer older than 40

    """
    with pytest.raises(ValueError, match="Invalid age: 45. Must be between 18 and 40."):
        Boxer().create_boxer(name="John Doe", weight=150, height=70, reach=74.5, age=45)



def test_create_boxer_duplicate():
    """Test error creating a Boxer with an existing name

    """
    Boxer().create_boxer(("John Doe", 120, 70, 74.5, 30))
    with pytest.raises(ValueError, match="Boxer with name 'John Doe' already exists"):
        Boxer().create_boxer(("John Doe", 120, 70, 74.5, 30))


def test_delete_boxer(boxer_model):
    """Test deleting a existing Boxer

    """
    boxer_id = boxer_model.id
    Boxer().delete_boxer(boxer_id)

    with pytest.raises(ValueError, match=f"Boxer with ID {boxer_id} not found."):
        Boxer().get_boxer_by_id(boxer_id)



def test_delete_boxer_not_found():
    """Test error deleting a non-existing Boxer

    """
    invalid_boxer_id = 9999 
    with pytest.raises(ValueError, match=f"Boxer with ID {invalid_boxer_id} not found."):
        Boxer().delete_boxer(invalid_boxer_id)
    

##################################################
# Retrive Stats on Boxer(s) Test Cases
##################################################


def test_get_leaderboard_wins(boxer_model, boxer_model2):
    """Test getting leaderboard by wins (default sort)

    """
    boxer_model.update_boxer_stats()
    assert True

def test_get_leaderboard_pct(sort_by):
    """Test getting leaderboard by pct

    """
    assert True


def test_get_leaderboard_none(sort_by):
    """Test error input not wins or pct

    """
    assert True


def test_get_boxer_by_id(boxer_model):
    """Test getting boxer by ID

    """
    boxer_id = boxer_model.id
    assert Boxer().get_boxer_by_name(boxer_id) == boxer_model


def test_get_boxer_by_id_not_found(boxer_id):
    """Test error getting Boxer with ID that does not exist

    """
    invalid_id = boxer_model.id
    with pytest.raises(ValueError, match=f"Boxer with ID {invalid_id} not found."):
        Boxer().get_boxer_by_name(invalid_id)


def test_get_boxer_by_name(boxer_model):
    """Test getting boxer by name

    """
    boxer_name = boxer_model.name
    assert Boxer().get_boxer_by_name(boxer_name) == boxer_model


def test_get_boxer_by_name_not_found():
    """Test error getting Boxer with name that does not exist

    """
    invalid_name = "Joe"
    with pytest.raises(ValueError, match=f"Boxer '{invalid_name}' not found."):
        Boxer().get_boxer_by_name(invalid_name)


def test_get_weight_class_heavyweight():
    """Test getting weight class heavyweight (over 203)

    """    
    weight = 203
    assert Boxer().get_weight_class(weight) == 'HEAVYWEIGHT'

def test_get_weight_class_middleweight():
    """Test getting weight class middleweight (between 166 and 203)

    """    
    weight = 166
    assert Boxer().get_weight_class(weight) == 'MIDDLEWEIGHT'

def test_get_weight_class_lightweight():
    """Test getting weight class lightweight (between 133 and 166)

    """    
    weight = 133
    assert Boxer().get_weight_class(weight) == 'LIGHTWEIGHT'

def test_get_weight_class_featherweight():
    """Test getting weight class featherweight (between 125 and 133)

    """    
    weight = 125
    assert Boxer().get_weight_class(weight) == 'FEATHERWEIGHT'


def test_get_weight_class_invalid():
    """Test error inputting invalid weight (less than 125)

    """   
    weight = 100 
    with pytest.raises(ValueError, match=f"Invalid weight: {weight}. Weight must be at least 125."):
        Boxer().get_weight_class(weight)

##################################################
# Change Stats of a Boxer Test Cases
##################################################


def test_update_boxer_stats_win(boxer_model):
    """Test updating Boxer stats for a win 

    """  
    boxer_id = boxer_model.id
    result = "win"
    boxer_model.update_boxer_stats(boxer_id, result)
    assert boxer_model.fights == 1
    assert boxer_model.wins == 1


def test_update_boxer_stats_loss(boxer_model):
    """Test updating Boxer stats for a loss 
    
    """  
    boxer_id = boxer_model.id
    result = "lose"
    boxer_model.update_boxer_stats(boxer_id, result)
    assert boxer_model.fights == 1
    assert boxer_model.wins == 0


def test_update_boxer_stats_no_result(boxer_model):
    """Test error if result is not "win" or "lose"
    
    """  
    boxer_id = boxer_model.id
    invalid_result = "err"
    with pytest.raises(ValueError, match=f"Invalid result: {invalid_result}. Expected 'win' or 'loss'."):
        boxer_model.update_boxer_stats(boxer_id, invalid_result)


def test_update_boxer_stats_not_found(boxer_model):
    """Test error if Boxer ID not found 
    
    """  
    invalid_boxer_id = 9999
    result = "win"
    with pytest.raises(ValueError, match=f"Boxer with ID {invalid_boxer_id} not found."):
        boxer_model.update_boxer_stats(invalid_boxer_id, result)