from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Post,Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.
def home(request):
	context={
	'posts':Post.objects.all()
	}
	return render(request,'blog/home.html',context)

class PostComment(CreateView):
	model = Comment
	fields=['text']
	template_name = "blog/post_comment.html"

	def form_valid(self,form):
		form.instance.author=self.request.user
		form.instance.post=get_object_or_404(Post,pk=self.kwargs.get('pk'))		
		return super().form_valid(form)


class PostListView(ListView):
	model=Post
	template_name='blog/home.html'
	context_object_name='posts'
	ordering=['-date_posted']
	#class based views

class UserPostListView(ListView):
	model=Post
	template_name='blog/user_post.html'
	context_object_name='posts'

	def get_queryset(self):
		user=get_object_or_404(User,username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
	model=Post

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model=Post
	success_url='/'
	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False



# LoginRequiredMixin: To make sure user is logged in before creating any post so this will redirect to the login page
class PostCreateView(LoginRequiredMixin, CreateView):
	model=Post
	fields=['title','content']
	
	def form_valid(self,form):
		form.instance.author=self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model=Post
	fields=['title','content']
	
	def form_valid(self,form):
		form.instance.author=self.request.user
		return super().form_valid(form)

	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False

def about(request):
	return render(request,'blog/about.html',{'title':'About'})