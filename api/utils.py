from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

from User.models import Profile

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        profile=Profile.objects.get(user=user)
        return (six.text_type(user.id)+six.text_type(timestamp)+six.text_type(profile.is_verified))    

generate_token=TokenGenerator()

class PasswordGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        print(login_timestamp)
        return (six.text_type(user.id)+six.text_type(timestamp)+six.text_type(login_timestamp))

reset_token=PasswordGenerator()