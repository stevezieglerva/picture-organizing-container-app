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
        self._total_requests = 0.0
        self._cache_hits = 0.0
        self.cache_hit_ratio = 0.0

    def __str__(self):
        text = f"""_total_requests:   {self._total_requests}
_cache_hits:      {self._cache_hits}
cache_hit_ratio:  {self.cache_hit_ratio}
        """
        return text

    def locate(self, lat: float, long: float) -> City:
        print(f"Locating {lat} / {long}")
        self._total_requests += 1
        min_city = ""
        min_state = ""
        result = self._find_closest_in_list(self._cache, lat, long)
        if result != None:
            self._cache_hits += 1
            self.cache_hit_ratio = self._cache_hits / self._total_requests
            return result
        cities_in_range = self._repo.get_gis_data_by_lat_long(lat, long)
        self._cache.extend(cities_in_range)
        city = self._find_closest_in_list(cities_in_range, lat, long)
        self.cache_hit_ratio = self._cache_hits / self._total_requests
        return city

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
            print(
                f"{lat_delta:<6} + {long_delta:<6} = {gis_delta:<10} {city}, {state} "
            )
            if gis_delta < min_delta and gis_delta < 0.5:
                min_delta = gis_delta
                min_city = city
                min_state = state
                print(f"\t* Choosing: {min_city}")
                result = City(
                    city=min_city,
                    state=min_state,
                    min_combined_distance=gis_delta,
                    location="cache",
                )

        return result
