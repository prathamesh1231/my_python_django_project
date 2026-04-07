from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MenuItem, ContactMessage, Cart, CartItem, Order, OrderItem

# ─── Static data ────────────────────────────────────────────────────────────

MENU_ITEMS_DATA = [
    {'name': 'Cheese Pizza',  'price': 299, 'image': 'food/images/pizza.jpg',      'emoji': '🍕', 'category': 'pizza'},
    {'name': 'Veg Burger',    'price': 149, 'image': 'food/images/burger.jpg',     'emoji': '🍔', 'category': 'burger'},
    {'name': 'Sandwich',      'price': 60,  'image': 'food/images/sandwhich.webp', 'emoji': '🥪', 'category': 'snack'},
    {'name': 'French Fries',  'price': 30,  'image': 'food/images/french.jpg',     'emoji': '🍟', 'category': 'snack'},
]

TEAM = [
    {'name': 'Divya Gunjal',  'role': 'Founder & Head Chef',  'image': 'food/images/divya_gunjal.jpeg',  'bio': 'The visionary behind the food-court. Divya brings passion, creativity, and secret family recipes to every dish.'},
    {'name': 'Kiran Badhe',   'role': 'Kitchen Manager',      'image': 'food/images/kiran_badhe.jpeg',   'bio': 'Kiran keeps the kitchen running like clockwork, ensuring every order is fresh, hot, and perfect.'},
    {'name': 'Athrav Jadhav', 'role': 'Customer Experience',  'image': 'food/images/athrav_jadhav.jpeg', 'bio': 'Athrav makes sure every guest leaves with a full stomach and a big smile. He knows every regular by name!'},
]

TIMELINE = [
    {'year': 2020, 'title': 'The First Stall 🛒',     'desc': 'A small food stall near the HP Petrol Pump with just three items and big dreams.'},
    {'year': 2021, 'title': 'The Crowd Grows 🎉',     'desc': 'Word spreads fast. French fries and special sauces added by popular demand.'},
    {'year': 2022, 'title': 'Permanent Home 🏠',      'desc': 'A proper seating space — welcoming families and friend groups to dine in comfort.'},
    {'year': 2023, 'title': 'Community Favourite ⭐', 'desc': 'The go-to landmark in Alephata for celebrations and after-school hangouts.'},
    {'year': 2026, 'title': 'Going Digital 💻',       'desc': 'Django-powered website launched to connect with customers online.'},
]

# ─── Helper ──────────────────────────────────────────────────────────────────

def _cart_count(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart.item_count()
    return 0

# ─── Public pages ────────────────────────────────────────────────────────────

def home(request):
    return render(request, 'food/home.html', {
        'featured': MENU_ITEMS_DATA[:3],
        'cart_count': _cart_count(request),
    })

def about(request):
    return render(request, 'food/about.html', {
        'team': TEAM, 'timeline': TIMELINE,
        'menu_items': MENU_ITEMS_DATA,
        'cart_count': _cart_count(request),
    })

def menu_view(request):
    return render(request, 'food/menu.html', {
        'menu_items': MENU_ITEMS_DATA,
        'cart_count': _cart_count(request),
    })

def contact(request):
    from .forms import ContactForm
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                message=form.cleaned_data['message'],
            )
            messages.success(request, '✅ Thank you! Your message has been sent.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'food/contact.html', {
        'form': form,
        'cart_count': _cart_count(request),
    })

def map_view(request):
    return render(request, 'food/map.html', {'cart_count': _cart_count(request)})

# ─── Auth ────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}! 👋')
            return redirect(request.POST.get('next', 'home'))
        messages.error(request, 'Invalid username or password.')
    return render(request, 'food/login.html', {'next': request.GET.get('next', '')})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        name      = request.POST.get('name', '').strip()
        if not all([username, email, password1, password2]):
            messages.error(request, 'Please fill in all required fields.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password1) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            name_parts = name.split()
            first = name_parts[0] if name_parts else ''
            last = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            user = User.objects.create_user(username=username, email=email, password=password1,
                                            first_name=first, last_name=last)
            login(request, user)
            messages.success(request, f'Account created! Welcome, {user.username} 🎉')
            return redirect('home')
    return render(request, 'food/register.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('home')

# ─── Cart ────────────────────────────────────────────────────────────────────

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'food/cart.html', {
        'cart': cart,
        'cart_count': cart.item_count(),
    })

@login_required
def add_to_cart(request, item_id):
    # Find matching item from static data by index
    try:
        item_data = MENU_ITEMS_DATA[item_id]
    except IndexError:
        messages.error(request, 'Item not found.')
        return redirect('menu')

    # Get or create a DB MenuItem
    menu_item, _ = MenuItem.objects.get_or_create(
        name=item_data['name'],
        defaults={
            'price': item_data['price'],
            'image': item_data['image'],
            'emoji': item_data['emoji'],
            'category': item_data['category'],
        }
    )
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'{menu_item.emoji} {menu_item.name} added to cart!')
    return redirect('menu')

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.info(request, 'Item removed from cart.')
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    try:
        qty = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        qty = 1
    if qty < 1:
        cart_item.delete()
    else:
        cart_item.quantity = qty
        cart_item.save()
    return redirect('cart')

# ─── Checkout & Orders ───────────────────────────────────────────────────────

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('menu')

    if request.method == 'POST':
        address = request.POST.get('address', '').strip()
        phone   = request.POST.get('phone', '').strip()
        if not address or not phone:
            messages.error(request, 'Please provide your address and phone number.')
        else:
            order = Order.objects.create(
                user=request.user,
                status='pending',
                total=cart.total(),
                address=address,
                phone=phone,
            )
            for ci in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    menu_item=ci.menu_item,
                    quantity=ci.quantity,
                    price=ci.menu_item.price,
                )
            cart.items.all().delete()
            messages.success(request, f'🎉 Order #{order.id} placed successfully!')
            return redirect('order_detail', order_id=order.id)

    return render(request, 'food/checkout.html', {
        'cart': cart,
        'cart_count': cart.item_count(),
    })

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'food/orders.html', {
        'orders': orders,
        'cart_count': _cart_count(request),
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'food/order_detail.html', {
        'order': order,
        'cart_count': _cart_count(request),
    })
