import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet, Count
from django.shortcuts import render
from django.views import generic


from dto.dto import GraphicDto
import datetime as DT
from tasks.models import Task, Worker


def get_tasks_labels(query_set: QuerySet[dict]) -> list[str]:
    return [
        f"{datetime.date(
            datetime.date.today().year,
            item["deadline__month"],
            item["deadline__day"]
        ).strftime("%B %d")}"
        for item in query_set
    ]


def graphic_tasks_per_week() -> dict:
    today = DT.date.today()
    future_week = today + DT.timedelta(days=7)
    tasks_graphic_per_week = GraphicDto.get_from_query_set(
        Task.objects.filter(deadline__gte=today, deadline__lte=future_week).values(
            "deadline__day",
            "deadline__month"
        ).annotate(count=Count("name")).order_by(
            "deadline__day",
            "deadline__month"
        ),
        get_tasks_labels
    )
    return {
        "tasks_per_week": tasks_graphic_per_week,
    }


@login_required
def index(request):
    user = request.user
    assignees_queryset = Task.objects.filter(assignees=user)
    num_tasks = assignees_queryset.count()
    num_completed_tasks = assignees_queryset.filter(is_completed=True).count()
    num_uncompleted_tasks = assignees_queryset.filter(is_completed=False).count()

    context = {
        "num_tasks": num_tasks,
        "num_completed_tasks": num_completed_tasks,
        "num_uncompleted_tasks": num_uncompleted_tasks,
        **graphic_tasks_per_week(),
    }
    return render(request, "base.html", context=context)


class WorkersListView(generic.ListView):
    model = Worker
    context_object_name = "workers_list"
    template_name = "tasks/workers_list.html"
    paginate_by = 10

