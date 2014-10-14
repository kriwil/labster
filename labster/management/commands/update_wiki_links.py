import re

from django.core.management.base import BaseCommand

from wiki.models import Article


class Command(BaseCommand):

    def handle(self, *args, **options):
        compiled = re.compile(r'\(\/wiki(\/.+) "wikilink"\)')
        articles = Article.objects.all()
        for count, article in enumerate(articles, start=1):
            if not article.current_revision:
                continue

            content = article.current_revision.content
            new_content = compiled.sub('(wiki:\\1)', content)
            article.current_revision.content = new_content
            article.current_revision.save()
