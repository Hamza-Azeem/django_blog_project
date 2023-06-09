from django.shortcuts import render
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404

# Create your views here.

def home(request):
    contex = {
        "posts": Post.objects.all()
    }
    return render(request, "blog/home.html", contex)

class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ['-date']
    paginate_by = 2

class UserPostListView(PostListView):
    model = Post
    fields = ['title', 'content']
    context_object_name = 'posts'
    paginate_by = 2
    def get_queryset(self):
        user = get_object_or_404(User, username= self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False



def about(request):
    return render(request, "blog/about.html", {"title": "About"})

