from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from api.exceptions import InvalidFormatException
from api.serializers import UserCreateSerializer
from api.services import friends_service, user_service


@api_view(['POST'])
def register_user(request: Request):
    if request.user is AnonymousUser:
        raise PermissionDenied('Only anonymous users allowed to register')

    data = JSONParser().parse(request)
    user_dto = UserCreateSerializer(data=data)
    user_dto.is_valid(raise_exception=True)
    return JsonResponse(user_service.create(user_dto).data)


@api_view(['GET'])
def get_user_by_id(request: Request, user_id: int):
    user_dao = user_service.get_by_id(user_id)
    if user_dao is None:
        raise NotFound('User with given id was not found')
    return JsonResponse(user_dao.data)


@api_view(['GET'])
def search_users(request: Request):
    name_query = request.query_params.get('name')
    if name_query is None or len(name_query) == 0:
        raise InvalidFormatException('"name" query param is missing')

    try:
        limit = int(request.query_params.get('limit', '10'))
    except ValueError:
        raise InvalidFormatException('Unable to parse "limit" query param')

    return JsonResponse(
        list(map(
            lambda u: u.data,
            user_service.search_by_name(name_query, limit)
        )),
        safe=False
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_friend(request: Request, user_id: int):
    friends_service.invite_friend(request.user.id, user_id)
    return JsonResponse({})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_invite(request: Request, user_id: int):
    friends_service.accept_invite(request.user.id, user_id)
    return JsonResponse({})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_invite(request: Request, user_id: int):
    friends_service.decline_invite(request.user.id, user_id)
    return JsonResponse({})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_incoming_invites(request: Request):
    return JsonResponse(
        list(map(
            lambda u: u.data,
            friends_service.get_incoming_invites(request.user.id)
        )),
        safe=False
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outcoming_invites(request: Request):
    return JsonResponse(
        list(map(
            lambda u: u.data,
            friends_service.get_outcoming_invites(request.user.id)
        )),
        safe=False
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friends(request: Request):
    return JsonResponse(
        list(map(
            lambda u: u.data,
            friends_service.get_friends(request.user.id)
        )),
        safe=False
    )


class FriendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, user_id: int):
        return JsonResponse({
            'status': friends_service.get_friend_status(request.user.id, user_id)
        })

    def delete(self, request: Request, user_id: int):
        friends_service.remove_friend(request.user.id, user_id)
        return JsonResponse({})
