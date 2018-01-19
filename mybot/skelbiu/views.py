from django.http import HttpResponseRedirect
from django.shortcuts import (
    render,
    redirect
)
from selenium import webdriver

from . import bot
from .models import Advertisement

def run_bot(request):
    driver = webdriver.Chrome()
    bot.login(driver)
    skelbiu = bot.Advertisement(driver)
    ads_to_publish_list = Advertisement.objects.all()
    for ad in ads_to_publish_list:
        images = ad.images.all()
        images_path = [t.image.path for t in images]
        skelbiu.publish(
            action = ad.action,
            category = ad.category_as_list,
            city = ad.city,
            description = ad.description,
            phone = ad.phone.phone_number,
            photos = images_path,
            price = str(ad.price),
            title = ad.title
        )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
