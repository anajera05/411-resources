import pytest
from dataclasses import asdict
import math
from contextlib import contextmanager
from boxing.models.ring_model import RingModel, get_random
from boxing.models.boxers_model import Boxer, update_boxer_stats

@pytest.fixture()
def ring_model():
    """Fixture to provide a new instance of RingModel for each test."""
    return RingModel()

"""Fixtures providing sample songs for the tests."""
@pytest.fixture
def sample_boxer1():
    return Boxer(1, 'Boxer 1', 130, 60, 10, 30)

@pytest.fixture
def sample_boxer2():
    return Boxer(2, 'Boxer 2', 190, 65, 15, 25)

@pytest.fixture
def sample_boxer3():
    return Boxer(3, 'Boxer 3', 195, 62, 13, 35)

@pytest.fixture
def sample_ring1(sample_boxer1):
    return [sample_boxer1]

@pytest.fixture
def sample_ring2(sample_boxer1, sample_boxer2):
    return [sample_boxer1, sample_boxer2]

@pytest.fixture
def mock_update_boxer_stats(mocker):
    """Mock the update_boxer_stats function for testing purposes."""
    return mocker.patch("boxing.models.ring_model.update_boxer_stats")
##################################################
# Add / Remove Boxers Test Cases
##################################################

def test_add_boxer_to_ring(ring_model, sample_boxer1):
    """Test adding a boxer to the playlist.

    """
    ring_model.enter_ring(sample_boxer1)
    assert len(ring_model.ring) == 1, f"Expected 1 boxer in the ring, got {len(ring_model.ring)} boxers"
    assert ring_model.ring[0].name == 'Boxer 1', f"Expected boxer's name to be 'Boxer 1', got {ring_model.ring[0].name} as their name"

def test_add_bad_boxer_to_ring(ring_model, sample_boxer1):
    """Test error when adding a boxer that is not of type boxer to ring.

    """
    with pytest.raises(TypeError, match=f"Invalid type: Expected 'Boxer', got '{type(asdict(sample_boxer1)).__name__}'"):
        ring_model.enter_ring(asdict(sample_boxer1))

def test_add_two_boxers_to_ring(ring_model, sample_boxer1, sample_boxer2):
    """Test adding 2 boxers to the ring."

    """
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
    assert len(ring_model.ring) == 2, f"Expected 2 boxers in the ring, got {len(ring_model.ring)} boxer(s)"
    assert ring_model.ring[0].name == 'Boxer 1', f"Expected 1st boxer's name to be 'Boxer 1', got {ring_model.ring[0].name} as their name"
    assert ring_model.ring[1].name == 'Boxer 2', f"Expected 2nd boxer's name to be 'Boxer 2', got {ring_model.ring[1].name} as their name"

def test_add_third_boxer_to_ring(ring_model, sample_boxer1, sample_boxer2, sample_boxer3):
    """Test adding 3 boxers to the ring. This is not valid.

    """
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
    with pytest.raises(ValueError, match="Ring is full, cannot add more boxers."):
        ring_model.enter_ring(sample_boxer3)

def test_clear_ring_with_no_boxers(ring_model):
    """Test clearing the ring even if there are already no boxers.

    """
    ring_model.ring.extend([])
    ring_model.clear_ring()
    assert len(ring_model.ring) == 0, "Ring should be empty after clearing"
    

def test_clear_ring_with_one_boxer(ring_model, sample_ring1):
    """Test clearing the ring with 1 boxer.

    """
    ring_model.ring.extend(sample_ring1)

    ring_model.clear_ring()
    assert len(ring_model.ring) == 0, "Ring should be empty after clearing"

def test_clear_ring_with_two_boxer(ring_model, sample_ring2):
    """Test clearing the ring with 2 boxers.

    """
    ring_model.ring.extend(sample_ring2)
    ring_model.clear_ring()
    assert len(ring_model.ring) == 0, "Ring should be empty after clearing"

##################################################
# Ring Retrieval Test Cases
##################################################

def test_get_skill_level(ring_model, sample_boxer1):
    """Test the arbitrary skill level calculation.

    """
    age_modifier = -1 if sample_boxer1.age < 25 else (-2 if sample_boxer1.age > 35 else 0)
    calculated_skill = (sample_boxer1.weight * len(sample_boxer1.name)) + (sample_boxer1.reach / 10) + age_modifier
    retrieved_skill = ring_model.get_fighting_skill(sample_boxer1)
    assert retrieved_skill == calculated_skill, f"Retrieved Skill: {retrieved_skill}; Calculated Skill: {calculated_skill}"

