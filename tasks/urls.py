from django.urls import path

from tasks.views import (
    index,
    create_task,
    complete_task,
    user_profile,
    WorkersListView,
    WorkersDetailView,
    AuthorCreateView,
    CalendarView,
    TaskDetailView,
    SelectAvatarView,
    TaskUpdateView,
    TaskDeleteView,
)

app_name = "tasks"

urlpatterns = [
    path("home_page/", index, name="home_page"),
    path("workers/", WorkersListView.as_view(), name="workers-list"),
    path("workers/<int:pk>/", WorkersDetailView.as_view(), name="workers-detail"),
    path("accounts/sign_up/", AuthorCreateView.as_view(), name="sign_up"),
    path("calendar/", CalendarView.as_view(), name="calendar"),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('create_task/', create_task, name='task-create'),
    path('task/<int:pk>/complete/', complete_task, name='complete-task'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('profile/update/', user_profile, name='user-profile'),
    path('profile/select_avatar/', SelectAvatarView.as_view(), name='select-avatar'),

]
