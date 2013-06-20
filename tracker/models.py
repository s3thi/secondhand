from django.contrib.auth.models import User
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.db import models


class ApiToken(models.Model):
    # TODO: write tests for ApiToken.

    EXPIRY_SECONDS = 7 * 24 * 60 * 60

    user = models.ForeignKey(User)
    token = models.CharField(max_length=256)
    generated_on = models.DateTimeField(auto_now_add=True)
    expiry_seconds = models.IntegerField(default=EXPIRY_SECONDS)
    force_expiry = models.BooleanField(default=False)

    @staticmethod
    def generate_api_token(user, expiry_seconds=EXPIRY_SECONDS):
        signer = TimestampSigner()
        token = signer.sign(user.username)

        api_token = ApiToken(user=user,
                             expiry_seconds=expiry_seconds,
                             token=token)
        api_token.save()
        return api_token

    def is_valid(self):
        if self.force_expiry:
            return False

        signer = TimestampSigner()

        try:
            username = signer.unsign(self.token, max_age=self.expiry_seconds)
        except (BadSignature, SignatureExpired):
            return False

        return username == self.user.username

    def expire(self):
        self.force_expiry = True
        self.save()

    def __unicode__(self):
        if self.is_valid():
            return 'Token for {0}'.format(self.user.username)
        else:
            return 'Expired token for {0}'.format(self.user.username)


class Project(models.Model):
    name = models.TextField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class Task(models.Model):
    name = models.TextField()
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class WorkSession(models.Model):
    task = models.ForeignKey('Task')
    user = models.ForeignKey(User)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __unicode__(self):
        return 'Session for {0}'.format(self.task.name)