def test_get_boxers_no_boxers(ring_model):
    """Test getting boxers in the ring if there are not boxers in the ring

    """
    ring_model.ring.extend([])
    retrieved_ring = ring_model.get_boxers()
    assert len(retrieved_ring) == 0, "No boxers returned if there are no boxers in the first place."

def test_get_two_boxers(ring_model, sample_ring2):
    """Test successfully retrieving a list of boxers in a ring when there's 2 boxers.

    """
    ring_model.ring.extend(sample_ring2)

    retrieved_ring = ring_model.get_boxers()
    assert retrieved_ring[0].id == 1, "Incorrect ID of 1st boxer"
    assert retrieved_ring[0].name == 'Boxer 1', "Incorrect name of 1st boxer"
    assert retrieved_ring[0].weight == 130, "Incorrect weight of 1st boxer"
    assert retrieved_ring[0].height == 60, "Incorrect height of 1st boxer"
    assert retrieved_ring[0].reach == 10, "Incorrect reach of 1st boxer"
    assert retrieved_ring[0].age == 30, "Incorrect age of 1st boxer"

    assert retrieved_ring[1].id == 2, "Incorrect ID of 2nd boxer"
    assert retrieved_ring[1].name == 'Boxer 2', "Incorrect name of 2nd boxer"
    assert retrieved_ring[1].weight == 190, "Incorrect weight of 2nd boxer"
    assert retrieved_ring[1].height == 65, "Incorrect height of 2nd boxer"
    assert retrieved_ring[1].reach == 15, "Incorrect reach of 2nd boxer"
    assert retrieved_ring[1].age == 25,  "Incorrect age of 2nd boxer"

def test_get_one_boxer(ring_model, sample_ring1):
    """Test successfully retrieving a list of boxers in a ring when there's 1 boxer.

    """
    ring_model.ring.extend(sample_ring1)

    retrieved_ring = ring_model.get_boxers()
    assert retrieved_ring[0].id == 1, "Incorrect ID of 1st boxer"
    assert retrieved_ring[0].name == 'Boxer 1', "Incorrect name of 1st boxer"
    assert retrieved_ring[0].weight == 130, "Incorrect weight of 1st boxer"
    assert retrieved_ring[0].height == 60, "Incorrect height of 1st boxer"
    assert retrieved_ring[0].reach == 10, "Incorrect reach of 1st boxer"
    assert retrieved_ring[0].age == 30, "Incorrect age of 1st boxer"


##################################################
# Fight Retrieval Test Cases
##################################################

def test_fight_no_boxers(ring_model):
    """Testing fight method with no boxers in the ring

    """
    with pytest.raises(ValueError, match="There must be two boxers to start a fight."):
        ring_model.fight()

def test_fight_one_boxer(ring_model, sample_ring1):
    """Testing fight method with only one boxer in the ring

    """
    ring_model.ring.extend(sample_ring1)
    with pytest.raises(ValueError, match="There must be two boxers to start a fight."):
        ring_model.fight()

def test_fight(ring_model, sample_ring2, mocker, mock_update_boxer_stats):
    """Testing fight method to see who wins

    """
    random_test = 0.5
    skill_test = 900
    mocker.patch("boxing.models.ring_model.get_random", return_value=random_test)
    ring_model.ring.extend(sample_ring2)
    mocker.patch.object(RingModel, 'get_fighting_skill', return_value=skill_test)
    skill_1 = skill_test
    skill_2 = skill_test
    delta = abs(skill_1 - skill_2)
    normalized_delta = 1 / (1 + math.e ** (-delta))
    random_number = random_test

    boxer_1 = ring_model.ring[0]
    boxer_2 = ring_model.ring[1]

    if random_number < normalized_delta:
        winner = boxer_1
        loser = boxer_2
    else:
        winner = boxer_2
        loser = boxer_1

    assert winner.name == ring_model.fight(), f"Winner {winner.name} was expected, but did not get that"

    assert mock_update_boxer_stats.call_count == 2, f"Called update_boxer_stats twice."
    