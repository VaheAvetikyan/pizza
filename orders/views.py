from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.core.mail import send_mail

from .models import Menu, Cart, Order
from .forms import SignUpForm

# Create your views here.


def index(request):

    # Get the current user
    user = request.user

    # If user is authenticated, set the count of shopping cart items
    if user.is_authenticated:
        cart_items = Cart.objects.filter(user_id=user.id).count()
    else:
        cart_items = 0

    # Get all menu items from database
    menu = Menu.objects.all()

    context = {
        "cart_count": cart_items,

        "pizza": menu.filter(type="Pizza"),
        "toppings": menu.filter(type="Toppings"),
        "subs": menu.filter(type="Subs"),
        "subsadd": menu.filter(type="Subs addons"),
        "pasta": menu.filter(type="Pasta"),
        "salads": menu.filter(type="Salads"),
        "platters": menu.filter(type="Dinner Platters"),
    }
    return render(request, "orders/index.html", context)


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created: {username}")
            login(request, user)

            try:
                # Send an email
                send_mail(
                        'Welcome to my Pizza store demo website',
                        f'Hi {user.username}! Your account is created successfully․ \n\n Note: This website is for demonstration purposes only.',
                        'pizza.demo.website@gmail.com',
                        [user.email],
                        fail_silently=False,    
                )
            except:
                messages.error(request, "Confirmation email not sent.")

            return redirect("/")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request=request,
                          template_name="registration/register.html",
                          context={"form": form})

    form = SignUpForm
    context = {"form": form}
    return render(request, "registration/register.html", context)


def additem(request):

    # Get the selected item from menu
    item = request.POST.get("item")
    size = request.POST.get("size")

    # Get user id
    user_id = request.user.id

    # Enter the selected item to shopping cart database
    new_item = Cart(item_id=item, user_id=user_id, size=size)
    new_item.save()

    # Get current count of shopping cart items
    items = Cart.objects.filter(user_id=user_id).count()

    return JsonResponse({"items": items})


def removeitem(request):

    # Get selected item id to remove
    cart_id = request.POST.get("cart_id")

    # Delete item from cart table in database
    Cart.objects.filter(id=cart_id).delete()

    # Get user id
    user_id = request.user.id

    # Get current count of shopping cart items
    cart_items = Cart.objects.filter(user_id=user_id)

    # Sum of the total in the shopping cart
    total = 0

    for object in cart_items:
        total += float(object.size)

    total = round(total, 2)

    # Return success
    return JsonResponse({"items": cart_items.count(), "total": total})


def cart(request):

    # Get user id
    user_id = request.user.id

    # Get items in the shopping cart
    cart_items = Cart.objects.filter(user_id=user_id)

    # Sum of the total in the shopping cart
    total = 0

    for object in cart_items:
        total += float(object.size)

    total = round(total, 2)

    # Context to send to view
    context = {
        "cart": cart_items,
        "cart_count": cart_items.count(),
        "total": total
    }

    return render(request, "orders/cart.html", context)


def placeorder(request):

    # Get user id
    user = request.user
    user_id = user.id

    # Get items in the shopping cart
    cart_items = Cart.objects.filter(user_id=user_id)

    if request.method == "GET":
        # Sum of the total in the shopping cart
        total = 0

        for object in cart_items:
            total += float(object.size)

        total = round(total, 2)

        # Context to send to view
        context = {
            "cart": cart_items,
            "total": total
        }

        return render(request, "orders/placeorder.html", context)

    else:
        # Enter the order into database
        for object in cart_items:
            new_order = Order(user=user, item=object.item,
                              price=object.size, time=timezone.now())
            new_order.save()

        # Send an email
        try:
            message = f"Hi {user.username}! Your order is placed successfully."
            
            for object in cart_items:
                message += f"\n{object.item.name} ({object.item.type}): price - $ {object.size}"

            send_mail(
                'Your Pizza order is on it\'s way!',
                f'{message} \n\n Note: This is just for demonstration purposes, no real order is made',
                'pizza.demo.website@gmail.com',
                [user.email],
                fail_silently=False,
            )
        except:
            messages.error(request, "Confirmation email not sent.")

        # Remove ordered items from shopping cart
        cart_items.delete()

        # Flash the message for success
        messages.success(request, f"Your order has been placed")

        return redirect("/orders")


def orders(request):

    # Get user id
    user = request.user

    orders = Order.objects.filter(user_id=user.id).order_by("-time")

    context = {
        "orders": orders
    }

    return render(request, "orders/history.html", context)
