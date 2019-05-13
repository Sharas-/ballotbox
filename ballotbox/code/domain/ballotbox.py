class DuplicateVoteException(ValueError):
    pass
class OptionUnavailableException(ValueError):
    pass

class BallotBox:
     
    def __init__(self, ballot_options):
        """
        Creates ballot box

        Args:
            ballot_options: options to vote for
        """
        if(not ballot_options or len(ballot_options) < 2):
            raise ValueError("Cannot create ballot with less than two woting options")
        self.options = set(ballot_options)
        self.votes = {}

    def is_voting_option(self, option):
        """
        Args:
            option: voting option's unique identifier

        Returns:
            True if voting option is in ballot  
        """
        return option in self.options

    def already_voted(self, voter):
        """
        Args:
            voter: voter's unique identifier

        Returns:
            True if voter already voted
        """
        return voter in self.votes

    def cast_vote(self, voter, option):
        """
        Adds voters' vote to this ballot box

        Args:
             voter: voter's unique identifier
             option: voting options' unique identifier
        """
        if self.already_voted(voter):
            raise DuplicateVoteException("Voter {0} already voted".format(voter))
        if not self.is_voting_option(option):
            raise OptionUnavailableException("This ballot has no option for {0}".format(option))
        self.votes[voter] = option

    def results(self):
        """
        Returns: Ballot results with vote counts for each option
        """
        from collections import Counter
        counts = Counter({option: 0 for option in self.options})
        counts.update(Counter(self.votes.values()))
        return counts

