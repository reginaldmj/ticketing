from django.contrib import admin
from django.urls import path
from tickets import views


urlpatterns = [
    # Auth
    path('login/',  views.login_view,  name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Tickets
    path('admin/', admin.site.urls),
    path('',                          views.home,           name='home'),
    path('ticket/<int:pk>/',          views.ticket_detail,  name='ticket_detail'),
    path('ticket/new/',               views.ticket_create,  name='ticket_create'),
    path('ticket/<int:pk>/edit/',     views.ticket_edit,    name='ticket_edit'),
    path('ticket/<int:pk>/delete/',   views.ticket_delete,  name='ticket_delete'),
    path('signup/', views.signup, name='signup'),

    # Users
    path('user/<int:pk>/',            views.user_profile,   name='user_profile'),
]
