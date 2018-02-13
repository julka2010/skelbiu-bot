from django.core.validators import RegexValidator
from django.db import models
from djmoney.models.fields import MoneyField
from django.utils.timezone import now

PROPOSE = 'propose'
LOOKING = 'looking'

ACTION_CHOICES = (
    (PROPOSE, 'Siūlau'),
    (LOOKING, 'Ieškau'),
)

class PhoneModel(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\d{8,8}$',
        message=(
            "Phone number must be entered in the format: '61234567'. "
            "Do not include +370 or 8."
        )
    )
    phone_number = models.CharField(
        validators=[phone_regex],  # validators should be a list
        max_length=17,
        blank=True
    )

    def __str__(self):
        return self.phone_number


class SkelbiuAccount(models.Model):
    phone = models.ForeignKey(
        PhoneModel,
        on_delete=models.PROTECT,
    )
    email = models.EmailField(null=True)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.login


class Advertisement(models.Model):
    action = models.CharField(
        max_length=8,
        choices=ACTION_CHOICES,
        default=PROPOSE,
    )
    active = models.BooleanField(default=True)
    category = models.CharField(max_length=200)
    city = models.CharField(max_length=20, default='Vilnius')
    description = models.TextField()
    skelbiu_account = models.ForeignKey(
        SkelbiuAccount,
        on_delete=models.PROTECT,
        related_name='advertisements',
    )
    price = MoneyField(decimal_places=2, default_currency='EUR', max_digits=8)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    @property
    def category_as_list(self):
        return self.category.split('>')


class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(
        Advertisement,
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = models.ImageField()

    def __str__(self):
        return self.image.name
