from django.contrib.auth import get_user_model
from django import forms

class SignUpForm(forms.ModelForm):

    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)
    Repeat_password = forms.CharField(label = 'Repeat_password', widget=forms.PasswordInput)
    # phone = forms.CharField(label='phone', max_length=13)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'Repeat_password', 'name', 'phone', 'email', 'message']

    def clean_Repeat_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['Repeat_password']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return cd['Repeat_password']