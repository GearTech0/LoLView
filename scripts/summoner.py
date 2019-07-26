"""
    summoner.py - Riot API wrapper
"""
import json
import riotwatcher
from os.path import join
import os

ROOT = join(
        os.path.basename(__file__), "../")


def create(name_or_list):
    if type(name_or_list) is 'str':
        return Summoner(name_or_list)
    else:
        return [Summoner(summoner) for summoner in name_or_list]


class Summoner():
    def __init__(self, watcher, name, region):
        self.metadata = watcher.summoner.by_name(region, name)
        self.name = self.metadata['name']
        self.summoner_level = self.metadata['summonerLevel']
        self.match_history = watcher.match.matchlist_by_account(
            region, self.metadata['accountId'])
