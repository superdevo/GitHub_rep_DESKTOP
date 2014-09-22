from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from usertrial.models import Drinker

from usertrial.forms import RegistrationForm
#------------------- Module that produces and handles CVS file format ---------------------
import csv
#---------------------Import for the PDF generation  SIMPLE -------------------------------
from reportlab.pdfgen import canvas
#---------------------Import for the PDF generation  COMPLEX ------------------------------
from cStringIO import StringIO
# import of canvas and HttpResponse is also mandatory for PDF generation
# import for the permissions check on the restricted_zone view
from django.contrib.auth.decorators import permission_required, login_required


def load_template(request, which_view):
    return render_to_response(which_view, context_instance=RequestContext(request))

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/usertrial/profile/')
    if request.method == 'POST':
        f = RegistrationForm(request.POST)
        if f.is_valid():
                user = User.objects.create_user(username= f.cleaned_data['username'], email= f.cleaned_data['email'], password= f.cleaned_data['password'], first_name = f.cleaned_data['name'])
                user.save()

                drinker = Drinker.objects.get(user=user)
                drinker.username = f.cleaned_data['username']
                drinker.name = f.cleaned_data['name']
                drinker.save()

                user = authenticate(username=request.POST['username'], password=request.POST['password'])

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/usertrial/profile/')
                else:
                    return HttpResponseRedirect('/usertrial/failed/') 
        return render_to_response('register.html', {'form' : f }, context_instance=RequestContext(request))       
    else:
        """ user is not submitting form, show it"""
        form = RegistrationForm()
        return render_to_response('register.html', {'form' : form }, context_instance=RequestContext(request))


def login_view(request):
    if request.method == 'POST':

        #Check that the test cookie worked
        if request.session.test_cookie_worked():

            #the test cookie worked, so i delete it and proceed with auth/login
            request.session.delete_test_cookie()

            user = authenticate(username=request.POST.get('username', False), password=request.POST.get('password', False))
            if user is not None:
                if user.is_active:
                    login(request, user) #i have an authenticated user and i now attach a session for it.
                    request.session['user_id'] = user.id
                    return HttpResponseRedirect('/usertrial/profile/')
            else:
                return HttpResponseRedirect('/usertrial/failed/')
        else:
            #The test cookie failed, so display an error message
            return HttpResponse("Please enable cookies and try again.")
    """
    I will now test whether the browser accept cookies or not. I will need the cookie to store a session number 
    for this user.
    """
    request.session.set_test_cookie()
    return render_to_response('login.html', context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/usertrial/')

# Number of unruly passengers each year 1995 - 2005. In a real
# application this would likely come from a database or some other back-end data store.
UNRULY_PASSENGERS = [146,184,235,200,226,251,299,273,281,304,203]


"""
This is an example of how to read and write cookies per user.
"""
def set_color(request):
    if "favorite_color" in request.GET:

        #Create an HttpResponse object...
        response = HttpResponse("Your favorite color is now %s and a cookie has been set. Please click the link to check." % \
                    request.GET['favorite_color'])

        #.... and set the cookie on the response
     
        response.set_cookie("favorite_color",
                    request.GET['favorite_color'])

        return response
    else:
        return HttpResponse("You didn't give a favorite color.")

def show_color(request):
    if "favorite_color" in request.COOKIES:
        return HttpResponse("Your favorite color is %s" % \
                request.COOKIES['favorite_color'])
    else:
        return HttpResponse("You don't have a favorite color.")



def unruly_passengers_csv(request):
    #Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=unruly.csv'

    #Create the CSV writer using the HttpResponse as the "file"
    writer = csv.writer(response)
    writer.writerow(['Year', 'Unruly Airline Passengers'])
    for (year, num) in zip(range(1995, 2006), UNRULY_PASSENGERS):
        writer.writerow([year,num])
    return response


def get_pdf(request):
    """
    Create the HttpResponse object with the appropriate PDF headers.
    """
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=hello.pdf'

    #Create the PDF object, using the response created as its file. See the reportlab docs for more funtionalities.

    p = canvas.Canvas(response)

    p.drawString(100, 100, 'Hello World!')
    
    #Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

def get_complex_pdf(request):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=hello-complex.pdf'

    temp = StringIO() #StringIO is a file-like object interface that is written in C
    p = canvas.Canvas(temp)
    p.drawString(100, 100, "Hello World!")
    p.setStrokeColorRGB(0.2,0.5,0.3)
    p.setFillColorRGB(1,0,1)

    p.showPage()
    p.save()

    #Get the value of the StrigIO buffer and write it to the response
    response.write(temp.getvalue())
    return response


"This is a test view that check whether a user is authenticated and had the necessary permissions."
#@permission_required('usertrial.restricted', login_url="/usertrial/login/")
@login_required #loging required and other decorators that need login redirect by default to /accounts/login
def restricted_zone(request):
    return render_to_response('restricted.html')
