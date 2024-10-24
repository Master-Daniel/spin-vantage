import logging

from app.draw import calc_wheel_rotations, get_prize_result, set_code_used, get_prize
from app.forms import DrawForm, LoginForm, RegisterForm, DepositForm, WithdrawForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout  # Import logout
from app.models import Draw, Prize, UniqueCode
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Get an instance of a logger
logger = logging.getLogger(__name__)

def draw_spin(request):
    logger.info(f"Draw_new with {request.method}")
    prizes = get_list_or_404(Prize)

    if request.method == "POST":
        form = DrawForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            instance = form.save(commit=False)
            instance.date = timezone.now()

            try:
                ucode = UniqueCode.objects.get(code=code)
            except Exception:
                ucode = UniqueCode(code='NO CODE', used=False, prize=None)

            if ucode.prize:
                instance.rotation = calc_wheel_rotations(ucode.prize.id)
                instance.prize = ucode.prize
            else:
                instance.rotation = calc_wheel_rotations()
                instance.prize = get_prize(get_prize_result(instance.rotation))
            instance.save()

            set_code_used(code, True)

            return render(request, 'index.html',
                          {'form': form, 'spin': True, 'result': instance.pk, 'rotation': instance.rotation, 'prizes': prizes})
        else:
            logger.warning(f"invalid form else => {form.is_valid()} {form.errors}")
            form = DrawForm(request.POST)
    else:
        form = DrawForm()

    return render(request, 'index.html', {'form': form, 'prizes': prizes})

def draw_result(request, pk):
    prizes = get_list_or_404(Prize)
    draw = get_object_or_404(Draw, pk=pk)
    logger.info(f"Draw with {request.method} for id {draw.pk}")
    prize = get_prize(draw.prize.pk)
    logger.info(f"Prize {prize.pk}, {prize.label}, {prize.winner}")
    if prize.try_again:
        set_code_used(draw.code, False)
    return render(request, 'draw.html', {'prizes': prizes, 'result_draw': draw, 'result_prize': prize})

@login_required
def dashboard(request):
    form = DrawForm()

    # Get the user instance directly
    user = request.user 

    prizes = get_list_or_404(Prize)
    return render(request, 'index.html', {
        'form': form,
        'prizes': prizes,
        'user': user,  # You can pass the user instance directly
    })

@login_required
def deposit(request):
    form = DepositForm()
    return render(request, 'deposit.html',  {'form': form})

@login_required
def withdraw(request):
    form = WithdrawForm()
    return render(request, 'withdraw.html', {"form": form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Use username instead of email since Django defaults to username
            username = form.cleaned_data['username']  # Change here to use username
            password = form.cleaned_data['password']

            # Authenticate using the username
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)  # Use auth_login to avoid conflicts
                return redirect('/dashboard')
            else:
                form.add_error(None, 'Invalid username or password.')
        return render(request, 'authentication/login.html', {'form': form})
    else:
        form = LoginForm()
        if request.user.is_authenticated:
            return redirect('/dashboard')
        else:
            return render(request, 'authentication/login.html', {'form': form})
        
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully.")
            return redirect('/')
    else:
        form = RegisterForm()
        return render(request, 'authentication/register.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('/')
