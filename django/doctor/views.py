from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from .models import Appointment
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.template import Context
from django.template.loader import render_to_string, get_template



# def home(request):
#     return HttpResponse('HI')
class HomeTemplateView(TemplateView):
    template_name = "index.html"

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        email = EmailMessage(
            subject=f"{name} from doctor Family.",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]
        )
        email.send()
        return HttpResponse("Email sent successfully")


class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"

    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")

        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=message
        )

        appointment.save()

        messages.add_message(request, messages.SUCCESS,
                             f"Thank You {fname}  for making an appointment , we will email you ASAP!")
        return HttpResponseRedirect(request.path)


class ManageAppointmentTemplateView(ListView):
    template_name = "manage-appointments.html"
    model = Appointment
    context_object_name = "appointments"
    login_required = True
    paginate_by = 3

    def post(self, request):
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.accepted = True
        appointment.accepted_date = datetime.datetime.now()
        appointment.save()

        data = {
            "fname": appointment.first_name,
            "date": date
        }
        message = get_template('email.html').render(data)

        email = EmailMessage(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.email],
        )
        email.content_subtype = "html"

        email.send()

        messages.add_message(request, messages.SUCCESS,
                             f"You have accepted the appointment of {appointment.first_name}")
        return HttpResponseRedirect(request.path)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({
            "appointments": appointments,
            "title": "Manage Appointments"
        })
        return context

# class ManageAppointmentTemplateView(LoginRequiredMixin, ListView):
#     template_name = 'manage-appointments.html'
#     model = Appointment
#     context_object_name = 'appointments'
#     paginate_by = 3
#
#     def get_queryset(self, *args, **kwargs):
#         super().get_queryset(*args, **kwargs).filter(
#             first_name=self.request.user
#         ).order_by('-sent_date')
