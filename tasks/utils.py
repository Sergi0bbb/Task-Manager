from calendar import HTMLCalendar


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(deadline__day=day)
        d = ""
        for event in events_per_day:
            d += f"<li> {event.get_html_url} </li>"
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return "<td></td>"

    def formatweek(self, theweek, events):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f"<tr> {week} </tr>"

    def formatmonth(self, user, withyear=True):
        events = user.tasks_to_do.filter(
            deadline__year=self.year, deadline__month=self.month,
        )
        cal = (
            "<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" class=\"calendar\">\n"
        )
        cal += (
            f"{self.formatmonthname(
                self.year,
                self.month,
                withyear=withyear
            )}\n"
        )
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, events)}\n"
        return cal
