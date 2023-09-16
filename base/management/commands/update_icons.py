from io import BytesIO

import favicon
import requests
from PIL import Image
from django.core.files.base import ContentFile
from django.core.management import BaseCommand

from base.models import Feed

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'


def get_square_icon(icons):
    if not icons:
        return

    for icon in icons:
        if icon.width == icon.height:
            return icon

    return icons[0]


class Command(BaseCommand):
    help = "Update favicons"

    def handle(self, *args, **options):
        for feed in Feed.objects.all():


            try:
                icons = favicon.get(feed.site_url, headers={'User-Agent': USER_AGENT}, timeout=15)
                icon = get_square_icon(icons)
                print(feed.site_url)
            except:
                icon = None
                print(f"SKIP {feed.site_url}")

            if icon:
                try:
                    response = requests.get(icon.url, stream=True)
                except:
                    print(f"SKIP {feed.site_url}")
                else:
                    temp_name = '/tmp/python-favicon.{}'.format(icon.format)

                    try:
                        with open(temp_name, 'wb') as image:
                            for chunk in response.iter_content(1024):
                                image.write(chunk)

                        buffer = BytesIO()
                        with Image.open(temp_name) as image:
                            image.convert('RGBA')
                            image.save(buffer, format='PNG')

                        buffer.seek(0)
                    except:
                        print(f"INVALID {feed.site_url}")

                    feed.favicon.save(f'{feed.title}.png', ContentFile(buffer.getvalue()), save=True)
