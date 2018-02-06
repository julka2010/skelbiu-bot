import csv
import sys
import traceback

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
    failed_ads = []
    with open('errors_log.csv', 'w') as errors_file:
        writer = csv.DictWriter(
            errors_file,
            dialect='excel',
            fieldnames=[
                'title',
                'exc_type',
                'exc_value',
                'exc_traceback',
                'action',
                'category',
                'phone',
                'city',
                'price',
                'description',
                'photos',
                ]
        )
        writer.writeheader()
        for ad in ads_to_publish_list:
            images = ad.images.all()
            images_path = [t.image.path for t in images]
            ad_info = {
                'action': ad.action,
                'category': ad.category_as_list,
                'city': ad.city,
                'description': ad.description,
                'phone': ad.phone.phone_number,
                'photos': images_path,
                'price': str(ad.price),
                'title': ad.title,
            }
            try:
                skelbiu.publish(**ad_info)
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                ad_info['photos'] = '\r\n'.join(ad_info['photos'])
                ad_info['exc_type'] = exc_type
                ad_info['exc_value'] = exc_value
                ad_info['exc_traceback'] = ''.join(
                    traceback.format_tb(exc_traceback))
                writer.writerow(ad_info)
                continue
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
