from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import MyTicket, MyUser
from .forms import TicketForm, SignupForm


# ── AUTH VIEWS ──────────────────────────────────────────────
def signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect('/')
        else:
            form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    """Display and process the login form."""
    if request.user.is_authenticated:
        return redirect('home')

    form_errors = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            form_errors = True  # tells template to show error

    return render(request, 'login.html', {'form': type('F', (), {'errors': form_errors})()})


def logout_view(request):
    """Log the user out and redirect to login."""
    logout(request)
    return redirect('login')


# ── TICKET VIEWS ─────────────────────────────────────────────

@login_required
def home(request):
    """List all tickets, newest first."""
    tickets = MyTicket.objects.select_related(
        'creator', 'user_assigned_to', 'user_who_completed'
    ).order_by('-date')
    return render(request, 'home.html', {'tickets': tickets})


@login_required
def ticket_detail(request, pk):
    """Show a single ticket's details."""
    ticket = get_object_or_404(MyTicket, pk=pk)
    return render(request, 'ticket_detail.html', {'ticket': ticket})


@login_required
def ticket_create(request):
    """Create a new ticket."""
    users = MyUser.objects.filter(is_active=True)

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.creator = request.user   # auto-set creator to logged-in user
            ticket.save()
            messages.success(request, f'Ticket "{ticket.title}" created successfully.')
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm()

    return render(request, 'ticket_form.html', {
        'form': form,
        'users': users,
        'ticket': None,           # None signals "create" mode to template
    })


@login_required
def ticket_edit(request, pk):
    """Edit an existing ticket (only creator or staff)."""
    ticket = get_object_or_404(MyTicket, pk=pk)
    users  = MyUser.objects.filter(is_active=True)

    if request.user != ticket.creator and not request.user.is_staff:
        messages.error(request, 'You can only edit tickets you created.')
        return redirect('ticket_detail', pk=pk)

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket updated.')
            return redirect('ticket_detail', pk=pk)
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'ticket_form.html', {
        'form': form,
        'users': users,
        'ticket': ticket,         # non-None signals "edit" mode
    })


@login_required
def ticket_delete(request, pk):
    """Delete a ticket (only creator or staff)."""
    ticket = get_object_or_404(MyTicket, pk=pk)

    if request.user != ticket.creator and not request.user.is_staff:
        messages.error(request, 'You can only delete tickets you created.')
        return redirect('ticket_detail', pk=pk)

    if request.method == 'POST':
        title = ticket.title
        ticket.delete()
        messages.success(request, f'Ticket "{title}" deleted.')
        return redirect('home')

    # GET request → show confirmation page
    return render(request, 'ticket_confirm_delete.html', {'ticket': ticket})


# ── USER VIEWS ───────────────────────────────────────────────

@login_required
def user_profile(request, pk):
    """Show a user's profile, assigned tickets, and created tickets."""
    profile_user    = get_object_or_404(MyUser, pk=pk)
    assigned_tickets = MyTicket.objects.filter(user_assigned_to=profile_user).order_by('-date')
    created_tickets  = MyTicket.objects.filter(creator=profile_user).order_by('-date')
    return render(request, 'user_profile.html', {
        'profile_user':     profile_user,
        'assigned_tickets': assigned_tickets,
        'created_tickets':  created_tickets,
    })

