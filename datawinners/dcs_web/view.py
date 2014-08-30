from django.shortcuts import render_to_response


def terms_and_conditions(request):
    return render_to_response("terms_conditions.html")

def home(request):
    return render_to_response("home.html")