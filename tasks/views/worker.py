from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import WorkerSearchForm, RegistrationForm, SelectAvatarForm
from tasks.models import Worker


@login_required
def worker_get_update_profile(request):
    user = request.user

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        position = request.POST.get("position")

        user.first_name = first_name
        user.last_name = last_name
        user.position.name = position
        with transaction.atomic():
            user.save()
            user.position.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("tasks:workers-list")

    return render(
        request,
        "tasks/user_profile.html",
        {"user": user}
    )


class WorkersListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    context_object_name = "workers_list"
    template_name = "tasks/workers_list.html"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = WorkerSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset().select_related("position")
        form = WorkerSearchForm(self.request.GET)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            position = form.cleaned_data.get("position")

            if username:
                queryset = queryset.filter(username__icontains=username)
            if position:
                queryset = queryset.filter(position=position)

        return queryset


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = RegistrationForm
    template_name = "registration/sign_up.html"
    success_url = reverse_lazy("tasks:home_page")


class WorkersDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker


class SelectAvatarView(LoginRequiredMixin, generic.View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = SelectAvatarForm()

        return render(
            request,
            "tasks/avatar_select.html",
            context={"form": form}
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = SelectAvatarForm(request.POST)

        if form.is_valid():
            user = request.user

            split_url = form.cleaned_data["avatar"].split("/")
            user.avatar = "/".join([split_url[-2], split_url[-1]])
            user.save()

            return redirect("tasks:worker-profile")

        return render(
            request,
            "tasks/avatar_select.html",
            context={"form": form}
        )
