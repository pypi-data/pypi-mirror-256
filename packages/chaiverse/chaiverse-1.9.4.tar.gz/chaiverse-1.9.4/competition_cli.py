import sys
from typing import List, Literal, Optional

from chaiverse.http_client import SubmitterClient
from chaiverse.login_cli import auto_authenticate
from chaiverse.schemas import Competition
from chaiverse import config


@auto_authenticate
def get_competitions(status: Optional[Literal['submitting', 'evaluating']]=None, developer_key=None) -> List[Competition]:
    submitter_client = SubmitterClient(developer_key=developer_key)
    response = submitter_client.get(config.COMPETITIONS_ENDPOINT, params=dict(status=status))
    competitions = [Competition(**competition) for competition in response['competitions']]
    return competitions


def create_competition(competition: Competition, developer_key: str=None):
    submitter_client = SubmitterClient(developer_key=developer_key)
    url = config.COMPETITIONS_ENDPOINT
    competition_id = submitter_client.post(url, data=competition.model_dump())
    return competition_id


def update_competition(competition_id: str, competition: Competition, developer_key: str=None):
    submitter_client = SubmitterClient(developer_key=developer_key)
    url = config.COMPETITION_ENDPOINT.format(competition_id=competition_id)
    competition = submitter_client.put(url, data=competition.model_dump())
    competition = Competition(**competition)
    return competition


def enroll_submission(submission_id, competition_id=None, developer_key=None):
    display_name = competition_id
    if competition_id is None:
        competition = get_competitions(status='submitting')[0]
        competition_id = competition.competition_id
        display_name = competition.display_name
    submitter_client = SubmitterClient(developer_key=developer_key)
    url = config.COMPETITION_ENROLLED_SUBMISSION_IDS_ENDPOINT.format(submission_id=submission_id, competition_id=competition_id)
    submission_ids = submitter_client.post(url)
    print(f'Enrolled {submission_id} into {display_name}.')
    return submission_ids


def withdraw_submission(submission_id, developer_key=None):
    competitions = get_competitions(status='submitting')
    assert competitions
    competition = competitions[0]

    submitter_client = SubmitterClient(developer_key=developer_key)
    url = config.COMPETITION_ENROLLED_SUBMISSION_IDS_ENDPOINT.format(submission_id=submission_id, competition_id=competition.competition_id)
    submission_ids = submitter_client.delete(url)
    print(f'Withdrawn {submission_id} from {competition.display_name}.')
    return submission_ids