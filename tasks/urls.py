from django.urls import path

from tasks.views import index, WorkersListView

app_name = "tasks"

urlpatterns = [
    path("/", index, name="index"),
    path("workers/", WorkersListView.as_view(), name="workers-list")
]
