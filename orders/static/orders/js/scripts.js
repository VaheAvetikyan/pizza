
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.add-item').forEach(function (button) {
        button.onclick = () => {

            // Initialize new request
            const request = new XMLHttpRequest();
            const item = button.dataset.item
            const size = button.dataset.size

            if (button.dataset.pizza != null) {
                var pizza = button.dataset.pizza
            }

            request.open('POST', 'additem/');

            // Callback function for when request completes
            request.onload = () => {

                // Extract JSON data from request
                const data = JSON.parse(request.responseText);

                // Show current shopping cart count
                document.querySelector('#cart-count').dataset.count = data.items

                if (pizza === "Regular - small" || pizza === "Sicilian - small") {
                    document.querySelectorAll('.topping-on-small').forEach(el => {
                        el.style.visibility = 'visible';
                    })
                }
                else if (pizza === "Regular - large" || pizza === "Sicilian - large") {
                    document.querySelectorAll('.topping-on-large').forEach(el => {
                        el.style.visibility = 'visible';
                    })
                }
            }

            // Add data to send with request
            const data = new FormData();
            data.append('item', item);
            data.append('size', size);

            // Set request header
            request.setRequestHeader("X-CSRFToken", csrftoken);

            // Send request
            request.send(data);
            return false;
        }
    });
});


addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.remove-item').forEach(function (button) {
        button.onclick = () => {

            // Initialize new request
            const request = new XMLHttpRequest();
            const cart_id = button.dataset.item
            request.open('POST', 'removeitem/');

            // Callback function for when request completes
            request.onload = () => {

                // Extract JSON data from request
                const response = JSON.parse(request.responseText);

                // Set current shopping cart count
                document.querySelector('#cart-count').dataset.count = response.items
                document.querySelector('#cart-count-total').textContent = response.items

                if (response.items === 0) {
                    document.querySelector('#proceed-to-order').style.visibility = 'hidden';
                }

                //Set current total
                document.querySelector('#cart-subtotal').textContent = response.total

                // Remove selected object from cart
                document.querySelector(`#_${cart_id}`).innerHTML = '';
            }

            // Add data to send with request
            const data = new FormData();
            data.append('cart_id', cart_id);

            // Set request header
            request.setRequestHeader("X-CSRFToken", csrftoken);

            // Send request
            request.send(data);
            return false;
        }
    });
});


var elem = document.querySelectorAll('.tabs')
var instance = M.Sidenav.getInstance(elem);

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {});
});

