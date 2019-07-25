"""
    core.py - Main hub of application
"""
import client

if __name__ == "__main__":
    players = client.get_players_from_image()
    print("Players are: ", players)
