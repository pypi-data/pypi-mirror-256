from typing import List, Tuple

from pydantic import BaseModel

import src.magicapp_api.data_models.api_dtos as api_dtos


class AllGuidelineDTOs(BaseModel):
    guideline_dto: api_dtos.Guideline
    section_dtos: List[api_dtos.Section]
    recommendation_dtos: List[api_dtos.Recommendation]
    pico_dtos: List[api_dtos.Pico]
    dichotomous_outcome_dtos: List[api_dtos.DichotomousOutcome]
    continuous_outcome_dtos: List[api_dtos.ContinuousOutcome]
    non_poolable_outcome_dtos: List[api_dtos.NonPoolableOutcome]


class AllSectionDTOs(BaseModel):
    section_dtos: List[api_dtos.Section]
    recommendation_dtos: List[api_dtos.Recommendation]
    pico_dtos: List[api_dtos.Pico]
    dichotomous_outcome_dtos: List[api_dtos.DichotomousOutcome]
    continuous_outcome_dtos: List[api_dtos.ContinuousOutcome]
    non_poolable_outcome_dtos: List[api_dtos.NonPoolableOutcome]


class AllRecommendationDTOs(BaseModel):
    recommendation_dtos: List[api_dtos.Recommendation]
    pico_dtos: List[api_dtos.Pico]
    dichotomous_outcome_dtos: List[api_dtos.DichotomousOutcome]
    continuous_outcome_dtos: List[api_dtos.ContinuousOutcome]
    non_poolable_outcome_dtos: List[api_dtos.NonPoolableOutcome]


class AllPicoDTOs(BaseModel):
    pico_dtos: List[api_dtos.Pico]
    dichotomous_outcome_dtos: List[api_dtos.DichotomousOutcome]
    continuous_outcome_dtos: List[api_dtos.ContinuousOutcome]
    non_poolable_outcome_dtos: List[api_dtos.NonPoolableOutcome]


class AllOutcomeDTOs(BaseModel):
    dichotomous_outcome_dtos: List[api_dtos.DichotomousOutcome]
    continuous_outcome_dtos: List[api_dtos.ContinuousOutcome]
    non_poolable_outcome_dtos: List[api_dtos.NonPoolableOutcome]


class OutcomeIDs(BaseModel):
    di_outcome_ids: List[Tuple[int, int, int]]
    co_outcome_ids: List[Tuple[int, int, int]]
    np_outcome_ids: List[Tuple[int, int, int]]


class Outcomes(BaseModel):
    di_outcome_dtos: List[api_dtos.DichotomousOutcome]
    co_outcome_dtos: List[api_dtos.ContinuousOutcome]
    np_outcome_dtos: List[api_dtos.NonPoolableOutcome]
