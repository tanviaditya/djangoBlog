from django.urls import path
from . import views
from .views import PostListView
from .views import PostDetailView
from .views import PostCreateView
from .views import PostUpdateView
from .views import PostDeleteView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),   
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),   
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),   
	path('post/new/', PostCreateView.as_view(), name='post-create'),   
    path('about/', views.about, name='blog-about'),

]



# <app>/<model>_<viewtype>.html  looking for this template