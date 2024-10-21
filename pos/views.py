from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import Product, Customer
from .forms import ProductForm, PaymentForm, CustomerForm, IndividualProductForm, ProductFormSet
from django.forms import formset_factory
from django_daraja.mpesa.core import MpesaClient
from django.contrib import messages


def product_list(request):
    products = Product.objects.all()
    total_quantity = sum(product.quantity for product in products)
    total_amount = sum(product.quantity * product.price for product in products)

    products_with_total = [
        {'product': product, 'total_amount': product.quantity * product.price}
        for product in products
    ]

    return render(request, 'pos/product_list.html', {
        'products': products_with_total,
        'total_quantity': total_quantity,
        'total_amount': total_amount,
    })

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('pos:product_list')
    else:
        form = ProductForm()
    return render(request, 'pos/add_product.html', {'form': form})

def process_payment(request):
    IndividualProductFormSet = formset_factory(IndividualProductForm, extra=1)

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        formset = IndividualProductFormSet(request.POST)

        if payment_form.is_valid() and formset.is_valid():
            total_amount = 0
            products_purchased = []
            insufficient_stock = {}

            for form in formset:
                product = form.cleaned_data['product']
                quantity = form.cleaned_data['quantity']
                total_price = product.price * quantity

                if product.quantity < quantity:
                    insufficient_stock[product.name] = {
                        'requested_quantity': quantity,
                        'available_stock': product.quantity,
                    }
                    continue  # Skip processing this product

                total_amount += total_price
                products_purchased.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': total_price,
                })

                product.quantity -= quantity
                product.save()

            if insufficient_stock:
                error_message = "The following products have insufficient stock:<br>"
                for product_name, details in insufficient_stock.items():
                    error_message += f"{product_name}: Requested {details['requested_quantity']}, Available {details['available_stock']}<br>"
                return HttpResponseBadRequest(f"{error_message}<br><a href='{reverse('pos:process_payment')}'>Return to Payment</a>")

            payment_method = payment_form.cleaned_data['payment_method']

            if payment_method == 'mpesa':
                phone_number = request.POST.get('phone_number')
                if phone_number:
                    amount = int(total_amount)  # Ensure the amount is an integer
                    cl = MpesaClient()  # Initialize your Mpesa client here
                    account_reference = 'Jogoo Oeri'
                    transaction_desc = 'Payments'
                    callback_url = 'https://example.com/callback/'  # Replace with your callback URL
                    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
                    return HttpResponse(response)
                else:
                    return HttpResponseBadRequest("Phone number is required for Mpesa payments")

            return render(request, 'pos/payment_success.html', {
                'total_amount': total_amount,
                'products_purchased': products_purchased,
                'payment_method': payment_method,
                'return_url': reverse('pos:process_payment'),  # Generate URL to return to process_payment view
            })

    else:
        payment_form = PaymentForm()
        formset = IndividualProductFormSet()

    return render(request, 'pos/process_payment.html', {
        'payment_form': payment_form,
        'formset': formset,
    })

def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pos:product_list')
    else:
        form = CustomerForm()
    return render(request, 'pos/add_customer.html', {'form': form})

def payment_success(request):
    return render(request, 'pos/payment_success.html')


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('pos:product_list'))  # Use the correct namespace
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'pos/update_product.html', {'form': form, 'product': product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect('pos:product_list')  # Replace with the name of your product list URL
    
    return render(request, 'pos/delete_product.html', {'product': product})


def check_product_name(request):
    name = request.GET.get('name', None)
    data = {
        'exists': Product.objects.filter(name=name).exists()
    }
    return JsonResponse(data)



def check_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = {
        'stock': product.quantity
    }
    return JsonResponse(data)


def customer_records(request):
    customers = Customer.objects.all()

    return render(request, 'pos/customer_records.html', {
        'customers': customers,
    })


def stock_records(request):
    products = Product.objects.all()

    return render(request, 'pos/stock_records.html', {
        'products': products,
    })