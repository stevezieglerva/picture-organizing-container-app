from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass(frozen=True)
class Guess:
    source: str
    city: str
    state: str


class LocationGuesser:
    def guess(self, source: str, date_taken: datetime):
        if (
            "disney" in source.lower()
            and date_taken.year == 2022
            and date_taken.month == 6
        ):
            return Guess(source=source, city="Lake Buena Vista", state="FL")
        if (
            "disney" in source.lower()
            and date_taken.year == 2014
            and date_taken.month == 8
        ):
            return Guess(source=source, city="Lake Buena Vista", state="FL")

        if date_taken.year == 2012 and date_taken.month == 5 and date_taken.day == 30:
            return Guess(source=source, city="Clifton", state="VA")

        if (
            "Steve_15_Year_UVA_Reunion" in source
            or "Charlottesville" in source
            or "2019-10-19" in source
        ):
            return Guess(source=source, city="Charlottesville", state="VA")

        if (
            "Ocean_City" in source
            or "Ziegler_Beach_Trip" in source
            or "Beach_2020-09" in source
        ):
            return Guess(source=source, city="Ocean City", state="MD")

        if "Asheville" in source:
            return Guess(source=source, city="Asheville", state="NC")

        if "Florida_Spring_Break" in source:
            return Guess(source=source, city="Fort Myers", state="FL")

        if "Luray_Caverns" in source:
            return Guess(source=source, city="Luray", state="VA")

        if "Cox_Farm" in source:
            return Guess(source=source, city="Centreville", state="VA")

        if "Ghost_Train" in source or "Burke_Lake_Park" in source:
            return Guess(source=source, city="Fairfax Station", state="VA")

        if "Glen_Echo" in source:
            return Guess(source=source, city="Glen Echo", state="VA")

        if "Tysons_Corner" in source or "Tea_Ritz_Carlton" in source:
            return Guess(source=source, city="Tysons", state="VA")

        if "Garden_Easter" in source:
            return Guess(source=source, city="Wheaton", state="MD")

        if "Beach_2021-08" in source or "Beach_Canon_2021-08" in source:
            return Guess(source=source, city="Surf City", state="NC")

        if "Rebecca_Danzenbaker" in source:
            return Guess(source=source, city="Ashburn", state="VA")

        if "2012_05_20_" in source in source:
            return Guess(source=source, city="Upperville", state="VA")

        if (
            "Owen_Birthday_DC" in source
            or "National_Harbor" in source
            or "Caps_Parade" in source
        ):
            return Guess(source=source, city="Washington", state="DC")

        if "Thanksgiving" in source:
            return Guess(source=source, city="Gainesville", state="VA")

        if "Farm_School" in source or "Frying_Pan" in source:
            return Guess(source=source, city="Herdon", state="VA")

        if "Omni_Homestead" in source:
            return Guess(source=source, city="Hot Springs", state="VA")

        if "Clemijontri" in source:
            return Guess(source=source, city="McLean", state="VA")

        if "Charlotte_Preschool" in source:
            return Guess(source=source, city="Apex", state="NC")

        if "_TAC" in source:
            return Guess(source=source, city="Cary", state="NC")

        if (
            "christmas" in source.lower()
            or "easter" in source.lower()
            or "halloween" in source.lower()
            or "pool" in source.lower()
        ) and date_taken.year >= 2018:
            return Guess(source=source, city="Apex", state="NC")

        if (
            "christmas" in source.lower()
            or "easter" in source.lower()
            or "halloween" in source.lower()
            or "pool" in source.lower()
        ) and date_taken.year < 2018:
            return Guess(source=source, city="Clifton", state="VA")

        if ("pumpkin_picking" in source.lower()) and date_taken.year < 2018:
            return Guess(source=source, city="Delaplane", state="VA")

        return None
