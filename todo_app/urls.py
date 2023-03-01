# todo_list/todo_app/urls.py
from django.urls import path
from todo_app import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.categoryListView.as_view(), name="index"),
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('signin/', views.UserLoginView.as_view(next_page='index') , name='signin'),
    path('logout/', LogoutView.as_view(next_page='signin'), name='logout'),
    path("category/<int:list_id>/", views.categoryItemListView.as_view(), name="list"),
    path("category/add/", views.categoryListCreate.as_view(), name="list-add"),
    path("category/<int:pk>/delete/", views.categoryListDelete.as_view(), name="list-delete"),
    path("category/<int:list_id>/item/add/",views.categoryItemCreate.as_view(),name="item-add"),
    path("category/<int:list_id>/item/<int:pk>/",views.categoryItemUpdate.as_view(),name="item-update"),
    path("category/<int:list_id>/item/<int:pk>/delete/",views.categoryItemDelete.as_view(),name="item-delete"),
]
