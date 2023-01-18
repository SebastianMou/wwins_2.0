from django.shortcuts import render, redirect
from .models import PostModel, Category
from django.contrib.auth.models import User
from .forms import UserRegisterForm, PostForm, UserUpdateForm, ProfileUpdateForm, PostUpdateForm, CommentForm, CategoryForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

from .tokens import account_activation_token

# Create your views here.
def home_info(request):
    return render(request, 'blog/home_info.html')

def home(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')
        data = {
            'complaint': 'complaint form WWINS',
            'email': email,
            'message': message, 
        }
        message = '''
        Form: {}

        New message: {}
        '''.format(data['email'], data['message'])
        send_mail(data['complaint'], message, '', ['ensocio.mx@gmail.com'])
        return render(request, 'blog/email_sent.html')

    posts = PostModel.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'blog/home.html', context)

def categories(request):
    return {
        'categories': Category.objects.all()
    }

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_category')
    else:
        form = CategoryForm()
    return render(request, 'blog/create_category.html', {'form': form})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = PostModel.objects.filter(category=category)
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'there was a error')
            return redirect('login')
    return render(request, 'blog/users/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'you where loged out')
    return redirect('home')

@login_required
def create_post(request):
    posts = PostModel.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # get the category instance
            category_name = form.cleaned_data['category']
            category = Category.objects.get(name=category_name)
            # assign the category instance to the post
            post = form.save(commit=False)
            post.category = category
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'blog/create_post.html', context)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('/')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('blog/users/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'blog/users/register.html', context)

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = PostModel.objects.filter(user=user)
    context = {
        'user': user, 
        'posts': posts
    }
    return render(request, 'blog/users/user_profile.html', context)

@login_required
def profile(request, username):
    # posts = request.user.PostModel.all()
    posts = PostModel.objects.all()
    posts = posts.filter(user=request.user)

    if request.method == 'POST':
        user = request.user
        u_form = UserUpdateForm(request.POST or None, instance=user)
        # p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profilemodel)
        if u_form.is_valid():
            user_form = u_form.save()
            messages.success(request, f'{user_form.username}, Your profile has been updated!')
            return redirect('profile', user_form.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        # p_form = ProfileUpdateForm(instance=request.user.profilemodel)

    context = {
        'u_form': u_form,
        # 'p_form': p_form,
        'posts': posts,
    }

    user = get_user_model().objects.filter(username=username).first()
    if user:
        u_form = UserUpdateForm(instance=user)
        return render(request, 'blog/profile.html', context)

    return render(request, 'blog/profile.html', context)

def like_post(request, pk):
    post = get_object_or_404(PostModel, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[pk]))

def post_detail(request, pk):
    likes_connected = get_object_or_404(PostModel, id=pk)

    liked = False
    if likes_connected.likes.filter(id=pk).exists():
        liked = True

    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            return redirect('post_detail', pk=post.id)
    else:
        c_form = CommentForm()

    context = {
        'post': post,
        'c_form': c_form,
        'total_likes': likes_connected.total_likes(),
        'post_is_liked': liked,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_edit(request, pk):
    post = PostModel.objects.get(id=pk)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = PostUpdateForm(instance=post)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/post_edit.html', context)

@login_required
def delete(request, post_id=None):
    post = PostModel.objects.get(id=post_id)
    post.delete()
    return redirect('/')

def community_guidelines(request):
    return render(request, 'blog/community_guidelines.html')

