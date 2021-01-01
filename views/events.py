from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from classic_tetris_project.models import Event
from classic_tetris_project.util import lazy
from .base import BaseView


class EventView(BaseView):
    @lazy
    def event(self):
        try:
            return Event.objects.get(slug=self.kwargs["event_slug"])
        except Event.DoesNotExist:
            raise Http404()


class IndexView(EventView):
    def get(self, request, event_slug):
        return render(request, "event/index.html", {
            "event": self.event,
            "user_ineligible_reason": self.event.user_ineligible_reason(self.current_user),
            "approved_qualifiers": list(self.event.qualifiers.filter(approved=True)
                                        .order_by("-qualifying_score")),
            "pending_qualifiers": list(self.event.qualifiers.filter(approved=None)
                                       .order_by("-qualifying_score")),
        })


class QualifyView(LoginRequiredMixin, EventView):
    def get(self, request, event_slug):
        if not self.event.is_user_eligible(self.current_user):
            return self.ineligible_redirect()

        return render(request, "event/qualify.html", {
            "event": self.event,
            "form": (self.event.form_class)(),
        })

    def post(self, request, event_slug):
        if not self.event.is_user_eligible(self.current_user):
            return self.ineligible_redirect()

        form = (self.event.form_class)(request.POST)
        if form.is_valid():
            form.save(self.event, self.current_user)
            messages.info(self.request, "Qualifier successfully recorded.")
            return redirect(reverse("event:index", args=[self.event.slug]))
        else:
            return render(request, "event/qualify.html", {
                "event": self.event,
                "form": form,
            })

    def ineligible_redirect(self):
        messages.info(self.request,
                      "You are no longer able to qualify for this event. If this is in error, "
                      "please contact a moderator.")
        return redirect(reverse("event:index", args=[self.event.slug]))
