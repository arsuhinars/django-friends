from api.exceptions import AlreadyExistsException
from api.models import UserEntity
from api.serializers import UserCreateSerializer, UserSerializer


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


user_service = UserService()
