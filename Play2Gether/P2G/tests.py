from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from P2G.models import Category, Game, UserProfile, Group, Message, Score, User
from Play2Gether import settings
from populate_P2G import populate


class CategoryViewTests(TestCase):
    """
    If there are no categories proper message should be displayed
    """
    def test_category_view_with_no_categories(self):
        response = self.client.get(reverse('P2G:categories'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are currently no Categories')
        self.assertQuerysetEqual(response.context['categories'], [])

    """
    Check whether new Categories are displayed properly
    """
    def test_categories_are_added_properly(self):
        category = add_cat('TestName', 'TestDescription', 10)
        response = self.client.get(reverse('P2G:categories'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestName')
        self.assertContains(response, 'TestDescription')

class GameViewTests(TestCase):
    """
    If there are no games proper message should be displayed
    """
    def test_game_view_with_no_games(self):
        response = self.client.get(reverse('P2G:games'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are currently no Games.')
        self.assertQuerysetEqual(response.context['games'], [])

    """
    Check whether new Games are displayed properly
    """
    def test_games_are_added_properly(self):
        category = add_cat('TestName', 'TestDescription', 10)
        game = add_game(category, 'TestGameName', "http://www.test.com", 'TestGameDescription', 10, 10)
        response = self.client.get(reverse('P2G:games'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestGameName')
        self.assertContains(response, 'TestGameDescription')

    """
    Check whether one can search for games
    """
    def test_search_game_function(self):
        category = add_cat('TestName', 'TestDescription', 10)
        game = add_game(category, 'TestGameName', "http://www.test.com", 'TestGameDescription', 10, 10)
        response = self.client.get('/P2G/suggest/', {'suggestion': 'Te'})
        self.assertContains(response, 'TestGameName')
        self.assertContains(response, 'TestGameDescription')
        response = self.client.get('/P2G/suggest/', {'suggestion': 'A'})
        self.assertNotContains(response, 'TestGameName')

    """
    Check whether one can search for games no matter if upper or lowercase
    """
    def test_search_game_function_lower_upper_case_independence(self):
        category = add_cat('TestName', 'TestDescription', 10)
        game = add_game(category, 'TestGameName', "http://www.test.com", 'TestGameDescription', 10, 10)
        response = self.client.get('/P2G/suggest/', {'suggestion': 'tE'})
        self.assertContains(response, 'TestGameName')
        self.assertContains(response, 'TestGameDescription')


class OtherPlayersViewTests(TestCase):
    """
    If there are no Users proper message should be displayed
    """
    def test_other_players_with_no_players(self):
        self.user = add_user('John', 'Test').user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(reverse('P2G:otherPlayers', kwargs={'username': self.user.username}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no users on P2G.')
        self.assertQuerysetEqual(response.context['user_profile_list'], [])

    """
    Check whether new Users are displayed properly
    """
    def test_users_are_added_properly(self):
        add_user('Max', 'TestBio')
        self.user = add_user('John', 'Test').user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(reverse('P2G:otherPlayers', kwargs={'username': self.user.username}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Max')

    """
    Check whether one can search for other players
    """
    def test_search_other_players_function(self):
        add_user('Max', 'TestBio')
        self.user = add_user('John', 'Test').user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)

        response = self.client.get('/P2G/search_others/', {'suggestion': 'Ma', 'user_id': self.user.id})
        self.assertContains(response, 'Max')
        response = self.client.get('/P2G/search_others/', {'suggestion': 'A', 'user_id': self.user.id})
        self.assertNotContains(response, 'Max')

    """
    Check whether one can search for other players no matter if upper or lowercase
    """
    def test_search_other_players_function_lower_upper_case_independence(self):
        add_user('Max', 'TestBio')
        self.user = add_user('John', 'Test').user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)

        response = self.client.get('/P2G/search_others/', {'suggestion': 'mA', 'user_id': self.user.id})
        self.assertContains(response, 'Max')


class FriendsViewTests(TestCase):
    """
    If there are no Friends proper message should be displayed
    """
    def test_friends_view_with_no_friends(self):
        self.user = add_user('John', 'Test').user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(reverse('P2G:friends', kwargs={'username': self.user.username}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You haven't added any friends yet. Search for Players and add them to your friend list.")
        self.assertQuerysetEqual(response.context['friends'], [])

    """
    Check whether new Friends are displayed properly
    """
    def test_users_are_added_properly(self):
        friend = add_user('Max', 'TestBio')
        profile = add_user('John', 'Test')
        self.user = profile.user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        profile.friends.add(friend)
        response = self.client.get(reverse('P2G:friends', kwargs={'username': self.user.username}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Max')

    """
    Check whether one can search for friends
    """

    def test_search_friends_function(self):
        friend = add_user('Max', 'TestBio')
        profile = add_user('John', 'Test')
        self.user = profile.user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        profile.friends.add(friend)

        response = self.client.get('/P2G/search_friends/', {'suggestion': 'Ma', 'user_id': self.user.id})
        self.assertContains(response, 'Max')
        response = self.client.get('/P2G/search_friends/', {'suggestion': 'A', 'user_id': self.user.id})
        self.assertNotContains(response, 'Max')

    """
    Check whether one can search for friends no matter if upper or lowercase
    """

    def test_search_friends_function_lower_upper_case_independence(self):
        friend = add_user('Max', 'TestBio')
        profile = add_user('John', 'Test')
        self.user = profile.user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        profile.friends.add(friend)

        response = self.client.get('/P2G/search_friends/', {'suggestion': 'mA', 'user_id': self.user.id})
        self.assertContains(response, 'Max')


class ScoreViewTests(TestCase):
    """
    If there are no Scores proper message should be displayed
    """
    #def test_score_view_with_no_scores(self):
    #    response = self.client.get(reverse('P2G:highscores'))

    #    self.assertEqual(response.status_code, 200)
    #    self.assertContains(response, 'There are currently no Scores')
    #    self.assertQuerysetEqual(response.context['categories'], [])

    """
    Check whether new Scores are displayed properly
    """
    def Test(self):
        pass


class GroupViewTests(TestCase):
    """
    If there are no Groups proper message should be displayed
    """
    def test_groups_view_with_no_groups(self):
        self.user = add_user('John', 'Test').user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.get(reverse('P2G:groups', kwargs={'user_id': self.user.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are currently in no Group')
        self.assertQuerysetEqual(response.context['groups'], [])

    """
    Check if a new group can be added and is displayed in the groups view
    """
    def test_groups_view_with_added_group(self):
        self.user = add_user('John', 'Test').user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        category = add_cat('TestName', 'TestDescription', 10)
        game = add_game(category, 'TestGameName', "http://www.test.com", 'TestGameDescription', 10, 10)
        group = add_group(game, 'Testgroup', [self.user])

        response = self.client.get(reverse('P2G:groups', kwargs={'user_id': self.user.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestGameName')

    """
    Check whether new Scores are displayed properly in the scores table
    """
    def test_score_is_added_in_the_group(self):
        self.user = add_user('John', 'Test').user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        category = add_cat('TestName', 'TestDescription', 10)
        game = add_game(category, 'TestGameName', "http://www.test.com", 'TestGameDescription', 10, 10)
        group = add_group(game, 'Testgroup', [self.user])
        add_score(game, self.user, 1234567, timezone.now(), group)

        response = self.client.get(reverse('P2G:group', kwargs={'group_id': group.id, 'user_id': self.user.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1234567')


    """
    Check whether new Messages are received properly
    """
    def test_that_messages_get_added_to_group(self):
        self.user = add_user('John', 'Test').user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        category = add_cat('TestName', 'TestDescription', 10)
        game = add_game(category, 'TestGameName', "http://www.test.com", 'TestGameDescription', 10, 10)
        group = add_group(game, 'Testgroup', [self.user])
        Message.objects.create(sender=self.user, content='Hi that is a Test Message', date=timezone.now(), group=group)

        response = self.client.get(reverse('P2G:group', kwargs={'group_id': group.id, 'user_id': self.user.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hi that is a Test Message')


class ScoreMethodTests(TestCase):
    """
    Check that newly added scores are initially not approved
    """
    def test_score_is_initially_not_approved(self):
        self.user = add_user('John', 'Test').user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        category = add_cat('TestName', 'TestDescription', 10)
        game = add_game(category, 'TestGameName', "http://www.test.com", 'TestGameDescription', 10, 10)
        group = add_group(game, 'Testgroup', [self.user])
        score = add_score(game, self.user, 1234567, timezone.now(), group)

        self.assertTrue(score.approved == False)


    """
    Check that scores can be approved
    """
    def test_scores_can_be_approved(self):
        self.user = add_user('John', 'Test').user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        category = add_cat('TestName', 'TestDescription', 10)
        game = add_game(category, 'TestGameName', "http://www.test.com", 'TestGameDescription', 10, 10)
        group = add_group(game, 'Testgroup', [self.user])
        score = add_score(game, self.user, 1234567, timezone.now(), group)

        self.assertFalse(score.approved)
        self.client.get('/P2G/approve_score/', {'score_id': score.id, 'group_id': group.id, 'user_id': self.user.id})
        updated_score = Score.objects.get(id=score.id)
        self.assertTrue(updated_score.approved)


    """
    Check that scores can be denied
    """
    def test_scores_can_be_denied(self):
        self.user = add_user('John', 'Test').user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        category = add_cat('TestName', 'TestDescription', 10)
        game = add_game(category, 'TestGameName', "http://www.test.com", 'TestGameDescription', 10, 10)
        group = add_group(game, 'Testgroup', [self.user])
        score = add_score(game, self.user, 1234567, timezone.now(), group)

        self.assertFalse(score.approved)
        self.client.get('/P2G/remove_score/', {'score_id': score.id, 'group_id': group.id, 'user_id': self.user.id})
        updated_score = Score.objects.filter(id=score.id).count()
        self.assertTrue(updated_score == 0)


class UserMethodTests(TestCase):
    """
    Check that users can add friends
    """
    def test_users_can_add_friends(self):
        friend = add_user('Max', 'TestBio')
        profile = add_user('John', 'Test')
        self.user = profile.user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        self.client.get('/P2G/add_friend/', {'user_id': profile.id, 'friend_id': friend.id})

        self.assertEquals(profile.friends.all()[0], UserProfile.objects.get(id=friend.id))


    """
    Check that users can remove friends
    """
    def test_users_can_remove_friends(self):
        friend = add_user('Max', 'TestBio')
        profile = add_user('John', 'Test')
        self.user = profile.user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        self.client.get('/P2G/add_friend/', {'user_id': profile.id, 'friend_id': friend.id})

        self.assertEquals(profile.friends.all()[0], UserProfile.objects.get(id=friend.id))
        self.client.get('/P2G/remove_friend/', {'user_id': profile.id, 'friend_id': friend.id})
        self.assertEquals(profile.friends.all().count(), 0)

class MessageMethodTests(TestCase):
    """
    Check that users can send messages
    """
    def test_message_send_method(self):
        self.user = add_user('John', 'Test').user
        self.user.set_password('Weddemann')
        self.user.save()
        self.client.force_login(self.user)
        category = add_cat('TestName', 'TestDescription', 10)
        game = add_game(category, 'TestGameName', "http://www.test.com", 'TestGameDescription', 10, 10)
        group = add_group(game, 'Testgroup', [self.user])

        self.client.get('/P2G/group_add_message/', {'user_id': self.user.id,
                                                    'group_id': group.id,
                                                    'message': 'Hi there, this is a test message'})
        self.assertEquals(Message.objects.get(group=group).content, 'Hi there, this is a test message')


class CookiesTest(TestCase):
    """
    Tests if cookies can be used, at least on the server-side.
    """
    def testMiddleware(self):
        #Tests to see if the SessionMiddleware is present.
        self.assertTrue('django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE)

    def sessionApp(self):
        #Makes sure the sessions app is present.
        self.assertTrue('django.contrib.sessions' in settings.INSTALLED_APPS)


def add_group(game, name, users):
    g = Group.objects.get_or_create(game=game, name=name)[0]
    g.save()
    for user in users:
        g.users.add(user)
    return g


def add_score(game, user, score, date, group):
    s = Score.objects.get_or_create(user=user, score=score, date=date, game=game, group=group)[0]
    return s


def add_user(name, bio):
    u = User.objects.get_or_create(username=name)[0]
    u.save()
    p = UserProfile.objects.get_or_create(user=u)[0]
    p.bio = bio
    p.save()
    return p


def add_cat(name, description, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.description = description
    c.likes = likes
    c.save()
    return c


def add_game(cat, name, link, description, play_count, likes):
    g = Game.objects.get_or_create(category=cat, name=name)[0]
    g.link = link
    g.description = description
    g.play_count = play_count
    g.likes = likes
    g.save()
    return g