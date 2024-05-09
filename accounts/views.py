from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# 会員登録ページに関する処理
class SignUpView(generic.CreateView): 
    form_class = UserCreationForm
    success_url = reverse_lazy('login') #リダイレクト先のURL
    template_name = 'registration/signup.html'

