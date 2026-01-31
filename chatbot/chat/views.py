from django.shortcuts import render
from .services import ask_ai

def chat_bot(request):
    response = ""
    input_text = ""

    if request.method == "POST":
        input_text = request.POST.get("input_text", "").strip()

        if input_text:
            response = ask_ai(input_text)
        else:
            response = "Please type something."

    return render(request, "chat.html", {
        "response": response,
        "input_text": input_text
    })
