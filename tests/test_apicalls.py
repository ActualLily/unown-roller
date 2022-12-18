from unittest import TestCase

import database.apicalls


class Test(TestCase):
    def test_getpokemon(self):
        self.assertEqual(database.apicalls.getpokemon("bulbasaur").id, 1)
        self.assertEqual(database.apicalls.getpokemon(1).name, "bulbasaur")

    def test_getspecies(self):
        self.assertEqual(database.apicalls.getspecies(1).color.name, "green")
        self.assertEqual(database.apicalls.getspecies("bulbasaur").gender_rate, 1)
