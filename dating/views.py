from django.shortcuts import render
from users.models import User
import random

def dating_page(request):
    male_user = None
    female_user = None

    if request.method == 'POST' and request.user.is_authenticated:
        current_user = request.user
        
        # Exclude the current user from the lists
        other_male_users = list(User.objects.filter(gender='M').exclude(pk=current_user.pk))
        other_female_users = list(User.objects.filter(gender='F').exclude(pk=current_user.pk))

        if current_user.gender == 'M':
            male_user = current_user
            if other_female_users:
                female_user = random.choice(other_female_users)
        elif current_user.gender == 'F':
            female_user = current_user
            if other_male_users:
                male_user = random.choice(other_male_users)

    context = {
        'male_user': male_user,
        'female_user': female_user,
    }
    return render(request, 'dating/dating_page.html', context)