from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet, Count, Case, When, Value, CharField, \
    IntegerField
from django.shortcuts import render

from dto.dto import GraphicDto
from tasks.models import Task


def get_tasks_labels(query_set: QuerySet[dict]) -> list[str]:
    return [
        item["priority_display"]
        for item in query_set
    ]


def graphic_tasks_per_week(user) -> dict:
    query_set = user.tasks_to_do.values("priority").annotate(
        count=Count("name"),
        priority_display=Case(
            When(priority="L", then=Value("Low")),
            When(priority="M", then=Value("Medium")),
            When(priority="H", then=Value("High")),
            output_field=CharField(),
        ),
        priority_order=Case(
            When(priority="L", then=Value(1)),
            When(priority="M", then=Value(2)),
            When(priority="H", then=Value(3)),
            output_field=IntegerField(),
        )
    ).order_by("priority_order")

    tasks_graphic_per_week = GraphicDto.get_from_query_set(
        query_set,
        get_tasks_labels
    )
    return {
        "tasks_per_week": tasks_graphic_per_week,
        "is_tasks_exist": query_set.exists(),
    }


@login_required
def index(request):
    user = request.user
    assignees_queryset = Task.objects.filter(assignees=user)
    num_tasks = assignees_queryset.count()
    num_completed_tasks = assignees_queryset.filter(is_completed=True).count()
    num_uncompleted_tasks = assignees_queryset.filter(
        is_completed=False).count()

    completion_percentage = (
            num_completed_tasks / num_tasks * 100) if num_tasks > 0 else 0

    context = {
        "num_tasks": num_tasks,
        "num_completed_tasks": num_completed_tasks,
        "num_uncompleted_tasks": num_uncompleted_tasks,
        "completion_percentage": completion_percentage,
        **graphic_tasks_per_week(user),
    }
    return render(request, "tasks/index.html", context=context)
