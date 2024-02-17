from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET



#def error_400(request, exception):
#    return render(request, "errors/400.dtl", status=400)

#def error_403(request, exception):
#    return render(request, "errors/403.dtl", status=403)

# APPEND_SLASH does not work if you do not return status=404
def error_404(request, exception):
    return render(request, "errors/404.dtl", status=404)

#def error_500(request):
#    return render(request, "errors/500.dtl", status=500)



# this evades the css styling unforunately
# def home_simple(request):
#    return HttpResponse("This page is GROOVY")


# https://adamj.eu/tech/2020/02/10/robots-txt/

@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /",
        # "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
