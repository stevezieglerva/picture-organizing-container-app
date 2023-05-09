import random
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import List

from domain.DTOs import HashRecord, MissingGISData, PictureCatalogGroup, PictureRecord
from domain.GeoLocator import GeoLocator
from domain.LocationGuesser import LocationGuesser
from domain.Picture import ImageIO, Picture
from infrastructure.repository.CatalogRepo import StoringCatalogData
from infrastructure.system.Clock import ITellingTime
from ulid import ULID


class AddNewPicture:
    def __init__(self, repo: StoringCatalogData, clock: ITellingTime):
        self._repo = repo
        self._clock = clock
        self._geo_locator = GeoLocator(repo)

    def add_new_picture_to_catalog(self, picture: Picture) -> PictureCatalogGroup:
        records = self._convert_picture_to_catalogrecords(
            picture,
            self._clock.get_time(),
            self._clock.get_time(),
            "created",
        )
        self._repo.add_new_picture_to_catalog(records)
        return records

    def _convert_picture_to_catalogrecords(
        self,
        picture: Picture,
        date_added: datetime,
        date_updated: datetime,
        new_update_desc: str,
    ) -> PictureCatalogGroup:
        layout = "landscape"
        if picture.height > picture.width:
            layout = "portrait"
        update_tmsp = date_updated.strftime("%m/%d/%y")

        city = ""
        state = ""
        missing_gis_data = None
        gis_lat = -1
        if picture.gis_lat != None:
            gis_lat = picture.gis_lat
        gis_long = -1
        if picture.gis_long != None:
            gis_long = picture.gis_long
        if gis_lat != -1 and gis_long != -1:
            print("Geolocating ...")
            location = self._geo_locator.locate(gis_lat, gis_long)
            if location != None:
                city = location.city
                state = location.state
        if gis_lat == -1 and gis_long == -1:
            print("Guesing...")
            guess = LocationGuesser().guess(picture.source, picture.taken)
            if guess != None:
                city = guess.city
                state = guess.state
        if city == "":
            print("Giving up on GIS data ...")
            missing_gis_data = MissingGISData(
                pk="MISSING_GIS",
                sk=picture.source,
                s3_url=picture.source,
                date_added=self._clock.get_time(),
                date_updated=self._clock.get_time(),
            )

        random_shown = random.randint(1, 100)
        last_shown_pk = "NEVER_SHOW"
        last_shown_date = datetime(1900, 1, 1)
        last_shown_sk = "-"
        if "original" in picture.source:
            last_shown_pk = f"LAST_SHOWN#{layout}"
            last_shown_date = date_added - timedelta(days=1)
            last_shown_sk = f"{last_shown_date.strftime('%Y-%m-%d')}_{random_shown}"

        on_this_day = picture.taken.strftime("%m-%d")
        model = ""
        if picture.model:
            model = picture.model
        picture_record = PictureRecord(
            pk=f"PICTURE",
            sk=picture.source,
            # only shown if original
            gsi1_pk=last_shown_pk,
            gsi1_sk=last_shown_sk,
            gsi2_pk=f"DATE_ADDED#{layout}",
            gsi2_sk=f"{date_added.isoformat()}",
            gsi3_pk=f"ON_THIS_DAY#{on_this_day}",
            gsi3_sk=f"{picture.taken.isoformat()}",
            gsi4_pk="UNIQUE_HASH",
            gsi4_sk=str(picture.hash_unique),
            gsi5_pk="DATE_TAKEN",
            gsi5_sk=picture.taken.isoformat(),
            ulid=str(ULID()),
            s3_url=picture.source,
            date_taken=picture.taken,
            date_added=date_added,
            date_updated=date_updated,
            height=picture.height,
            width=picture.width,
            layout=layout,
            view_count=0,
            hash_average_hash=str(picture.hash_average_hash),
            hash_crop_resistant=str(picture.hash_crop_resistant),
            hash_phash=str(picture.hash_phash),
            hash_unique=str(picture.hash_unique),
            year=picture.taken.year,
            month=picture.taken.month,
            day=picture.taken.day,
            model=model,
            update_desc=f"{update_tmsp}-{new_update_desc}",
            gis_lat=gis_lat,
            gis_long=gis_long,
            city=city,
            state=state,
            last_shown=last_shown_date,
        )
        hashes = [
            self._create_hash_dynamodb_recordset(
                "AVERAGE_HASH", str(picture.hash_average_hash), picture.source
            )
        ]
        hashes.append(
            self._create_hash_dynamodb_recordset(
                "PHASH", str(picture.hash_phash), picture.source
            )
        )
        return PictureCatalogGroup(
            picture=picture_record, hashes=hashes, missing_gis_data=missing_gis_data
        )

    def _create_hash_dynamodb_recordset(
        self,
        hash_type: str,
        hash_value: str,
        s3_url: str,
    ) -> dict:
        records = []
        print(f"\t\t{hash_type}/{hash_value}")

        hash_record = HashRecord(
            pk=f"HASH_{hash_type}",
            sk=s3_url,
            hash_type=hash_type,
            hash_value=hash_value,
            s3_url=s3_url,
            gsi1_pk=f"{hash_type}_1",
            gsi1_sk=hash_value[0:4],
            gsi2_pk=f"{hash_type}_2",
            gsi2_sk=hash_value[4:8],
            gsi3_pk=f"{hash_type}_3",
            gsi3_sk=hash_value[8:12],
            gsi4_pk=f"{hash_type}_4",
            gsi4_sk=hash_value[12:],
        )

        return hash_record
