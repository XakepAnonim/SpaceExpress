from geopy.distance import geodesic

from ..main.models import Warehouse


def calculate_delivery_options(company, delivery_city):
    """
    Функция для рассчета путей доставки от склада компании до указанного города
    """
    company_cities = company.cities.all()

    warehouses = []
    for city in company_cities:
        warehouse = Warehouse.objects.create(city=city)
        warehouses.append(warehouse)

    delivery_options = []
    for warehouse in warehouses:
        distance_km = geodesic(
            warehouse.city.coords, delivery_city.coords
        ).kilometers

        duration_hours = distance_km / 60
        delivery_cost = distance_km * 6 / 10

        delivery_options.append(
            {
                "path": f"{warehouse.city} — {delivery_city}",
                "distance": f"{distance_km:.2f}км",
                "time-cost": f"{duration_hours:.0f}ч",
                "price": f"{delivery_cost:.2f} руб.",
            }
        )
        best_option = min(
            delivery_options, key=lambda x: float(x["distance"][:-2])
        )

    Warehouse.objects.all().delete()

    return {
        "best_path": best_option,
    }
