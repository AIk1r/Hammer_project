import random
import string

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import User


def register(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            code = random.randint(1000, 9999)
            cache.set(phone_number, code, 120)

            # Store the code in session
            request.session['code'] = code

            print(f"Generated code for {phone_number} is {code}")
            return redirect('verify')
        else:
            code = random.randint(1000, 9999)
            cache.set(phone_number, code, 120)

            request.session['code'] = code

            return redirect('verify')
    return render(request, 'register.html')


def verify(request):
    # Fetch the code from session
    code = request.session.get('code', 'Not available')

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        entered_code = request.POST.get('code')
        stored_code = cache.get(phone_number)
        if str(stored_code) == entered_code:
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                user = User.objects.create(phone_number=phone_number)

            # Create session for the user
            request.session['session_key'] = user.phone_number
            return redirect('profile')  # Redirect to the user's profile page

        else:
            return HttpResponse("Invalid code.")
    # Pass the code to the template here
    return render(request, 'verify.html', {'code': code})


def profile(request):
    phone_number = request.session.get('session_key')

    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        return redirect('verify')  # Redirect to the verification page if the user does not exist

    if request.method == 'POST':
        invite_code = request.POST.get('invite_code')

        if invite_code:
            user.used_invite_code = invite_code
            user.save()

    # Check if the user has an invite code
    if not user.invite_code:
        # Generate invite code if it does not exist
        invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        user.invite_code = invite_code
        user.save()

    # Check if a user has been invited
    invited_by = User.objects.filter(used_invite_code=user.invite_code).first()
    if invited_by and invited_by != user:  # Prevent self-invitation
        if not user.invited_by:  # Check if the user has already been invited
            user.invited_by = invited_by
            user.save()

    # Get the users invited by the current user who have used the invite code
    invited_users = User.objects.filter(invited_by=user)

    # Create a list of invited user phone numbers
    invited_user_phone_numbers = [invited_user.phone_number for invited_user in invited_users]

    # Check if the user has already entered an invite code
    has_entered_invite_code = user.invited_by is not None or user.used_invite_code is not None

    return render(request, 'profile.html', {'user': user, 'invited_users': invited_user_phone_numbers,
                                            'has_entered_invite_code': has_entered_invite_code})


# def get_users(request):
#     users = User.objects.all()
#     data = []
#     for user in users:
#         user_data = {
#             'id': user.id,
#             'phone_number': user.phone_number,
#             'invite_code': user.invite_code,
#             'invited_by': user.invited_by.phone_number if user.invited_by else None,
#             'used_invite_code': user.used_invite_code
#         }
#         data.append(user_data)
#     return JsonResponse(data, safe=False)
