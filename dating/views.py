from django.shortcuts import render

def dating_page(request):
    return render(request, 'dating/dating_page.html')