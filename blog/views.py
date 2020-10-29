from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.http import JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Post,Comment,Report
from users.models import Connection 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.
def home(request):
	context={
	'posts':Post.objects.all(),
	'connections':Connection.object.all()
	}
	return render(request,'blog/home.html',context)

def send_request(request,username=None):
	if username is not None:
		friend_user=User.objects.get(username=username)
		friend=Connection.objects.create(follower=request.user,following=friend_user)
		data={
			'status':True,
			'message':"Request Sent"
		}
		return redirect("/")

class PostComment(LoginRequiredMixin,CreateView):
	model = Comment
	fields=['text']
	template_name = "blog/post_comment.html"

	def form_valid(self,form):
		form.instance.author=self.request.user
		form.instance.post=get_object_or_404(Post,pk=self.kwargs.get('pk'))		
		return super().form_valid(form)

class PostReport(LoginRequiredMixin,CreateView):
	model = Report
	fields=['reason']
	template_name = "blog/post_report.html"

	def form_valid(self,form):
		form.instance.author=self.request.user
		form.instance.post=get_object_or_404(Post,pk=self.kwargs.get('pk'))		
		return super().form_valid(form)


class DeleteComment(DeleteView):
	model = Comment
	def test_func(self):
		comment=self.get_object()
		if self.request.user==comment.author:
			return True
	def get_success_url(self):
		post = Post.objects.get(pk=self.object.post.pk)
		return post.get_absolute_url()
	

class PostListView(ListView):
	model=Post
	template_name='blog/home.html'
	context_object_name='posts'
	ordering=['-date_posted']
	#class based views

class ViewConnections(ListView):
	model=Connection
	context_object_name='connections'

	def get_queryset(self):
		user=get_object_or_404(User,username=self.request.user.username)
		return Connection.objects.filter(follower=user)
	
	

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