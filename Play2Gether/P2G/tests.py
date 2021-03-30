from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from P2G.models import Category, Game, UserProfile, Group, Message, Score, User


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
        add_score(game, self.user, 1234567, False, timezone.now(), group)

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
    Check that scores date is not in the future
    """
    def Test(self):
        pass

    """
    Check that newly added scores are initially not approved
    """
    def Test(self):
        pass

    """
    Check that scores can be approved
    """
    def Test(self):
        pass

    """
    Check that scores can be denied
    """
    def Test(self):
        pass


class UserMethodTests(TestCase):
    """
    Check that users can change there Bio
    """
    def Test(self):
        pass

    """
    Check that users can add new friends
    """
    def Test(self):
        pass

    """
    Check that users can remove friends
    """
    def Test(self):
        pass



class MessageMethodTests(TestCase):
    """
    Check that users can send messages
    """
    def Test(self):
        pass


def add_group(game, name, users):
    g = Group.objects.get_or_create(game=game, name=name)[0]
    g.save()
    for user in users:
        g.users.add(user)
    return g


def add_score(game, user, score, approved, date, group):
    s = Score.objects.get_or_create(user=user, score=score, date=date, game=game, group=group)[0]
    s.approved = approved
    s.save()
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