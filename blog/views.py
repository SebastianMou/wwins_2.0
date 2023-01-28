from django.shortcuts import render, redirect
from .models import PostModel, ProfileModel, GoalsModel, Category, Follower
from django.contrib.auth.models import User
from .forms import (UserRegisterForm, PostForm, UserUpdateForm, 
ProfileUpdateForm, GoalsForm, GoalUpdateForm, PostUpdateForm, CommentForm, CategoryForm)
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.db.models import Count
from django.urls import reverse_lazy

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

def search_pc(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        posts = PostModel.objects.filter(title__contains=searched)
        categories = Category.objects.filter(name__contains=searched)
        users_prof = ProfileModel.objects.filter(user__username__icontains=searched).annotate(post_count=Count('user__posts'))
        goals = GoalsModel.objects.filter(goal__icontains=searched)

        context = {
            'searched': searched,
            'posts': posts,
            'categories': categories,
            'users_prof': users_prof,
            'goals': goals,
        }
        return render(request, 'blog/search_pc.html', context)
    else:
        return render(request, 'blog/search_pc.html')

def home(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_post_count = PostModel.objects.filter(user=current_user).count()
    else:
        user_post_count = None
        posts = PostModel.objects.all()

    posts = PostModel.objects.all()
    context = {
        'posts': posts,
        'user_post_count': user_post_count,
    }
    return render(request, 'blog/home.html', context)

def categories(request):
    categories = Category.objects.all()[:10]

    return {
        'categories': categories,
    }

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect(category)
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
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    context = {
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
        messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
            received activation link to confirm and complete the registration. Note: Check your spam folder.')
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
    user_post_count = PostModel.objects.filter(user=user).count()

    goals = GoalsModel.objects.filter(user=user)
    count = goals.filter(complete=False).count()

    is_following = False
    if request.user.is_authenticated:
        is_following = request.user.follower.filter(following=user).exists()

    posts = PostModel.objects.filter(user=user)
    context = {
        'user': user, 
        'posts': posts,
        'is_following': is_following,
        'user_post_count': user_post_count,
        'goals': goals,
        'count': count,
    }
    return render(request, 'blog/users/user_profile.html', context)

def all_goals(request):
    goals = GoalsModel.objects.all()
    context = {
        'goals': goals,
    }
    return render(request, 'blog/all_goals.html', context)

def create_a_goal(request):
    if request.method == 'POST':
        form_goal = GoalsForm(request.POST)
        if form_goal.is_valid():
            goal = form_goal.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect(reverse_lazy('home'))
    else:
        form_goal = GoalsForm()
    context = {
        'form_goal': form_goal,
    }
 
    return render(request, 'blog/create_user_goals.html', context)

def goal_detail(request, pk):
    goal = GoalsModel.objects.get(id=pk)
    context = {
        'goal': goal,
    }
    return render(request, 'blog/goal_detail.html', context)

@login_required
def goal_delete(request, goal_id=None):
    goals_post = GoalsModel.objects.get(id=goal_id)
    goals_post.delete()
    return redirect('/')

@login_required
def goal_edit(request, pk):
    post = GoalsModel.objects.get(id=pk)
    if request.method == 'POST':
        form = GoalUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('goal_detail', pk=post.id)
    else:
        form = GoalUpdateForm(instance=post)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/goal_edit.html', context)

@login_required
def profile(request, username):
    posts = PostModel.objects.all()
    posts = posts.filter(user=request.user)

    user = request.user
    user_post_count = PostModel.objects.filter(user=user).count()

    goals = GoalsModel.objects.filter(user=request.user)
    count = goals.filter(complete=False).count()

    if request.method == 'POST':
        user = request.user
        u_form = UserUpdateForm(request.POST or None, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profilemodel)
        if u_form.is_valid() and p_form.is_valid():
            user_form = u_form.save()
            p_form.save()
            messages.success(request, f'{user_form.username}, Your profile has been updated!')
            return redirect('profile', user_form.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profilemodel)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
        'user_post_count': user_post_count,
        'goals': goals,
        'count': count,
    }

    user = get_user_model().objects.filter(username=username).first()
    if user:
        u_form = UserUpdateForm(instance=user)
        return render(request, 'blog/profile.html', context)

    return render(request, 'blog/profile.html', context)

def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    follow = Follower(follower=request.user, following=user_to_follow)
    follow.save()
    return redirect('user_profile', user_id=user_to_follow.id)

def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    follow = get_object_or_404(Follower, follower=request.user, following=user_to_unfollow)
    follow.delete()
    return redirect('user_profile', user_id=user_to_unfollow.id)

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

def complaint(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')
        name = request.POST.get('name')
        data = {
            'complaint': 'complaint form WWINS',
            'name': name,
            'email': email,
            'message': message, 
        }
        message = '''
        From: {}
        Email: {}

        New message: {}
        '''.format(data['name'], data['email'], data['message'])
        send_mail(data['complaint'], message, '', ['ensocio.mx@gmail.com'])
        return render(request, 'blog/email_sent.html')

    return render(request, 'blog/complaint.html')