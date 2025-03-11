import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment  # Make sure you have a Payment model if you wish to record payments


@login_required
def upgrade_view(request):
    """
    Displays the 'Upgrade to Premium' page and, upon POST, redirects to Stripe Checkout.
    """
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY  # Use your secret key from settings

        try:
            # Create a new Stripe Checkout Session for a £100 payment (10000 pence)
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': "Premium Package for Master Students",
                        },
                        'unit_amount': 10000,  # 100.00 GBP in pence
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/payments/success/'),
                cancel_url=request.build_absolute_uri('/payments/cancel/'),
            )
            return redirect(session.url, code=303)
        except Exception as e:
            # Optionally log or handle the error more gracefully
            print("Stripe Error:", e)
            return render(request, 'payments/upgrade_error.html', {'error': str(e)})

    # GET request: show the upgrade page
    return render(request, 'payments/upgrade.html')


@login_required
def payment_success_view(request):
    """
    Marks the user as premium and records the payment after successful checkout.
    """
    # Mark user as premium
    request.user.profile.premium_member = True
    request.user.profile.save()

    # Optionally, record the payment
    Payment.objects.create(
        user=request.user,
        amount=100.00,
        successful=True
    )

    return render(request, 'payments/upgrade_success.html')


@login_required
def payment_cancel_view(request):
    """
    Displays a cancellation page if the user quits the Stripe checkout.
    """
    return render(request, 'payments/payment_cancel.html')
