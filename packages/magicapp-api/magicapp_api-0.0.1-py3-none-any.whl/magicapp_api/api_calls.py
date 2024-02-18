import requests

BASE_URL = "https://api.magicapp.org"


def fetch_guideline(guideline_id: int, verbose: bool = True):
    if verbose:
        print(f"Fetching guideline {guideline_id}...")
    url = f"{BASE_URL}/api/v1/guidelines/{guideline_id}"
    return fetch_from_api(url)


def fetch_guideline_sections(guideline_id: int, verbose: bool = True):
    if verbose:
        print(f"Fetching sections for {guideline_id}...")
    url = f"{BASE_URL}/api/v1/guidelines/{guideline_id}/sections"
    return fetch_from_api(url)


def fetch_guideline_recs(guideline_id: int, verbose: bool = True):
    if verbose:
        print(f"Fetching recommendations for {guideline_id}...")
    url = f"{BASE_URL}/api/v1/guidelines/{guideline_id}/recommendations"
    return fetch_from_api(url)


def fetch_rec_picos(section_id: int, rec_id: int, verbose: bool = True):
    if verbose:
        print(f"Fetching picos for {section_id}...")
    url = f"{BASE_URL}/api/v1/sections/{section_id}/recommendations/{rec_id}/picos"
    return fetch_from_api(url)


def fetch_dichotomous_outcome(outcome_id: int, verbose: bool = True):
    if verbose:
        print(f"Fetching dichotomous outcomes for {outcome_id}...")
    url = f"{BASE_URL}/api/v1/picos/outcomes/dichotomous/{outcome_id}"
    return fetch_from_api(url)


def fetch_continuous_outcome(outcome_id: int, verbose: bool = True):
    if verbose:
        print(f"Fetching continuous outcomes for {outcome_id}...")
    url = f"{BASE_URL}/api/v1/picos/outcomes/continuous/{outcome_id}"
    return fetch_from_api(url)


def fetch_non_poolable_outcome(outcome_id: int, verbose: bool = True):
    if verbose:
        print(f"Fetching non-poolable outcomes for {outcome_id}...")
    url = f"{BASE_URL}/api/v1/picos/outcomes/non-poolable/{outcome_id}"
    return fetch_from_api(url)


def fetch_from_api(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None
