# Ballot Box - a simple HTTP service representing a ballot.

A single instance of a docker container represents a separate ballot.

## Usage

- When creating new ballot instance container, initialize it with ballot vote options through BALLOT_OPTIONS environment variable.
- POST votes to ballot HTTP resource with ballot option in request body and user id in Authorization header to cast a vote.
- GET voting results from ballot HTTP resource.
- Destroy the container when ballot is over.
