from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostAdd, PostUpdateView, PostDeleteView, add_subscribe, del_subscribe
from . import views

urlpatterns = [
        path('', PostList.as_view()),
        path('<int:pk>', PostDetail.as_view(), name='post_detail'),
        path('search', PostSearch.as_view()),
        path('add', PostAdd.as_view(), name='post_create'),
        path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
        path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
        path('<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
        path('<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
        path('news/', views.news_list, name='news_list'),
        path('news/<int:pk>/', views.news_detail, name='news_detail'),
        path('news/', views.news_list, name='news_list'),
        path('news/search/', views.news_search, name='news_search'),
        path('news/create/', views.news_create, name='news_create'),
        path('news/<int:pk>/edit/', views.news_edit, name='news_edit'),
        path('news/<int:pk>/delete/', views.news_delete, name='news_delete'),
        ]


