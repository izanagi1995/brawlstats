import asynctest
import asyncio
import datetime
import os

import brawlstats
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('../.env'))

TOKEN = os.getenv('unofficial_token')


class TestAsyncClient(asynctest.TestCase):
    """Tests all methods in the asynchronous BrawlAPI client that
    uses the `aiohttp` module in `brawlstats`
    """
    async def setUp(self):
        self.player_tag = 'GGJVJLU2'
        self.club_tag = 'QCGV8PG'
        self.client = brawlstats.BrawlAPI(
            TOKEN,
            is_async=True,
            timeout=30
        )

    async def tearDown(self):
        await asyncio.sleep(1)
        await self.client.close()

    async def test_get_player(self):
        player = await self.client.get_player(self.player_tag)
        self.assertEqual(player.tag, self.player_tag)

    async def test_get_club(self):
        club = await self.client.get_club(self.club_tag)
        self.assertEqual(club.tag, self.club_tag)

    async def test_get_leaderboard_player(self):
        lb = await self.client.get_leaderboard('players')
        self.assertTrue(isinstance(lb, brawlstats.brawlapi.Leaderboard))
        region = await self.client.get_leaderboard('players', region='us')
        self.assertTrue(isinstance(region, brawlstats.brawlapi.Leaderboard))

    async def test_get_leaderboard_club(self):
        lb = await self.client.get_leaderboard('clubs')
        self.assertTrue(isinstance(lb, brawlstats.brawlapi.Leaderboard))

    async def test_get_leaderboard_brawler(self):
        lb = await self.client.get_leaderboard('brawlers', brawler='shelly')
        self.assertTrue(isinstance(lb, brawlstats.brawlapi.Leaderboard))

    async def test_get_events(self):
        events = await self.client.get_events()
        self.assertTrue(isinstance(events.current, list))

    async def test_get_constants(self):
        default = await self.client.get_constants()
        self.assertTrue(isinstance(default, brawlstats.brawlapi.Constants))
        maps = await self.client.get_constants('maps')
        self.assertTrue(isinstance(maps, brawlstats.brawlapi.Constants))

        async def request():
            await self.get_constants(invalid_key)
        invalid_key = 'invalid'
        self.assertAsyncRaises(KeyError, request)

    async def test_get_misc(self):
        misc = await self.client.get_misc()
        self.assertEqual(misc.server_date_year, datetime.date.today().year)

    async def test_club_search(self):
        search = await self.client.search_club('Cactus Bandits')
        self.assertTrue(isinstance(search, list))

    async def test_battle_logs(self):
        logs = await self.client.get_battle_logs(self.player_tag)
        self.assertTrue(isinstance(logs, brawlstats.brawlapi.BattleLog))

    # Other
    async def test_invalid_tag(self):
        async def request():
            await self.client.get_player(invalid_tag)
        invalid_tag = 'P'
        self.assertAsyncRaises(brawlstats.NotFoundError, request)
        invalid_tag = 'AAA'
        self.assertAsyncRaises(brawlstats.NotFoundError, request)
        invalid_tag = '2PPPPPPP'
        self.assertAsyncRaises(brawlstats.ServerError, request)

    async def test_invalid_lb(self):
        async def request():
            await self.client.get_leaderboard(invalid_type, invalid_limit)
        invalid_type = 'test'
        invalid_limit = 200
        self.assertAsyncRaises(ValueError, request)
        invalid_type = 'players'
        invalid_limit = 201
        self.assertAsyncRaises(ValueError, request)
        invalid_type = 'players'
        invalid_limit = -5
        self.assertAsyncRaises(ValueError, request)


if __name__ == '__main__':
    asynctest.main()