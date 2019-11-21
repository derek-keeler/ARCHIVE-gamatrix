"""Module containing code for outputting result data to JSON."""

import json
from typing import List

from steamingpile import interfaces


class JsonOutputFormatter(interfaces.IOutputFormatter):
    def __init__(self):
        pass

    def write_results(self, results: List[str]) -> bytes:
        return json.dumps(results)
