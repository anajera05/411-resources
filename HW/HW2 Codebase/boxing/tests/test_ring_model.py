import pytest
from dataclasses import asdict
import math

from boxing.models.ring_model import RingModel
from boxing.models.boxers_model import Boxer

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


##################################################
# Add / Remove Boxers Test Cases
##################################################

def test_add_boxer_to_ring(ring_model, sample_boxer1):
    """Test adding a boxer to the playlist.

    """
    ring_model.enter_ring(sample_boxer1)
    assert len(ring_model.ring) == 1
    assert ring_model.ring[0].name == 'Boxer 1'

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
    assert len(ring_model.ring) == 2
    assert ring_model.ring[0].name == 'Boxer 1'
    assert ring_model.ring[1].name == 'Boxer 2'

def test_add_third_boxer_to_ring(ring_model, sample_boxer1, sample_boxer2, sample_boxer3):
    """Test adding 3 boxers to the ring. This is not valid.

    """
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
    with pytest.raises(ValueError, match="Ring is full, cannot add more boxers."):
        ring_model.enter_ring(sample_boxer3)

def test_clear_ring_with_no_boxers(ring_model):
    ring_model.clear_ring()
    assert len(ring_model.ring) == 0, "Ring should be empty after clearing"
    

def test_clear_ring_with_one_boxer(ring_model, sample_boxer1):
    """Test clearing the ring with 1 boxer.

    """
    ring_model.enter_ring(sample_boxer1)

    ring_model.clear_ring()
    assert len(ring_model.ring) == 0, "Ring should be empty after clearing"

def test_clear_ring_with_two_boxer(ring_model, sample_boxer1, sample_boxer2):
    """Test clearing the ring with 2 boxers.

    """
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
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
    retrieved_ring = ring_model.get_boxers()
    assert len(retrieved_ring) == 0

def test_get_boxers(ring_model, sample_boxer1, sample_boxer2):
    """Test successfully retrieving a list of boxers in a ring.

    """
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)

    retrieved_ring = ring_model.get_boxers()
    assert retrieved_ring[0].id == 1
    assert retrieved_ring[0].name == 'Boxer 1'
    assert retrieved_ring[0].weight == 130
    assert retrieved_ring[0].height == 60
    assert retrieved_ring[0].reach == 10
    assert retrieved_ring[0].age == 30

    assert retrieved_ring[1].id == 2
    assert retrieved_ring[1].name == 'Boxer 2'
    assert retrieved_ring[1].weight == 190
    assert retrieved_ring[1].height == 65
    assert retrieved_ring[1].reach == 15
    assert retrieved_ring[1].age == 25

##################################################
# Fight Retrieval Test Cases
##################################################

def test_fight_no_boxers(ring_model):
    with pytest.raises(ValueError, match="There must be two boxers to start a fight."):
        ring_model.fight()

def test_fight_one_boxer(ring_model, sample_boxer1):
    ring_model.enter_ring(sample_boxer1)
    with pytest.raises(ValueError, match="There must be two boxers to start a fight."):
        ring_model.fight()

def test_fight(ring_model, sample_boxer1, sample_boxer2):
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
    skill_1 = ring_model.get_fighting_skill(sample_boxer1)
    skill_2 = ring_model.get_fighting_skill(sample_boxer2)
    delta = abs(skill_1 - skill_2)
    normalized_delta = 1 / (1 + math.e ** (-delta))
    # random_number=0.5
    # if random_number < normalized_delta:
    #     winner = boxer_1
    #     loser = boxer_2
    # else:
    #     winner = boxer_2
    #     loser = boxer_1

    