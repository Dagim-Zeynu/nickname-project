from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Department, Profile
from django.contrib.auth.models import User
from .models import Nickname, Reaction, Report
from .forms import NicknameForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib import messages

@login_required
def department_list(request):
    if not request.user.is_authenticated:
        return redirect('home')
    departments = Department.objects.all().order_by('name')
    return render(request, 'nicknames/department_list.html', {'departments': departments})

@login_required
def student_list(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    students = Profile.objects.filter(department=department).exclude(user=request.user)
    return render(request, 'nicknames/student_list.html', {
        'department': department,
        'students': students
    })

@login_required
def student_detail(request, student_id):
    student = get_object_or_404(User, id=student_id)
    if student == request.user:
        nicknames = Nickname.objects.filter(given_to=student).annotate(
            reaction_count=Count('reactions')
        ).order_by('-reaction_count', '-created_at')
    else:
        nicknames = (Nickname.objects.filter(given_to=student, given_by=request.user) | 
                    Nickname.objects.filter(given_to=student, given_by__in=User.objects.exclude(id=request.user.id))
        ).annotate(
            reaction_count=Count('reactions')
        ).order_by('-reaction_count', '-created_at')
    
    return render(request, 'nicknames/student_detail.html', {
        'student': student,
        'nicknames': nicknames,
        'is_self': student == request.user
    })

@login_required
def give_nickname(request, student_id):
    student = get_object_or_404(User, id=student_id)
    
    if student == request.user:
        messages.error(request, "You can't give a nickname to yourself!")
        return redirect('nicknames:student_list', department_id=student.profile.department.id)
    
    if request.method == 'POST':
        form = NicknameForm(request.POST)
        if form.is_valid():
            nickname = form.save(commit=False)
            nickname.given_to = student
            nickname.given_by = request.user
            nickname.save()
            return redirect('nicknames:student_detail', student_id=student_id)
    else:
        form = NicknameForm()
    
    return render(request, 'nicknames/give_nickname.html', {
        'form': form,
        'student': student
    })

@require_POST
@login_required
def add_reaction(request, nickname_id, reaction_type):
    nickname = get_object_or_404(Nickname, id=nickname_id)
    
    # Check if reaction type is valid
    if reaction_type not in [choice[0] for choice in Reaction.REACTION_CHOICES]:
        return JsonResponse({'success': False, 'error': 'Invalid reaction type'})
    
    # Get existing reaction for this user on this nickname
    existing_reaction = Reaction.objects.filter(
        nickname=nickname,
        user=request.user
    ).first()
    
    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            # If same reaction, remove it
            existing_reaction.delete()
            new_count = Reaction.objects.filter(
                nickname=nickname,
                reaction_type=reaction_type
            ).count()
            return JsonResponse({
                'success': True,
                'count': new_count,
                'action': 'removed',
                'old_type': reaction_type
            })
        else:
            # If different reaction, update it and return both counts
            old_type = existing_reaction.reaction_type
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
            
            # Get updated counts for both old and new reaction types
            old_count = Reaction.objects.filter(
                nickname=nickname,
                reaction_type=old_type
            ).count()
            new_count = Reaction.objects.filter(
                nickname=nickname,
                reaction_type=reaction_type
            ).count()
            
            return JsonResponse({
                'success': True,
                'count': new_count,
                'action': 'changed',
                'old_type': old_type,
                'old_count': old_count
            })
    else:
        # Create new reaction
        Reaction.objects.create(
            nickname=nickname,
            user=request.user,
            reaction_type=reaction_type
        )
        new_count = Reaction.objects.filter(
            nickname=nickname,
            reaction_type=reaction_type
        ).count()
        return JsonResponse({
            'success': True,
            'count': new_count,
            'action': 'added'
        })

@require_POST
@login_required
def add_rating(request, student_id):
    student = get_object_or_404(User, id=student_id)
    
    if student == request.user:
        return JsonResponse({
            'success': False,
            'error': "You can't rate yourself!"
        })
    
    try:
        score = int(request.POST.get('score', 0))
        if not 1 <= score <= 10:
            raise ValueError("Score must be between 1 and 10")
            
        rating, created = Rating.objects.update_or_create(
            given_to=student,
            given_by=request.user,
            defaults={'score': score}
        )
        
        # Calculate new averages
        student_avg = student.profile.average_rating
        department_avg = student.profile.department.average_rating
        rating_count = student.profile.rating_count
        
        return JsonResponse({
            'success': True,
            'student_avg': student_avg,
            'department_avg': department_avg,
            'rating_count': rating_count,
            'stars': '★' * score + '☆' * (10 - score)
        })
        
    except (ValueError, TypeError) as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

def terms(request):
    return render(request, 'terms.html')

def home(request):
    if request.user.is_authenticated:
        return redirect('nicknames:department_list')
    return render(request, 'home.html')

@require_POST
@login_required
def report_nickname(request, nickname_id):
    nickname = get_object_or_404(Nickname, id=nickname_id)
    
    if nickname.reports.filter(reported_by=request.user).exists():
        return JsonResponse({
            'success': False,
            'error': 'You have already reported this nickname'
        })
    
    reason = request.POST.get('reason')
    if reason not in [choice[0] for choice in Report.REPORT_REASONS]:
        return JsonResponse({
            'success': False,
            'error': 'Invalid report reason'
        })
    
    Report.objects.create(
        nickname=nickname,
        reported_by=request.user,
        reason=reason,
        details=request.POST.get('details', '')
    )
    
    messages.success(request, 'Thank you for your report. We will review it shortly.')
    return JsonResponse({'success': True}) 