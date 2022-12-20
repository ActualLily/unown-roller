from unittest import TestCase

import database.connectionhandler


class Test(TestCase):

    def test_fetchhorizontal_blank(self):
        data = database.connectionhandler.fetchhorizontal("pokemon", filter="name = 'pikablu'")
        self.assertIsNone(data)#

    def test_fetchhorizontal_group(self):
        data = database.connectionhandler.fetchhorizontal("pokemon", filter="name = 'bulbasaur'")
        expected = {'pokedex': 1, 'name': 'bulbasaur', 'form': '', 'page': '90', 'rank': 2, 'type1': 'grass', 'type2': 'poison',
         'ability1': 'overgrow', 'ability2': None, 'moves': None, 'descriptor': 'Seed Pokémon', 'hp': 3, 'str': 2,
         'strmax': 4, 'dex': 2, 'dexmax': 4, 'vit': 2, 'vitmax': 4, 'spe': 2, 'spemax': 4, 'ins': 2, 'insmax': 4,
         'evostage': 'First', 'evospeed': 'Medium'}

        self.assertEqual(data, expected)

    def test_fetchhorizontal_filtered(self):
        data = database.connectionhandler.fetchhorizontal("pokemon", "pokedex, name", "pokedex = 1")
        expected = {'pokedex': 1, 'name': 'bulbasaur'}

        self.assertEqual(data, expected)

    def test_fetchvertical_blank(self):
        data = database.connectionhandler.fetchvertical("types", filter="type = 'void'")
        self.assertIsNone(data)

    def test_fetchvertical(self):
        data = database.connectionhandler.fetchvertical("types", "type")
        expected = ['bug', 'dark', 'dragon', 'electric', 'fairy', 'fight', 'fire', 'flying', 'ghost', 'grass', 'ground', 'ice', 'normal', 'poison', 'psychic', 'rock', 'steel', 'water']

        self.assertEqual(data, expected)

    def test_hasperms(self):
        # Check if Leah#0004 has permissions
        self.assertTrue(database.connectionhandler.hasperms(128942926922383360))
