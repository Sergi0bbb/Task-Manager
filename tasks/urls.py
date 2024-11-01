from django.urls import path

from tasks.views.calendar import CalendarView
from tasks.views.index import index
from tasks.views.tasks import (
    TaskDetailView,
    create_task,
    complete_task,
    TaskUpdateView,
    TaskDeleteView
)
from tasks.views.worker import (
    WorkersListView,
    WorkersDetailView,
    WorkerCreateView,
    SelectAvatarView,
    worker_get_update_profile
)

app_name = "tasks"

urlpatterns = [
    path("", index, name="home_page"),
    path("workers/", WorkersListView.as_view(), name="workers-list"),
    path("workers/<int:pk>/", WorkersDetailView.as_view(), name="workers-detail"),
    path("accounts/sign_up/", WorkerCreateView.as_view(), name="sign_up"),
    path("calendar/", CalendarView.as_view(), name="calendar"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create_task/", create_task, name="task-create"),
    path("tasks/<int:pk>/complete/", complete_task, name="complete-task"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("profiles/update/", worker_get_update_profile, name="worker-profile"),
    path("profiles/select_avatar/", SelectAvatarView.as_view(), name="select-avatar"),
]
