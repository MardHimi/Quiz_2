from django.urls import path
from .views import LoginView, RegistrationView, UserDashboardView, AdddebtView, payDebtView, logout_view

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('pay-debt/<int:debt_id>', payDebtView.as_view(), name='pay-debt'),
    path('add-debt/', AdddebtView.as_view(), name='add-debt'),
    path('logout/', logout_view, name='logout')
]