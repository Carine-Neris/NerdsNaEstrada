from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, user, name, email, password=None):
        if not user:
            raise ValueError('The given username and email must be set')
        email = self.normalize_email(email)
        user = self.model(user=user, name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user, name, email, password=None):
        user = self.create_user(user, name, email, password=password)
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    SEXO_CHOICES = [
        ('FEM', 'Feminino'),
        ('MAS', 'Masculino'),
    ]
    user = models.CharField('username', max_length=20, unique=True,
                            help_text='Required. 20 characters or fewer. Letters, \
                            numbers and @/./+/-/_ characters')
    name = models.CharField('name', max_length=50, null=False, blank=False)
    about_you = models.CharField('about you', max_length=300, blank=True)
    email = models.EmailField('email address', max_length=255, unique=True)
    sexoChoice = models.CharField('Gender', choices=SEXO_CHOICES, null=True, blank=True, max_length=10)
    is_staff = models.BooleanField('staff status', default=False, help_text= 'Designates whether the user can log into this admin site.')

    # o campo abaixo será utilizado pelo Django para autenticação
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user', 'name']

    objects = UserManager()

    class Meta:
        app_label = "blog"
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('title', max_length=150, null=False, blank=False)
    text = models.TextField('text', null=False, blank=False)
    author = models.ForeignKey('blog.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField('created date', default=timezone.now)
    published_date = models.DateTimeField('published date', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comentário feito  por {} em {}'.format(self.name, self.post)