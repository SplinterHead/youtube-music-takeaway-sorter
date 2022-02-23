from typing import Any, List

from .lib.logging import get_logger

log = get_logger("sorter")


def sort_lists(csv_list: List[Any], os_list: List[tuple]) -> List[Any]:
    log.info(f"{len(csv_list)} CSV records and {len(os_list)} Files to match")
    output_dict = {}
    for os_file in os_list:
        if len(csv_list) > 0:
            log.info(f"Looking for a match: {os_file[0]} ({os_file[1]}s)")
            absolute_difference_function = lambda list_value: abs(
                list_value.duration - os_file[1]
            )
            closest_match = min(csv_list, key=absolute_difference_function)
            log.info(
                f"  The closest match looks to be {closest_match.title} ({closest_match.duration}s)"
            )
            csv_list.pop(csv_list.index(closest_match))
            closest_match.filename = os_file[0]
            output_dict[closest_match.filename] = closest_match
    # Reduce dict to a list
    return list(output_dict.values())
