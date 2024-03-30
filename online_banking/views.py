from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, UserProfileForm, paymentForm, AddDebtForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User_profile, Account, debt, card

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'banking/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_dashboard')

        return render(request, 'banking/login.html', {'form': form})


class RegistrationView(View):
    def get(self, request):
        user_form = RegistrationForm()
        profile_form = UserProfileForm()

        return render(request, 'banking/registration.html', {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        user_form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('login')

        return render(request, 'banking/registration.html', {"user_form":user_form, "profile_form":profile_form})




class UserDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user_profile = User_profile.objects.get(user=request.user)
        accounts = Account.objects.filter(owner=user_profile)
        Debt = debt.objects.filter(user=user_profile, amount__gt=0)
        return render(request, 'banking/dashboard.html',
                      {'user_profile': user_profile, 'accounts': accounts, 'debts': Debt})


class payDebtView(LoginRequiredMixin, View):
    def post(self, request, debt_id):
        Debt = get_object_or_404(debt, id=debt_id)
        form = paymentForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']

            if amount <= request.user.user_profile.balance:
                Debt.pay_debt(amount)
                request.user.user_profile.balance -= amount
                request.user.user_profile.save()
                return redirect('user_dashboard')

            else:
                return redirect('user_dashboard')
        return redirect('user_dashboard')


class AdddebtView(LoginRequiredMixin, View):
    def post(self, request):
        form = AddDebtForm(request.POST)
        if form.is_valid():
            Debt = form.save(commit=False)
            Debt.user = request.user.user_profile
            Debt.save()
            return redirect('user_dashboard')
        return render(request, 'banking/dashboard.html', {'add_debt_form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

