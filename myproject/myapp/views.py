from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from .models import route
from .models import Gride
from .models import message   # 👈 apna model name yaha likho
from .models import BusBooking
from .models import Feedback
# from .forms import message, FeedbackForm
from .forms import PostForm, FeedbackForm 
from django.db.models import Q



@login_required(login_url='login')
def booking(request):
    return render(request, 'Booking.html')
# Create your views here.
def home(request):
    return render(request,"headar.html")

def temp(request):
    return render(request,"temp.html")
# def search(request):
#     return render(request,"Search.html")

def perent(request):
    gride_data = Gride.objects.all()

    paginator = Paginator(gride_data, 6)  # 5 items per page

    page_number = request.GET.get('page')  # URL se page number lega
    page_obj = paginator.get_page(page_number)

    query = (request.GET.get('q') or '').strip()
    # data = route.objects.all()
    data = None

    if query:
        data = route.objects.filter(
            Q(busname__icontains=query) |
            Q(pickplace__icontains=query) |
            Q(destplace__icontains=query) 
        )

    # Combine posts and feedback for the feed
    feed_posts = list(message.objects.all().order_by("-id")[:6])
    feed_feedback = list(Feedback.objects.all().order_by("-created_at")[:6])
    
    # Combine and sort by combining the lists
    combined_feed = feed_posts + feed_feedback
    
    context = {
        "data": data,
        "query": query,
        "page_obj": page_obj,
        "feed_posts": combined_feed,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "Gride.html", context)

    return render(request, "perent.html", context)

def routes(request):
    query = request.GET.get('q') or ''

    data = route.objects.all()

    if query:
        data = route.objects.filter(
            Q(busname__icontains=query) |
            Q(pickplace__icontains=query) |
            Q(destplace__icontains=query)
        )

    paginator = Paginator(data, 10)  # 10 routes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "query": query,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "routes_list.html", context)

    return render(request, "routes_list.html", context)

def gallery(request):
    data = Gride.objects.all()

    paginator = Paginator(data, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "gallery.html", context)

    return render(request, "gallery.html", context)
#     })
# def newimg (request):
#          image = Gride.objects.all()
#          return render(request,"Gride.html",{"image":image})

# def gride_page(request):
#     data = Gride.objects.all()

#     paginator = Paginator(data, 6)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'parent.html', {'page_obj': page_obj})


# def gride_page(request):
  

# views.py
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('perent')
    else:
        form = PostForm()

    return render(request, 'perent.html', {
        'form': form,
        'feed_posts': list(message.objects.all().order_by('-id')[:6]) + list(Feedback.objects.all().order_by('-created_at')[:6]),
        'data': route.objects.all(),
        'query': None,
        'page_obj': Paginator(Gride.objects.all(), 6).get_page(1),
    })

def feed_view(request):
    return render(request, 'feed.html')

# 🔝 Back to top view
def back_to_top(request):
    return redirect('feed') 


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)   # ✅ login ho jayega
            return redirect('booking')   # 👈 yaha booking page bhejo
        else:
            return render(request, 'login.html', {
                'error': 'Invalid Username or Password'
            })
    return render(request, "login.html")

# 🔝 contact to login
def Contact_to_log(request):
    return redirect('login')
 
# def TEM(request):
#     return redirect('TEMP') 

def search_view(request):
    return render(request, 'search.html')


def bus_booking(request):

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        from_city = request.POST.get('from_city')
        to_city = request.POST.get('to_city')
        date = request.POST.get('date')
        bus_type = request.POST.get('bus_type')
        seats = request.POST.get('seats')

        booking = BusBooking.objects.create(
            name=name,
            email=email,
            phone=phone,
            from_city=from_city,
            to_city=to_city,
            date=date,
            bus_type=bus_type,
            seats=seats
        )

        # Send confirmation email
        subject = 'Bus Booking Confirmation - YatraSetu'
        message = f'''
Dear {name},

Thank you for booking with YatraSetu!

Booking Details:
- Passenger Name: {name}
- From: {from_city}
- To: {to_city}
- Date: {date}
- Bus Type: {bus_type}
- Number of Seats: {seats}
- Phone: {phone}

Your booking has been confirmed. You will receive further details soon.

Safe travels!
YatraSetu Team
'''
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            # Log the error or handle it as needed
            print(f"Email sending failed: {e}")

        return redirect('routes')

    return render(request, 'booking.html')

def submit_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('perent')
    else:
        form = FeedbackForm()

    return render(request, 'perent.html', {
        'form': form,
        'feed_posts': list(Post.objects.all().order_by('-id')[:6]) + list(Feedback.objects.all().order_by('-created_at')[:6]),
        'data': route.objects.all(),
        'query': None,
        'page_obj': Paginator(Gride.objects.all(), 6).get_page(1),
        'show_feedback_form': True,
    })