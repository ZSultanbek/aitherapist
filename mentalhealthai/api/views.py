from .models import Message
from django.shortcuts import redirect, render
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the variables from .env

# Create your views here.
import google.generativeai as genai
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from vault_client import get_ai_therapist_secrets

# Настрой API-ключ
secrets = get_ai_therapist_secrets()
GENAI_API_KEY = secrets["gemini_api_key"]
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


@login_required
@csrf_exempt
def chat(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        # Get the conversation history
        history = Message.objects.filter(user=request.user).order_by("timestamp")
        # Format the conversation history for the prompt
        
        intro_prompt = (
            "Сіз психологсыз, сіздін атыныз Мен Жақынмын. "
            "Қолдау, жұмсақ және кәсіби түрде жауап беріңіз, "
            "сіз әрқашан жақынсыз екеніңізді және әңгімелесушіні тыңдауға әрқашан дайын екеніңізді есте сақтаңыз."
        )
        
        conversation_history = "\n".join([f"User: {msg.content}\nBot: {msg.response}" for msg in history])
         # Append the latest user message

        full_prompt = f"{intro_prompt}\n\n{conversation_history}\nUser: {user_message}\nBot:"
        
        
        try:
            response = model.generate_content(full_prompt)
            bot_reply = response.text  # исправлено здесь
            Message.objects.create(user=request.user, content=user_message, response=bot_reply)  # и здесь
            return JsonResponse({"response": bot_reply})  # и здесь
        except Exception as e:
            return JsonResponse({"response": "Произошла ошибка. Попробуйте позже."})
    else:
        history = Message.objects.filter(user=request.user).order_by("timestamp")
        return render(request, "chat.html", {"history": history})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def home(request):
    return render(request, "home.html")