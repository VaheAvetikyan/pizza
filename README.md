# Project 3

Web application for handling a pizza restaurant’s online orders. 


Models:

models.py __ there are 3 models for Menu, Shopping Cart and Orders.
admin.py __ some modifications to admin default view.
forms.py __ contains a SignUpForm that inherits from Django's UserCreationForm and adds email field to user model.


Control:

views.py __ index 
                    function gets number of items in users cart, and renders all menu items,
            register 
                    function registers user and logs them in, also sending email about successfully creating an acount.
            additem 
                    function gets AJAX request, adds selected item to shopping cart database and returns JSON response about the current number of cart.
            removeitem 
                    function gets AJAX request, removes the item from shopping cart database.
            cart 
                    function renders all items in users shopping cart.
            placeorder
                    function gets current items from users shopping cart and adds them in orders database, also sending email about order.
            orders
                    function renders all items that user has ordered.


View:

templates __ base.html, cart.html (shopping cart items), history.html (ordered items), index.html (menu items), placeorder.html (for confirmation of the order)

static __   css/styles.css (a few modifications to materialize styles)
            js/scripts.js (handleing some AJAX requests and a few DOM manipulations)
            media/pizza-icon.png (favicon)
