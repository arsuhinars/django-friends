from django.urls import path

from api.views import (
    FriendView,
    accept_invite,
    decline_invite,
    get_friends,
    get_incoming_invites,
    get_outcoming_invites,
    get_user_by_id,
    invite_friend,
    register_user,
    search_users,
)

urlpatterns = [
    path('registration', register_user),
    path('user/<int:user_id>', get_user_by_id),
    path('users/search', search_users),
    path('friend/<int:user_id>', FriendView.as_view()),
    path('friend/<int:user_id>/invite', invite_friend),
    path('friend/<int:user_id>/accept', accept_invite),
    path('friend/<int:user_id>/decline', decline_invite),
    path('friends', get_friends),
    path('friends/incoming', get_incoming_invites),
    path('friends/outcoming', get_outcoming_invites),
]
