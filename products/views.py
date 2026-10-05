from django.shortcuts import render, redirect
from .models import Product, Category, Order, Customer, OrderItem

def product_list(request):
    products = Product.objects.filter(available=True)

    return render(
        request,
        "products/product_list.html",
        {"products": products}
    )


def home(request):
    return render(request, "products/home.html")

def register(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")

        if Customer.objects.filter(email=email).exists():
            return render(
                request,
                "products/register.html",
                {"error": "Email already registered"}
            )

        Customer.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode
        )

        return redirect("login")

    return render(
        request,
        "products/register.html"
    )

def customer_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        customer = Customer.objects.filter(email=email).first()

        if customer and customer.check_password(password):

            request.session["customer_id"] = customer.id

            return redirect("home")

        return render(
            request,
            "products/login.html",
            {"error": "Invalid email or password"}
        )

    return render(
        request,
        "products/login.html"
    )

def customer_logout(request):

    request.session.flush()

    return redirect("home")


def category_list(request):
    categories = Category.objects.all()

    return render(
        request,
        "products/category_list.html",
        {"categories": categories}
    )


def category_products(request, category_id):
    products = Product.objects.filter(
        category_id=category_id,
        available=True
    )

    return render(
        request,
        "products/product_list.html",
        {"products": products}
    )


def product_detail(request, product_id):

    product = Product.objects.get(id=product_id)

    if request.method == "POST":

        cart = request.session.get("cart", {})

        product_id = str(product.id)

        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1

        request.session["cart"] = cart

        return redirect("cart")

    return render(
        request,
        "products/product_detail.html",
        {"product": product}
    )

def cart(request):
    cart = request.session.get("cart", {})

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        action = request.POST.get("action")

        if product_id in cart:

            if action == "increase":
                cart[product_id] += 1

            elif action == "decrease":
                cart[product_id] -= 1

                if cart[product_id] <= 0:
                    del cart[product_id]

            elif action == "remove":
                del cart[product_id]

        request.session["cart"] = cart

        return redirect("cart")

    products = []
    total_amount = 0

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        item_total = product.price * quantity
        total_amount += item_total

        products.append({
            "product": product,
            "quantity": quantity,
            "item_total": item_total
        })

    return render(
        request,
        "products/cart.html",
        {
            "products": products,
            "total_amount": total_amount
        }
    )

def checkout(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    customer = Customer.objects.get(id=customer_id)

    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart")

    if request.method == "POST":

        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        total_amount = 0

        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            total_amount += product.price * quantity

        order = Order.objects.create(
            user=customer,
            name=name,
            address=address,
            phone=phone,
            total_amount=total_amount
        )

        for product_id, quantity in cart.items():

            product = Product.objects.get(id=product_id)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        request.session["cart"] = {}

        return redirect("order_success", order_id=order.id)

    return render(
        request,
        "products/checkout.html"
    )


def order_success(request, order_id):
    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    order = Order.objects.get(
        id=order_id,
        user_id=customer_id
    )

    return render(
        request,
        "products/order_success.html",
        {"order": order}
    )

def my_orders(request):
    customer_id = request.session.get("customer_id")

    # Login nahi hai to Login page par bhejo
    if not customer_id:
        return redirect("login")

    orders = Order.objects.filter(
        user_id=customer_id
    ).order_by("-created_at")

    return render(
        request,
        "products/my_orders.html",
        {"orders": orders}
    )