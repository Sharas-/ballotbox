import pytest
from domain.ballotbox import *

def test_voter_can_vote_only_once():
    options = ['option', 'option 2']
    bbox = BallotBox(options)
    voterid = 'voter'
    bbox.cast_vote(voterid, options[0])
    with pytest.raises(DuplicateVoteException):
        bbox.cast_vote(voterid, options[0])

def test_voter_cannot_change_her_vote():
    options = ['option', 'option 2']
    bbox = BallotBox(options)
    voterid = 'voter'
    bbox.cast_vote(voterid, options[0])
    with pytest.raises(DuplicateVoteException):
        bbox.cast_vote(voterid, options[1])

def test_cant_create_ballotbox_without_options():
    with pytest.raises(ValueError):
        BallotBox(None)
    with pytest.raises(ValueError):
        BallotBox([])
        
def test_cant_create_ballotbox_with_one_option():
    with pytest.raises(ValueError):
        BallotBox(['one option'])

def test_cant_vote_on_non_existing_option():
    bbox = BallotBox(['option 1', 'option 2'])
    with pytest.raises(OptionUnavailableException):
        bbox.cast_vote('voter', 'option 3')

def test_when_no_votes_casted_result_counts_are_all_zero():
    options = ['option 1', 'option 2']
    bbox = BallotBox(options)
    expected_results = {option: 0 for option in options}
    assert bbox.results() == expected_results

def test_even_options_not_voted_for_represented_in_results():
    option_voted = 'favourite option'
    option_unvoted = 'loser option'
    bbox = BallotBox([option_voted, option_unvoted])
    bbox.cast_vote('voter1', option_voted)
    expected_results = {option_voted: 1, option_unvoted: 0}
    assert bbox.results() == expected_results

def test_vote_counts_are_aggregated_in_results():
    option1 = 'option 1'
    option2 = 'option 2'
    bbox = BallotBox([option1, option2])
    bbox.cast_vote('voter1', option1)
    bbox.cast_vote('voter2', option1)
    bbox.cast_vote('voter3', option1)
    bbox.cast_vote('voter4', option2)
    bbox.cast_vote('voter5', option2)
    expected_results = {option1: 3, option2: 2}
    assert bbox.results() == expected_results

