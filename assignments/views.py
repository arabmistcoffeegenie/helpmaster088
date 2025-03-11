# assignments/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Assignment
from .forms import AssignmentForm
from datetime import datetime
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def submit_assignment(request):
    """
    Handles assignment submission for premium members.
    This version uses AssignmentForm to capture all fields including the uploaded file.
    """
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.payment_status = 'premium'
            assignment.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm()
    return render(request, 'assignments/submit_assignment.html', {'form': form})


@login_required
def assignment_list(request):
    """
    Lists all assignments for the logged-in user.
    """
    assignments = Assignment.objects.filter(student=request.user)
    return render(request, 'assignments/assignment_list.html', {'assignments': assignments})


@login_required
def pay_per_assignment(request):
    """
    Handles the non-premium (pay-per-assignment) flow.
    (Note: File uploads aren’t handled in this flow.)
    """
    if request.method == 'POST':
        title = request.POST.get('title') or "Untitled Assignment"
        degree = request.POST.get('degree') or ""
        module = request.POST.get('module') or ""
        instructions = request.POST.get('instructions') or ""
        deadline_str = request.POST.get('deadline')
        parsed_deadline = None
        if deadline_str:
            try:
                parsed_deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            except ValueError:
                parsed_deadline = None

        request.session['pending_assignment'] = {
            'title': title,
            'degree': degree,
            'module': module,
            'instructions': instructions,
            'deadline': deadline_str,
        }
        
        # Create a Stripe Checkout Session for £39 (3900 pence)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'unit_amount': 3900,
                    'product_data': {
                        'name': 'Assignment Submission Fee',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/assignments/pay-per-assignment/success/'),
            cancel_url=request.build_absolute_uri('/assignments/pay-per-assignment/'),
            customer_email=request.user.email,
        )
        return redirect(checkout_session.url)
    else:
        return render(request, 'assignments/pay_per_assignment.html')


@login_required
def pay_per_assignment_success(request):
    """
    Called after successful payment. Creates a new Assignment record using the pending data
    stored in the session. (File upload is not handled in this flow.)
    """
    pending_data = request.session.get('pending_assignment')
    if not pending_data:
        return redirect('pay_per_assignment')

    deadline_str = pending_data.get('deadline')
    parsed_deadline = None
    if deadline_str:
        try:
            parsed_deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            parsed_deadline = None

    assignment = Assignment.objects.create(
        student=request.user,
        title=pending_data.get('title'),
        degree=pending_data.get('degree'),
        module=pending_data.get('module'),
        instructions=pending_data.get('instructions'),
        deadline=parsed_deadline,
        payment_status='paid'
    )

    del request.session['pending_assignment']
    
    return render(request, 'assignments/pay_per_assignment_success.html', {'assignment': assignment})
