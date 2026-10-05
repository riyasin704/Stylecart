from django.shortcuts import render, redirect

from products.models import (
    Product,
    Category,
    Order,
    AdminAccount,
    Customer
)


def admin_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        admin = AdminAccount.objects.filter(email=email).first()

        if admin and admin.check_password(password):

            request.session["admin_id"] = admin.id

            return redirect("admin_dashboard")

        return render(
            request,
            "adminpanel/login.html",
            {
                "error": "Invalid email or password"
            }
        )

    return render(
        request,
        "adminpanel/login.html"
    )


def admin_dashboard(request):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_orders = Order.objects.count()
    total_customers = Customer.objects.count()

    return render(
        request,
        "adminpanel/dashboard.html",
        {
            "total_products": total_products,
            "total_categories": total_categories,
            "total_orders": total_orders,
            "total_customers": total_customers
        }
    )


def admin_logout(request):

    request.session.pop("admin_id", None)

    return redirect("admin_login")


def orders(request):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    all_orders = Order.objects.all().order_by("-created_at")

    return render(
        request,
        "adminpanel/orders.html",
        {
            "orders": all_orders
        }
    )


def update_order_status(request, order_id):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    if request.method == "POST":

        order = Order.objects.get(id=order_id)

        new_status = request.POST.get("status")

        valid_statuses = [
            choice[0]
            for choice in Order.STATUS_CHOICES
        ]

        if new_status in valid_statuses:

            order.status = new_status
            order.save()

    return redirect("orders")


def products(request):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    all_products = Product.objects.all()

    categories = Category.objects.all()

    edit_id = request.GET.get("edit")

    edit_product = None

    if edit_id:

        edit_product = Product.objects.get(
            id=edit_id
        )

    return render(
        request,
        "adminpanel/products.html",
        {
            "products": all_products,
            "categories": categories,
            "edit_product": edit_product
        }
    )


def edit_product(request, product_id):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    product = Product.objects.get(
        id=product_id
    )

    if request.method == "POST":

        product.category_id = request.POST.get(
            "category"
        )

        product.name = request.POST.get(
            "name"
        )

        product.description = request.POST.get(
            "description"
        )

        product.price = request.POST.get(
            "price"
        )

        if request.FILES.get("image"):

            product.image = request.FILES.get(
                "image"
            )

        product.available = (
            request.POST.get("available") == "on"
        )

        product.save()

        return redirect("products")

    return redirect(
        "/stylecart-admin/products/?edit="
        + str(product_id)
    )


def delete_product(request, product_id):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    product = Product.objects.get(
        id=product_id
    )

    product.available = False

    product.save()

    return redirect("products")


def add_product(request):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    categories = Category.objects.all()

    if request.method == "POST":

        category_id = request.POST.get(
            "category"
        )

        name = request.POST.get(
            "name"
        )

        description = request.POST.get(
            "description"
        )

        price = request.POST.get(
            "price"
        )

        image = request.FILES.get(
            "image"
        )

        Product.objects.create(
            category_id=category_id,
            name=name,
            description=description,
            price=price,
            image=image
        )

        return redirect("products")

    return render(
        request,
        "adminpanel/add_product.html",
        {
            "categories": categories
        }
    )


def add_category(request):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    if request.method == "POST":

        name = request.POST.get(
            "name"
        )

        description = request.POST.get(
            "description"
        )

        Category.objects.create(
            name=name,
            description=description
        )

        return redirect("categories")

    return render(
        request,
        "adminpanel/add_category.html"
    )


def categories(request):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    all_categories = Category.objects.all()

    edit_id = request.GET.get("edit")

    edit_category = None

    if edit_id:

        edit_category = Category.objects.get(
            id=edit_id
        )

    return render(
        request,
        "adminpanel/categories.html",
        {
            "categories": all_categories,
            "edit_category": edit_category
        }
    )


def edit_category(request, category_id):

    if not request.session.get("admin_id"):
        return redirect("admin_login")

    category = Category.objects.get(
        id=category_id
    )

    if request.method == "POST":

        category.name = request.POST.get(
            "name"
        )

        category.description = request.POST.get(
            "description"
        )

        category.save()

        return redirect("categories")

    return redirect(
        "/stylecart-admin/categories/?edit="
        + str(category_id)
    )