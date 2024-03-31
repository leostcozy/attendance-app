from django.test import TestCase, Client
from django.contrib.auth.models import User
# Create your tests here.

class LoginRedirectTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'testpass'
        }
        User.objects.create_user(**self.credentials)

        # テストクライアントのインスタンスを設定
        self.client = Client()

    def test_redirect(self):
        '''
        ログインしていない状態でアクセスするとリダイレクトされるか
        '''
        response = self.client.get('/', follow=True)
        # リダイレクト情報を取得
        redirect_url = list(response.redirect_chain[0])[0]
        # リダイレクト先のURLが設定されていること
        self.assertEqual(redirect_url, '/accounts/login/?next=/')

    def test_not_redirect(self):
        '''
        ログインしている状態でアクセスするとリダイレクトされないか
        '''
        # テストユーザーでログイン
        self.client.login(
            username=self.credentials['username'], 
            password=self.credentials['password']
        )
        response = self.client.get('/')
        # リダイレクトされず画面を開くこと
        self.assertEqual(response.status_code, 200)