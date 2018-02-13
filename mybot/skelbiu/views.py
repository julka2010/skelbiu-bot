import json
import sys
import traceback

from django.http import HttpResponseRedirect
from django.shortcuts import (
    render,
    redirect
)
from selenium import webdriver

from . import bot
from .models import (
    Advertisement,
    SkelbiuAccount,
)

def run_bot(request):
    for skelbiu_acc in SkelbiuAccount.objects.all():
        driver = webdriver.Chrome()
        bot.login(driver, skelbiu_acc.login, skelbiu_acc.password)
        skelbiu = bot.Advertisement(driver)
        skelbiu.delete_all()
        ads_to_publish_list = skelbiu_acc.advertisements.filter(active=True)
        with open('errors_log.csv', 'w') as errors_file:
            errors_file.write('[\n')
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
                    errors_file.write('{obj},\n'.format(obj=json.dumps(ad_info)))
                    continue
            errors_file.write(']\n')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
