# views_api.py


from django.shortcuts import render, redirect


  
#-----------------------------------------
# /api/
#-----------------------------------------

# need custom auth if not behin IDP
def index(request):

    str_headers = "none"

    context={}
    context["env"] = str_headers
    context["title"] = "API"

    return render(request, 'app_sirene/base.html', context)
    


    