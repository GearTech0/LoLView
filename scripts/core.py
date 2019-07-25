"""
    core.py - Main hub of application
"""
from client import get_client_screenshot, get_players_from_image
from client import scale_and_resample
import os

if __name__ == "__main__":
    data_folder = os.path.join(
        os.path.basename(__file__), "../data/image_300.jpg")

    players = get_players_from_image(get_client_screenshot())
    print("Players are: ", players)
