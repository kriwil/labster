import re

from django.core.management.base import BaseCommand

from wiki.models import Article


class Command(BaseCommand):

    def handle(self, *args, **options):
        compiled = re.compile(r'href=(""|\'\')')

        articles = Article.objects.all()
        fixed_count = 0
        for count, article in enumerate(articles, start=1):
            if not article.current_revision:
                continue

            html = article.render()
            search = compiled.search(html)
            if search:
                content = article.current_revision.content
                content = content.replace(' "wikilink"', '')
                content = content.replace('"wikilink"', '')
                article.current_revision.content = content
                article.current_revision.save()

                fixed_count += 1

        self.stdout.write("fixed: {}\n".format(fixed_count))
