from django.urls import path, include
# from .views import  home
from .views import HomeTemplateView, AppointmentTemplateView, ManageAppointmentTemplateView

urlpatterns = [
    # path('', home, name='home'),
    path('', HomeTemplateView.as_view(), name='home'),
    path('make-an-appointment/', AppointmentTemplateView.as_view(), name='appointment'),
    path('manage-appointments/', ManageAppointmentTemplateView.as_view(), name='manage'),
]
