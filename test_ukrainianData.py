from unittest import TestCase
from ukrainian_data_adt import UkrainianData


class TestUkrainianData(TestCase):

    def setUp(self) -> None:
        self.migration_data = UkrainianData("338a8ccf-8b77-476b-b138-9bb5b7550584")

    def test_get_value(self):
        self.assertEqual(self.migration_data.get_value('м. Севастополь***', 'Число прибулих 2010'), 5266)
        with self.assertRaises(KeyError):
            self.migration_data.get_value('Неіснуюче місто', 'Число прибулих 2010')

    def test_get_row(self):
        self.assertEqual(self.migration_data.get_row("м. Севастополь***"),
                         {'Число прибулих 2010': 5266, 'Число вибулих 2010': 3490,
                          'Міграційний приріст, скорочення (-) населення 2010': 1776, 'Число прибулих 2011': 5053,
                          'Число вибулих 2011': 3501, 'Міграційний приріст, скорочення (-) населення 2011': 1552,
                          'Число прибулих 2012': 6433, 'Число вибулих 2012': 3562,
                          'Міграційний приріст, скорочення (-) населення 2012': 2871, 'Число прибулих 2013': 6614,
                          'Число вибулих  2013': 3318, 'Міграційний приріст, скорочення (-) населення 2013': 3296,
                          'Число прибулих 2014': None, 'Число вибулих 2014': None,
                          'Міграційний приріст, скорочення (-) населення 2014': None, 'Число прибулих 2015': None,
                          'Число вибулих 2015': None, 'Міграційний приріст, скорочення (-) населення 2015': None,
                          'Число прибулих 2016': None, 'Число вибулих 2016': None,
                          'Міграційний приріст, скорочення (-) населення  2016': None, 'Число прибулих 2017': None,
                          'Число вибулих 2017': None, 'Міграційний приріст, скорочення (-) населення  2017': None})
        with self.assertRaises(KeyError):
            self.migration_data.get_row("Неіснуюче місто")

    def test_get_column(self):
        self.assertEqual(self.migration_data.get_column("Число прибулих 2010"),
                         {'Україна': 683449, 'Україна*': 647927, 'Автономна Республіка Крим': 30256, 'Вінницька': 30682,
                          'Волинська': 17718, 'Дніпропетровська': 46437, 'Донецька**': 58195, 'Житомирська': 23543,
                          'Закарпатська': 8456, 'Запорізька': 23639, 'Івано-Франківська': 17170, 'Київська': 27815,
                          'Кіровоградська': 17114, 'Луганська**': 32535, 'Львівська': 31857, 'Миколаївська': 15354,
                          'Одеська': 37958, 'Полтавська': 25189, 'Рівненська': 19551, 'Сумська': 21385,
                          'Тернопільська': 14217, 'Харківська': 44096, 'Херсонська': 15063, 'Хмельницька': 23065,
                          'Черкаська': 21205, 'Чернівецька': 10805, 'Чернігівська': 18286, 'м. Київ': 46592,
                          'м. Севастополь***': 5266})
        with self.assertRaises(KeyError):
            self.migration_data.get_column("Неіснуюча колонка")

    def test_correlation_index(self):
        self.assertEqual(UkrainianData.correlation_index(
                                        list(self.migration_data.get_column("Число прибулих 2010").values()),
                                        list(self.migration_data.get_column("Число прибулих 2012").values())).tolist(),
                                        [[1.0, 0.9997480282827755], [0.9997480282827754, 1.0]])

    def test_show_change_plot(self):
        self.assertEqual(self.migration_data.show_change_plot("Вінницька", "Число прибулих"), None)

    def test__rgb_to_hex(self):
        self.assertEqual(self.migration_data._rgb_to_hex((12, 125, 0)), "#0c7d00")

    def test_show_data(self):
        self.assertIsNone(self.migration_data.show_data())

    def test__get_needed_colour(self):
        self.assertEqual(self.migration_data._get_needed_colour(125, 150), "#2b2bff")



