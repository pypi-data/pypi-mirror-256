import os

from src.magicapp_api.api_wrapper import get_all_guideline_dtos
from src.magicapp_api.data_models.data_classes import AllGuidelineDTOs


def test_get_all_guideline_dtos():
    guideline_id = 6748
    result: AllGuidelineDTOs = get_all_guideline_dtos(guideline_id)

    # Add assertions here based on what you expect the result to be
    # TODO

    _save_guideline_dtos(guideline_id, result)


def _save_guideline_dtos(guideline_id: int, result: AllGuidelineDTOs):
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    counter = 0
    while True:
        suffix = f"_{counter}" if counter > 0 else ""
        filename = os.path.join(
            output_dir, f"guideline_{guideline_id}_dtos{suffix}.json"
        )
        if not os.path.exists(filename):
            break
        counter += 1

    with open(filename, "w") as f:
        f.write(result.model_dump_json())
