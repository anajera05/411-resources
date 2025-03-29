from dataclasses import asdict

import pytest

from boxing.models.boxers_model import Boxer


##################################################
# Create/Remove Boxer Test Cases
##################################################


def test_create_boxer(name, weight, height, reach, age):
    """Test creating a Boxer

    """
    boxer1 = Boxer(weight)
    boxer1.create_boxer(name, weight, height, reach, age)
    assert True


def test_create_boxer_invalid_weight(name, weight, height, reach, age):
    """Test error creating a Boxer with a weight below 125

    """
    assert True


def test_create_boxer_invalid_height(name, weight, height, reach, age):
    """Test error creating a Boxer with a height 0 or shorter

    """
    assert True


def test_create_boxer_invalid_reach(name, weight, height, reach, age):
    """Test error creating a Boxer with a reach 0.0 or shorter

    """
    assert True


def test_create_boxer_invalid_age_young(name, weight, height, reach, age):
    """Test error creating a Boxer younger than 18

    """
    assert True

def test_create_boxer_invalid_age_old(name, weight, height, reach, age):
    """Test error creating a Boxer older than 40

    """
    assert True


def test_create_boxer_duplicate(name, weight, height, reach, age):
    """Test error creating a Boxer with an existing name

    """
    assert True


def test_delete_boxer():
    """Test deleting a existing Boxer

    """
    assert True

def test_delete_boxer_not_found():
    """Test error deleting a non-existing Boxer

    """
    assert True
    

##################################################
# Retrive Stats on Boxer(s) Test Cases
##################################################


def test_get_leaderboard_wins(sort_by):
    """Test getting leaderboard by wins (default sort)

    """
    assert True


def test_get_leaderboard_pct(sort_by):
    """Test getting leaderboard by pct

    """
    assert True


def test_get_leaderboard_none(sort_by):
    """Test error input not wins or pct

    """
    assert True


def test_get_boxer_by_id(boxer_id):
    """Test getting boxer by ID

    """
    assert True


def test_get_boxer_by_id_not_found(boxer_id):
    """Test error getting Boxer with ID that does not exist

    """
    assert True


def test_get_boxer_by_name(boxer_name):
    """Test getting boxer by name

    """
    assert True


def test_get_boxer_by_name_not_found(boxer_name):
    """Test error getting Boxer with name that does not exist

    """
    assert True


def test_get_weight_class_heavyweight(weight):
    """Test getting weight class heavyweight

    """    
    assert True

def test_get_weight_class_middleweight(weight):
    """Test getting weight class middleweight

    """    
    assert True

def test_get_weight_class_lightweight(weight):
    """Test getting weight class lightweight

    """    
    assert True

def test_get_weight_class_featherweight(weight):
    """Test getting weight class featherweight

    """    
    assert True


def test_get_weight_class_invalid(weight):
    """Test error inputting invalid weight (less than 125)

    """    
    assert True

##################################################
# Change Stats of a Boxer Test Cases
##################################################


def test_update_boxer_stats_win(boxer_id, result):
    """Test updating Boxer stats for a win 

    """  
    assert True


def test_update_boxer_stats_loss(boxer_id, result):
    """Test updating Boxer stats for a loss 
    
    """  
    assert True


def test_update_boxer_stats_not_found(boxer_id, result):
    """Test error if Boxer ID not found 
    
    """  
    assert True