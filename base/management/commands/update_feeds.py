import datetime
from multiprocessing import Pool

from django.core.management.base import BaseCommand

from base.models import Feed, Entry


def _update(x):
    x.update()


class Command(BaseCommand):
    help = "Updates all Feeds"

    def handle(self, *args, **options):

        pool = Pool(processes=20)
        try:
            pool.map(_update, Feed.objects.all())
        finally:
            pool.terminate()

        Entry.objects.filter(
            fetched_at__lte=datetime.datetime.now() - datetime.timedelta(days=60)).delete()
