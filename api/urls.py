from django.urls import path

from api.views import get_user_by_id, register_user, search_users

urlpatterns = [
    path('registration', register_user),
    path('user/<int:user_id>', get_user_by_id),
    path('user/search', search_users)
]
