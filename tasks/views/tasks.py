from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import TaskCreationForm
from tasks.models import Task


@login_required
def create_task(request):
    user = request.user
    if user.position.name == "Project Manager":
        positions = ("Project Manager",)
    else:
        positions = ("Project Manager", user.position.name)

    if request.method == "GET":
        form = TaskCreationForm(positions=positions)

    if request.method == "POST":
        form = TaskCreationForm(positions=positions, data=request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.giver = user
            task.is_completed = False
            task.save()
            form.save_m2m()
            return redirect("tasks:workers-list")

    context = {"form": form}
    return render(request, "tasks/task_create.html", context=context)


@login_required
def complete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.is_completed = True
    task.save()
    return redirect("tasks:task-detail", pk=task.pk)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView
):
    model = Task
    form_class = TaskCreationForm
    template_name = "tasks/task_update.html"

    def form_valid(self, form):
        messages.success(self.request, "Task updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        task = self.get_object()
        return (self.request.user == task.giver or
                self.request.user.position.name == "Project Manager")


class TaskDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView
):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy('tasks:calendar')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Task deleted successfully!")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        task = self.get_object()
        return (self.request.user == task.giver or
                self.request.user.position.name == "Project Manager")
