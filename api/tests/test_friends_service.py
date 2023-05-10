from django.test import TestCase
from rest_framework.exceptions import NotFound

from api.models import UserEntity
from api.serializers import FriendshipStatus
from api.services import friends_service


class FriendsGetTestCase(TestCase):
    def setUp(self):
        self.friend_1 = UserEntity.objects.create_user('Theresa', 'kL)@_0Ze^1')
        self.friend_2 = UserEntity.objects.create_user('Cory', '+6o_RmYlPI')
        self.stranger = UserEntity.objects.create_user('Jesse', 'qB_9OgA&3f')

        self.friend_1.friends.add(self.friend_2)
        self.friend_1.save()

    def tearDown(self):
        self.friend_1.delete()
        self.friend_2.delete()
        self.stranger.delete()

    def test_positive_1(self):
        temp = friends_service.get_friends(self.friend_1.id)
        result = set(map(lambda u: (u.data['id'], u.data['name']), temp))

        self.assertEqual({(self.friend_2.id, self.friend_2.name)}, result)

    def test_positive_2(self):
        temp = friends_service.get_friends(self.friend_2.id)
        result = set(map(lambda u: (u.data['id'], u.data['name']), temp))

        self.assertEqual({(self.friend_1.id, self.friend_1.name)}, result)

    def test_positive_3(self):
        result = friends_service.get_friends(self.stranger.id)
        self.assertEqual(len(result), 0)

    def test_negative_unexisting_user(self):
        self.assertRaises(
            NotFound,
            lambda: friends_service.get_friends(self.stranger.id + 4)
        )


class FriendsStatusTestCase(TestCase):
    def setUp(self):
        self.friend_1 = UserEntity.objects.create_user('Theresa', 'kL)@_0Ze^1')
        self.friend_2 = UserEntity.objects.create_user('Cory', '+6o_RmYlPI')
        self.inviter = UserEntity.objects.create_user('Kevin', 'f^5RGucSeW')
        self.receiver = UserEntity.objects.create_user('Brian', 'J98hXLjj)t')
        self.stranger = UserEntity.objects.create_user('Jesse', 'qB_9OgA&3f')

        self.friend_1.friends.add(self.friend_2)
        self.friend_1.save()

        self.inviter.outcoming_invites.add(self.receiver)

    def tearDown(self):
        self.friend_1.delete()
        self.friend_2.delete()
        self.inviter.delete()
        self.receiver.delete()
        self.stranger.delete()

    def test_positive_1(self):
        self.assertEqual(
            friends_service.get_friend_status(self.friend_1.id, self.friend_2.id),
            FriendshipStatus.FRIEND
        )

    def test_positive_2(self):
        self.assertEqual(
            friends_service.get_friend_status(self.friend_2.id, self.friend_1.id),
            FriendshipStatus.FRIEND
        )

    def test_positive_3(self):
        self.assertEqual(
            friends_service.get_friend_status(self.inviter.id, self.receiver.id),
            FriendshipStatus.OUTCOMING_INVITE
        )

    def test_positive_4(self):
        self.assertEqual(
            friends_service.get_friend_status(self.receiver.id, self.inviter.id),
            FriendshipStatus.INCOMING_INVITE
        )

    def test_positive_5(self):
        self.assertEqual(
            friends_service.get_friend_status(self.stranger.id, self.friend_1.id),
            FriendshipStatus.NONE
        )

    def test_negative_unexisting_user(self):
        self.assertRaises(
            NotFound,
            lambda: friends_service.get_friend_status(self.stranger.id + 5, self.friend_1.id)
        )

    def test_negative_unexisting_friend(self):
        self.assertRaises(
            NotFound,
            lambda: friends_service.get_friend_status(self.friend_1.id, self.stranger.id + 5)
        )
