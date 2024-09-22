from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from django.views import generic

from tasks.models import Task
from tasks.utils import Calendar


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "tasks/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        month = self.request.GET.get("month")
        year = self.request.GET.get("year")
        if month and year:
            today = datetime.date(int(year), int(month), 1)
        else:
            today = datetime.date.today()

        cal = Calendar(today.year, today.month)
        html_cal = cal.formatmonth(user=user, withyear=True)

        next_month = today.replace(day=28) + datetime.timedelta(days=4)
        next_month = next_month.replace(day=1)
        prev_month = today.replace(day=1) - datetime.timedelta(days=1)
        prev_month = prev_month.replace(day=1)

        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = f'month={prev_month.month}&year={prev_month.year}'
        context["next_month"] = f'month={next_month.month}&year={next_month.year}'
        return context
