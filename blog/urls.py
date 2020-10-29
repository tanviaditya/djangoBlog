from django.urls import path
from . import views
from .views import PostListView,UserPostListView,PostComment,DeleteComment,ViewConnections
from .views import PostDetailView
from .views import PostCreateView
from .views import PostUpdateView
from .views import PostDeleteView,PostReport

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('connections/', ViewConnections.as_view(), name='connections'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),   
    path('post/<int:pk>/comment', PostComment.as_view(), name='add-comment'),
    path('post/<int:pk>/report', PostReport.as_view(), name='add-report'),
    path('post/<int:pk>/comment/delete/', DeleteComment.as_view(), name='comment-delete'),   
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),   
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),   
	path('post/new/', PostCreateView.as_view(), name='post-create'),   
    path('post/<str:username>/', UserPostListView.as_view(), name='user-posts'),   
    path('about/', views.about, name='blog-about'),
    path('send_request/<str:username>',views.send_request ,name='send_request')

]



# <app>/<model>_<viewtype>.html  looking for this template