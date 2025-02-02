from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FAQ
from .serializers import FAQSerializer

@api_view(['GET'])
def faq_list(request):
    lang = request.query_params.get('lang', 'en')
    
    faqs = FAQ.objects.all()
    data = []
    
    for faq in faqs:
        if lang == 'hi':
            data.append({
                'question': faq.question_hi if faq.question_hi else faq.question,
                'answer': faq.answer_hi if faq.answer_hi else faq.answer
            })
        elif lang == 'bn':
            data.append({
                'question': faq.question_bn if faq.question_bn else faq.question,
                'answer': faq.answer_bn if faq.answer_bn else faq.answer
            })
        else:
            data.append({
                'question': faq.question,
                'answer': faq.answer
            })
    
    return Response(data)

from django.shortcuts import render
from .models import FAQ

def faq_list(request):
    # Fetch all FAQs from the database
    faqs = FAQ.objects.all()
    return render(request, 'faqs/faq_list.html', {'faqs': faqs})
