from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

from django.db.models import QuerySet


@dataclass
class GraphicDto:
    labels: list
    data: list

    @staticmethod
    def _get_count(query_set: QuerySet[dict]) -> list[int]:
        return [item["count"] for item in query_set]

    @classmethod
    def get_from_query_set(
            cls, query_set: QuerySet[dict],
            get_labels_func: Callable
    ) -> GraphicDto:
        return cls(
            get_labels_func(query_set),
            cls._get_count(query_set)
        )
