import json
from django.core.management.base import BaseCommand

from common.models import Country, Region
from core.settings.base import BASE_DIR

class Command(BaseCommand):
    help = 'Load all regions'

    def handle(self, *args, **options):

        try:
            with open(str(BASE_DIR) + "/data/regions.json", encoding="utf-8") as f:
                regiones = json.load(f)
                country = Country.objects.get(name="O'zbekiston", code="UZ")
                for region in regiones:
                    Region.objects.get_or_create(name=region['name_uz'], country=country)

            self.stdout.write(self.style.SUCCESS('Regions loaded successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading Regions: {e}"))