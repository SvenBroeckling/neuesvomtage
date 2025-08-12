import datetime
import re
import os

from django.core.management import BaseCommand
from django.conf import settings

from base.models import Entry, TopWord, TopWordLemmaWord

DIR = os.path.join(settings.BASE_DIR, 'contrib')


class WordList:
    def __init__(self):
        self.words = {}
        with open(os.path.join(DIR, 'frequent_german.txt'), 'r') as fw:
            self.frequent_german_words = [w.strip().lower() for w in fw.readlines()]
        with open(os.path.join(DIR, 'frequent_english.txt'), 'r') as fw:
            self.frequent_english_words = [w.strip().lower() for w in fw.readlines()]
        with open(os.path.join(DIR, 'frequent_french.txt'), 'r') as fw:
            self.frequent_french_words = [w.strip().lower() for w in fw.readlines()]

    def word_valid(self, word):
        if not word:
            return False
        if len(word) < 3:
            return False
        if word in self.frequent_german_words:
            return False
        if word in self.frequent_english_words:
            return False
        if word in self.frequent_french_words:
            return False
        return True

    def get_lemma(self, word):
        qs = TopWordLemmaWord.objects.filter(word__iexact=word)
        if qs.exists():
            return qs.earliest('id').lemma.lemma
        return word

    def insert_word(self, word):
        if not self.word_valid(word):
            return

        word = self.get_lemma(word)

        if word not in self.words.keys():
            self.words[word] = {
                'count': 1,
                'similar': [],
            }
        else:
            self.words[word]['count'] += 1

    def sorted_list(self, min_count=0):
        sl = [(x[0], x[1]['count']) for x in self.words.items() if x[1]['count'] > min_count]
        return sorted(sl, key=lambda x: x[1])


class Command(BaseCommand):
    help = "Generate the Top Word list"
    words = {}

    def handle(self, *args, **options):
        entries = Entry.objects.filter(
            created_at__gte=datetime.datetime.now() - datetime.timedelta(days=1))
        word_list = WordList()

        for e in entries:
            cleaned_title = re.sub('[^a-zA-ZäöüÄÖÜß-]', ' ', e.title).lower()
            for word in cleaned_title.split(' '):
                word_list.insert_word(word.strip(' -'))

        TopWord.objects.all().delete()
        for tw in word_list.sorted_list(min_count=10):
            TopWord.objects.create(word=tw[0], count=tw[1])
