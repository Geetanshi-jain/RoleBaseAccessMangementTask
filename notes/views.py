from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Profile
from django.contrib.auth import logout


def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=email).exists():
            return render(request, "notes/signup.html", {"msg": "User already exists"})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        Profile.objects.create(user=user, role=role)

        return redirect("login")

    return render(request, "notes/signup.html")




def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "notes/login.html", {"msg": "Invalid Credentials"})

    return render(request, "notes/login.html")


from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    profile = request.user.profile
    
    if profile.role == "user":
        return redirect("user_dashboard")

    elif profile.role == "manager":
        return redirect("manager_dashboard")

    else:
        return redirect("admin_dashboard")



from .models import Notes
from django.contrib.auth.decorators import login_required

@login_required
def user_dashboard(request):
    notes = Notes.objects.filter(user=request.user)
    return render(request, "notes/user_dashboard.html", {"notes": notes})


from .models import Notes
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings


@login_required
def add_note(request):
    if request.method == "POST":
        text = request.POST.get("note")
        is_work = request.POST.get("is_work")

        Notes.objects.create(
            user=request.user,
            notes=text,
            is_work=True if is_work == "True" else False
        )

    return redirect("user_dashboard")


@login_required
def request_delete(request, note_id):
    note = get_object_or_404(Notes, id=note_id)

    if note.user == request.user and note.is_work:
        note.deletion_request = True
        note.manager_request = "pending"
        note.save()

    return redirect("user_dashboard")


@login_required
def manager_dashboard(request):
    if request.user.profile.role != "manager":
        return redirect("dashboard")

    notes = Notes.objects.filter(
        is_work=True,
        deletion_request=True,
        manager_request="pending"
    )

    return render(request, "notes/manager_dashboard.html", {"notes": notes})



@login_required
def approve_note(request, note_id):
    note = get_object_or_404(Notes, id=note_id)

    if request.user.profile.role == "manager":
        note.manager_request = "approved"
        note.save()

        # Email to user
        send_mail(
            "Deletion Request Approved",
            "Your work note deletion request is approved.",
            settings.EMAIL_HOST_USER,
            [note.user.email],
        )

    return redirect("manager_dashboard")


@login_required
def reject_note(request, note_id):
    note = get_object_or_404(Notes, id=note_id)

    if request.user.profile.role == "manager":
        note.manager_request = "rejected"
        note.save()

        send_mail(
            "Deletion Request Rejected",
            "Your work note deletion request is rejected.",
            settings.EMAIL_HOST_USER,
            [note.user.email],
        )

    return redirect("manager_dashboard")


@login_required
def admin_dashboard(request):
    if request.user.profile.role != "admin":
        return redirect("dashboard")

    notes = Notes.objects.filter(
        manager_request="approved",
        is_active=True
    )

    return render(request, "notes/admin_dashboard.html", {"notes": notes})



@login_required
def admin_delete(request, note_id):
    note = get_object_or_404(Notes, id=note_id)

    if request.user.profile.role == "admin":
        note.is_active = False
        note.save()

        send_mail(
            "Note Deleted",
            "Your work note has been deleted by admin.",
            settings.EMAIL_HOST_USER,
            [note.user.email],
        )

    return redirect("admin_dashboard")


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
