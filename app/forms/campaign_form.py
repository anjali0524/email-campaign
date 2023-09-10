from django import forms
from app.models.campaign import Campaign

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['subject', 'preview_text', 'article_url', 'html_content', 'plain_text_content', 'published_date']
