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


def get_target_dimensions(width: int, height: int, user_agent: str):
    height_device_increase = 0
    if user_agent != None:
        if "Mac OS" in user_agent and (width == 1920 or width == 1680):
            height_device_increase = 50
            print(f"Adding height_device_increase: {height_device_increase}")
        if "Mac OS" in user_agent and width == 1112:
            height_device_increase = 70
            print(f"Adding height_device_increase: {height_device_increase}")

    return width, height + height_device_increase


def get_device_name(user_agent: str) -> str:
    if "Jio" in user_agent:
        return "Sony Bravia TV"
    if "iPhone OS 16_2" in user_agent:
        return "Steve Phone"
    if (
        "Mac OS X 10" in user_agent
        and "Chrome" not in user_agent
        and "Firefox" not in user_agent
    ):
        return "Charlotte iPad"
    if "Mac OS X 10" in user_agent:
        return "Steve Laptop"
    return ""
