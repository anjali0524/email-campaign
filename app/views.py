from django.shortcuts import render, redirect
from .models import Subscriber
from .forms import CampaignForm, SubscriberForm
from django.http import HttpResponse
from app.interactions.send_campaign_email import send_campaign_email
from .models import Campaign , Subscriber
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Subscriber
from rest_framework import status
from celery import shared_task





def home(request):
    return HttpResponse('Email Apis', status=200)

@api_view(['POST'])
def add_subscriber(request):
    print('here')
    if request.method == 'POST':
        email = request.data.get('email')
        first_name = request.data.get('first_name')

        if email and first_name:
            # Check if the subscriber already exists
            existing_subscriber = Subscriber.objects.filter(email=email).first()

            if existing_subscriber:
                return Response({'detail': 'Subscriber already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new subscriber
            subscriber = Subscriber(email=email, first_name=first_name)
            subscriber.save()

            return Response({'detail': 'Subscriber added successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Email and first_name are required fields.'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def unsubscribe(request):
    try:
        subscriber = Subscriber.objects.get(email=request.data.get('email'))
        subscriber.active = 'inactive'
        subscriber.save()
        return render(request, 'unsubscribe_success.html')
    except Subscriber.DoesNotExist:
        return render(request, 'unsubscribe_error.html', {'error_message': 'Subscriber not found.'})

@shared_task
@api_view(['POST'])
def send_campaign(request):
    form = CampaignForm(request.POST)
    if form.is_valid():
        # Process and send the campaign
        campaign = form.save()  # Assuming you've defined the CampaignForm properly
        send_campaign_email(campaign)  # Use the function from the previous example to send the campaign
        return render(request, 'campaign_sent.html', {'campaign': campaign})

    return render(request, 'send_campaign.html', {'form': form})





def test_send_campaign_email(request):
    # Create a test Campaign object
    test_campaign = Campaign(
        subject="Test Campaign",
        preview_text="This is a test campaign.",
        article_url="https://cogoport-production.sgp1.digitaloceanspaces.com/e23ee14dc896fb4a366ba7c2490ade31/DN%20164434.pdf",
        html_content="<p>This is a test email with HTML content.</p>",
        plain_text_content="This is a test email with plain text content.",
        published_date = "2023-04-12"
        # to_email="sirius.sonu2405@gmail.com"  # Replace with a test recipient's email
    )

    # Call the email sending function with the test Campaign object
    test = send_campaign_email(test_campaign)
    if test == True:
        return HttpResponse("Test email sent successfully!")
    else:
        return HttpResponse("Test email got failed!")

