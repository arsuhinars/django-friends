from rest_framework.exceptions import NotFound

from api.exceptions import AlreadyExistsException, InvalidFormatException
from api.models import UserEntity
from api.serializers import FriendshipStatus, UserCreateSerializer, UserSerializer


class UserService():
    def create(self, dto: UserCreateSerializer) -> UserSerializer:
        try:
            UserEntity.objects.get(name=dto.data['name'])
            raise AlreadyExistsException('User with given name already exists')
        except UserEntity.DoesNotExist:
            ...

        user = UserEntity.objects.create_user(
            dto.data['name'],
            dto.data['password']
        )
        return UserSerializer(user)

    def get_by_id(self, id: int) -> UserSerializer | None:
        try:
            user = UserEntity.objects.get(id=id)
            return UserSerializer(instance=user)
        except UserEntity.DoesNotExist:
            return None

    def search_by_name(self, name: str, limit: int) -> list[UserSerializer]:
        users = UserEntity.objects.filter(name__icontains=name)[:limit]
        return list(map(lambda u: UserSerializer(instance=u), users))


class FriendsService():
    def get_friends(self, user_id: int) -> list[UserSerializer]:
        try:
            user: UserEntity = UserEntity.objects.get(id=user_id)
        except UserEntity.DoesNotExist:
            raise NotFound('User with given id was not found')

        return list(map(lambda u: UserSerializer(instance=u), user.friends.all()))

    def get_friend_status(self, user_id: int, friend_id: int) -> FriendshipStatus:
        try:
            user: UserEntity = UserEntity.objects.get(id=user_id)
        except UserEntity.DoesNotExist:
            raise NotFound('User with given id was not found')

        if not UserEntity.objects.filter(id=friend_id).exists():
            raise NotFound('User with given id was not found')

        if user.friends.filter(id=friend_id).exists():
            return FriendshipStatus.FRIEND

        if user.incoming_invites.filter(id=friend_id).exists():
            return FriendshipStatus.INCOMING_INVITE

        if user.outcoming_invites.filter(id=friend_id).exists():
            return FriendshipStatus.OUTCOMING_INVITE

        return FriendshipStatus.NONE

    def get_incoming_invites(self, user_id: int) -> list[UserSerializer]:
        try:
            user = UserEntity.objects.get(id=user_id)
        except UserEntity.DoesNotExist:
            raise NotFound('User with given id was not found')

        return list(
            map(lambda u: UserSerializer(instance=u), user.incoming_invites.all())
        )

    def get_outcoming_invites(self, user_id: int) -> list[UserSerializer]:
        try:
            user = UserEntity.objects.get(id=user_id)
        except UserEntity.DoesNotExist:
            raise NotFound('User with given id was not found')

        return list(
            map(lambda u: UserSerializer(instance=u), user.outcoming_invites.all())
        )

    def invite_friend(self, user_id: int, friend_id: int):
        try:
            user: UserEntity = UserEntity.objects.get(id=user_id)
        except UserEntity.DoesNotExist:
            raise NotFound('User with given id was not found')

        try:
            friend: UserEntity = UserEntity.objects.get(id=friend_id)
        except UserEntity.DoesNotExist:
            raise NotFound('User with given id was not found')

        if user_id == friend_id:
            raise InvalidFormatException('Unable to invite yourself')

        if user.friends.filter(id=friend_id).exists():
            raise InvalidFormatException('Given user is already your friend')

        if user.outcoming_invites.filter(id=friend_id).exists():
            raise InvalidFormatException('Given user is already invited')

        if friend.outcoming_invites.contains(user):
            friend.outcoming_invites.remove(user)
            friend.friends.add(user)
            friend.save()
            return

        user.outcoming_invites.add(friend)
        user.save()

    def remove_friend(self, user_id: int, friend_id: int):
        try:
            user: UserEntity = UserEntity.objects.get(id=user_id)
        except UserEntity.DoesNotExist:
            raise NotFound('User with given id was not found')

        try:
            friend: UserEntity = UserEntity.objects.get(id=friend_id)
        except UserEntity.DoesNotExist:
            raise NotFound('User with given id was not found')

        if not user.friends.filter(id=friend_id).exists():
            raise InvalidFormatException('Given user is not your friend')

        user.friends.remove(friend)
        user.save()

    def accept_invite(self, user_id: int, friend_id: int):
        try:
            user: UserEntity = UserEntity.objects.get(id=user_id)
        except UserEntity.DoesNotExist:
            raise NotFound('User with given id was not found')

        try:
            friend: UserEntity = UserEntity.objects.get(id=friend_id)
        except UserEntity.DoesNotExist:
            raise NotFound('User with given id was not found')

        if not friend.outcoming_invites.filter(id=user_id).exists():
            raise InvalidFormatException('Given user did not send invite')

        friend.outcoming_invites.remove(user)
        friend.friends.add(user)
        friend.save()

    def decline_invite(self, user_id: int, friend_id: int):
        try:
            user: UserEntity = UserEntity.objects.get(id=user_id)
        except UserEntity.DoesNotExist:
            raise NotFound('User with given id was not found')

        try:
            friend: UserEntity = UserEntity.objects.get(id=friend_id)
        except UserEntity.DoesNotExist:
            raise NotFound('User with given id was not found')

        if not friend.outcoming_invites.filter(id=user_id).exists():
            raise InvalidFormatException('Given user did not send invite')

        friend.outcoming_invites.remove(user)
        friend.save()


user_service = UserService()
friends_service = FriendsService()
