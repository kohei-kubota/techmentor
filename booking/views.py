from django.shortcuts import render

# Create your views here.
def about(request):
    return render(request, 'booking/about.html', {}) #context_instance=RequestContext(request)


