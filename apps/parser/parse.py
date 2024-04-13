import json
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.main.models import City  # noqa: E402


def parse_cities(json_file):
    with open(json_file, encoding="utf-8") as file:
        cities_data = json.load(file)

    for city_data in cities_data:
        name = city_data["name"].lower()
        lat = city_data["coords"]["lat"]
        lon = city_data["coords"]["lon"]

        city, created = City.objects.get_or_create(name=name)
        city.coords = f"{lat}, {lon}"
        city.save()


if __name__ == "__main__":
    json_file = "resources/russian-cities.json"
    parse_cities(json_file)
