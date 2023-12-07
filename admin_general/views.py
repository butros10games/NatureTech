from django.shortcuts import render

# Create your views here.
def admin_index(request):
    return render(request, 'boer-admin/admin_general/admin_index.html')