from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

from django import forms
from django.contrib.auth.forms import UserCreationForm
from tasks.models import Position, Worker, Task


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TimeInput(
            attrs={"placeholder": "Search by username"}
        )
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        label="Position",
        empty_label="All Positions",
    )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Worker
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "position"
        ]


class TaskCreationForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={
            "class": "assignee-checkboxes"}
        )
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "assignees"
        ]
        widgets = {
            "deadline": forms.DateInput(
                attrs={"type": "date", "min": timezone.now().date()}
            ),
            "priority": forms.Select(),
        }

    def __init__(self, positions=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if positions:
            if len(positions) == 2:
                self.fields["assignees"].queryset = get_user_model().objects.filter(
                    Q(position__name=positions[0]) | Q(position__name=positions[1])
                )
            else:
                self.fields["assignees"].queryset = get_user_model().objects.filter(
                    position__name=positions[0]
                )
        else:
            self.fields["assignees"].queryset = get_user_model().objects.all()


class SelectAvatarForm(forms.ModelForm):
    avatar = forms.CharField(max_length=100)

    class Meta:
        model = get_user_model()
        fields = ("avatar", )
