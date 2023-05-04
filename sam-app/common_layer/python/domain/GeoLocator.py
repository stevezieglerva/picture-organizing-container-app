from dataclasses import asdict, dataclass
from typing import List

from infrastructure.repository.CatalogRepo import GISRecord, StoringCatalogData


@dataclass(frozen=True)
class City:
    city: str
    state: str
    min_combined_distance: float
    location: str


class GeoLocator:
    def __init__(self, repo: StoringCatalogData, cache: List[GISRecord] = []):
        self._repo = repo
        self._cache = cache

    def locate(self, lat: float, long: float) -> City:

        min_city = ""
        min_state = ""
        result = self._find_closest_in_list(self._cache, lat, long)
        if result != None:
            return result
        cities_in_range = self._repo.get_gis_data_by_lat_long(lat, long)
        return self._find_closest_in_list(cities_in_range, lat, long)

    def _find_closest_in_list(
        self, records: List[GISRecord], lat: float, long: float
    ) -> City:
        result = None
        min_delta = 1000.0
        for r in records:
            record_long = r.long
            record_lat = r.lat
            city = r.city
            state = r.state
            lat_delta = round(abs(lat - record_lat), 4)
            long_delta = round(abs(long - record_long), 4)
            gis_delta = round(lat_delta + long_delta, 4)
            print(f"{lat_delta:<6} + {long_delta:<6} = {gis_delta:<10} {city}")
            if gis_delta < min_delta and gis_delta < 0.5:
                min_delta = gis_delta
                min_city = city
                min_state = state
                print("Choosing: {min_city}")
                result = City(
                    city=min_city,
                    state=min_state,
                    min_combined_distance=gis_delta,
                    location="cache",
                )

        return result
