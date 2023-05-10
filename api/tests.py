from django.test import TestCase

from api.exceptions import AlreadyExistsException
from api.models import UserEntity
from api.serializers import UserCreateSerializer
from api.services import user_service

USER_NAMES = [
    'Nicholas', 'Michelle', 'Miranda', 'Tiffany', 'Fred',
    'Pamela', 'Margaret', 'Scott', 'Jennifer', 'Thomas'
]
PASSWORDS = [
    'xGm38k09', 'VPsiA93M', 'fG2UvySC', 'JtaVJlcj', 'Pk4YeDHy',
    '4Nm6sbb9', 'diPjbI0d', 'EjCvKldr', '7eoPeCFH', 'zZ4PWMZQ'
]


class UserCreateTestCase(TestCase):
    def setUp(self):
        self.users = [
            UserEntity.objects.create_user(name, password)
            for name, password in zip(USER_NAMES, PASSWORDS)
        ]

    def tearDown(self):
        for user in self.users:
            user.delete()

    def test_positive(self):
        user_name = 'Sandra'
        password = '(4Fzm)b1Wl'

        user_dto = UserCreateSerializer(data={
            'name': user_name,
            'password': password
        })
        user_dto.is_valid(raise_exception=True)

        user = user_service.create(user_dto)

        self.assertEqual(user.data['name'], user_name)

        user_entity: UserEntity = UserEntity.objects.get(id=user.data['id'])

        self.assertEqual(user_entity, user.instance)
        self.assertEqual(user_entity.name, user_name)
        self.assertTrue(user_entity.check_password(password))

    def test_negative_existing_user(self):
        user_dto = UserCreateSerializer(data={
            'name': USER_NAMES[0],
            'password': PASSWORDS[0]
        })
        user_dto.is_valid(raise_exception=True)

        self.assertRaises(
            AlreadyExistsException,
            lambda: user_service.create(user_dto)
        )


class UserGetTestCase(TestCase):
    def setUp(self):
        self.users = [
            UserEntity.objects.create_user(name, password)
            for name, password in zip(USER_NAMES, PASSWORDS)
        ]

    def tearDown(self):
        for user in self.users:
            user.delete()

    def test_positive(self):
        for user in self.users:
            received_user = user_service.get_by_id(user.id)
            self.assertEqual(user.id, received_user.data['id'])
            self.assertEqual(user.name, received_user.data['name'])
            self.assertEqual(user, received_user.instance)

    def test_negative_unexisting_user(self):
        self.assertIsNone(user_service.get_by_id(len(self.users) + 2))


class UserSearchTestCase(TestCase):
    def setUp(self):
        self.users = [
            UserEntity.objects.create_user(name, password)
            for name, password in zip(USER_NAMES, PASSWORDS)
        ]

    def tearDown(self):
        for user in self.users:
            user.delete()

    def test_positive_1(self):
        for user in self.users:
            temp = user_service.search_by_name(user.name, 1)

            self.assertEqual(len(temp), 1)

            result = set(map(lambda u: (u.data['id'], u.data['name']), temp))

            self.assertIn((user.id, user.name), result)

    def test_positive_2(self):
        PHRASES = [
            ('ich', [0, 1]),
            ('as', [0, 9]),
            ('la', [0, 5]),
            ('if', [3, 8]),
            ('an', [2, 3])
        ]
        for phrase, idxs in PHRASES:
            temp = user_service.search_by_name(phrase, len(idxs))

            self.assertEqual(len(temp), len(idxs))

            result = set(map(lambda u: u.data['name'], temp))

            self.assertEqual(set(USER_NAMES[i] for i in idxs), result)
