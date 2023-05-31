from typing import List

from domain.DatePicker import DateOptions
from domain.DTOs import PictureSelectionOption
from domain.SystemEnvironment import SystemEnvironment


def select_picture(
    date_picker_option: DateOptions,
    width: int,
    height: int,
    oldest_shown: List[PictureSelectionOption],
    recently_updated: List[PictureSelectionOption],
    on_this_day: List[PictureSelectionOption],
) -> PictureSelectionOption:
    layout = "landscape"
    if height > width:
        layout = "portrait"
    print(f"layout: {layout}")
    print(f"date_picker_option type: {date_picker_option.type}")
    selected_pic = None
    for p in oldest_shown:
        if p.layout == layout:
            selected_pic = p
            break
    return selected_pic
