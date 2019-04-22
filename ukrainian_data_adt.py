import requests
import json
from io import StringIO
import csv
import numpy as np
import matplotlib.pyplot as plt
import folium
import geocoder
from transliterate import translit


class UkrainianData:
    """
    Class developed to improve user experience of working with data.gov.ua datasets (particularly on migration)

    Recommendations:
    After initializing object instance highly recommended to call
    print(obj.column_names)
    or
    obj.show_data()
    print(obj.explanation)
    To understand the dataset you are working with and what keys it supports
    """

    def __init__(self, package_id):
        """
        :param package_id: id of dataset on data.gov.ua.
        """
        # data is a dict of dicts
        # explanation is a string
        data_list = self._get_data(package_id)
        self._data, self.explanation = self._build_data_dict(data_list)
        self.column_names = data_list[0][1:]
        self.row_names = [row[0] for row in data_list[1:] if not row[0].startswith("*")]

    @staticmethod
    def _build_data_dict(data_list):
        """
        Processes data_list to make it useful for our object
        :param data_list: output of _get_data method
        :return: data in dictionary, string with explanations to the data
        """
        data_dict = {}
        keys = data_list[0][1:]
        explanations = []
        for row in data_list[1:]:
            if row[0].startswith("*"):
                explanations.append(row[0])
            else:
                for ind, value in enumerate(row[1:]):
                    try:
                        value = int(value)
                    except ValueError:
                        value = None
                    if row[0] in data_dict.keys():
                        data_dict[row[0]][keys[ind]] = value
                    else:
                        data_dict[row[0]] = {keys[ind]:value}

        return data_dict, "\n".join(explanations)

    @staticmethod
    def _get_data(package_id):
        """
        retrieve dataset from data.gov.ua
        :param package_id: id of dataset on data.gov.ua.
        example: 338a8ccf-8b77-476b-b138-9bb5b7550584 - id of dataset on migration
        :return: list of lists containing rows of csv file
        """
        DATASET_URL = "https://data.gov.ua/api/3/action/package_show?"
        BASE_REQUEST_URL = "https://data.gov.ua/api/3/action/resource_show?"
        params_package = {'id': package_id}
        # r, r2, r3, req - chain of requests recieved from data.gov.ua to get dataset. No need to get in details

        r = requests.get(url=DATASET_URL, params=params_package)

        req = json.loads(r.text)

        resource_id = req['result']['resources'][-1]['id']
        params_dataset = {'id': resource_id}

        r2 = requests.get(url=BASE_REQUEST_URL, params=params_dataset)

        req2 = json.loads(r2.text)

        dataset_link = req2['result']['url']
        r3 = requests.get(dataset_link)

        data = []
        fstream = StringIO(r3.text)

        reader = csv.reader(fstream, delimiter=',')
        for row in reader:
            data.append(row)

        return data

    def show_data(self):
        """
        Shows _data as stored in object
        :return:
        """
        print(self._data)

    def get_value(self, row_name, col_name):
        """

        :param row_name: string - name of row as given in dataset
        :param col_name: string - name of column as given in dataset
        :return:
        """
        try:
            return self._data[row_name][col_name]
        except KeyError:
            raise KeyError("The position you request is not available / Typo parameters")

    def get_row(self, row_name):
        """
        Returns all values in requested row
        :param row_name: string - name of row as given in dataset
        :return: dictionary
        """
        return self._data[row_name]

    def get_column(self, col_name):
        """
        Returns all values in requested column
        :param column_name: string - name of column as given in dataset
        :return: dictionary
        """
        column_dict = {}
        for key in self._data.keys():
            column_dict[key] = self._data[key][col_name]
        return column_dict

    @staticmethod
    def correlation_index(values1, values2):
        """
        Pearson correlation coefficient
        :param values1: list
        :param values2: list
        :return: matrix
        """
        try:
            return np.corrcoef(values1, values2)
        except TypeError:
            raise ValueError("Some data points you are trying to correlate may be unavailable (None)")

    def show_change_plot(self, row_name, param):
        """
        Shows plot representing change of certain parameter in certain region(row_name) in time
        :param row_name: string - name of row as given in dataset
        :param param: name of column or part of it as given in dataset (example: Число прибулих)
        :return: None
        """
        needed_columns = [col for col in self.column_names if param in col]
        if not needed_columns:
            raise ValueError("param for plotting is not available")
        else:
            values_to_plot = [self.get_value(row_name, col) for col in needed_columns]
            if not values_to_plot:
                raise ValueError("row_name for plotting is not available")
            else:
                # if value is None, don't plot it
                needed_columns = [needed_columns[ind] for ind, val in enumerate(values_to_plot) if val is not None]
                values_to_plot = [val for val in values_to_plot if val is not None]

                x = np.arange(len(needed_columns))
                plt.bar(needed_columns, height=values_to_plot)
                plt.xticks(x, needed_columns, fontsize=7, rotation=15)
                plt.legend([row_name])
                plt.show()

    def get_map(self, param, year):
        """
        returns map visualizing how a particular parameter is different in different regions of Ukraine
        :param param: string with parameter name to map (example: Число прибулих)
        :param year: year information for which to map
        :return: string with html
        """
        column = [col for col in self.column_names if param in col and str(year) in col][0]
        values_dict = self.get_column(column)
        return self.generate_map(values_dict, column)

    @staticmethod
    def _rgb_to_hex(rgb):
        '''
        method used to give proper colours on map
        The higher the value of parameter, the more intensive the colour is
        :param rgb: tuple
        :return: str
        '''
        return '#%02x%02x%02x' % rgb

    @staticmethod
    def _get_needed_colour(value, max_value):
        """
        The higher the value of parameter, the more intensive the colour is
        :param value: number
        :param max_value: number
        :return: string representing colour
        """
        new_value = int(value / max_value * 255)
        return '#%02x%02x%02x' % (255 - new_value, 255 - new_value, 255)

    @staticmethod
    def generate_map(value_dict, param):
        """
        :param value_dict: key - Ukraine region val - number
        :return: string with html-map
        """

        map_ua = folium.Map()
        fg = folium.FeatureGroup(name="Map of Ukraine :" + translit(param, "ru", reversed=True))
        print("Generating a map...")
        max_value = max(list(value_dict.values())[3:])
        for key in value_dict.keys():
            if value_dict[key]:
                # folium doesn't support Ukrainian, so here transliteration is used
                fg.add_child(folium.CircleMarker(location=geocoder.arcgis(key.replace("*", "")
                                                                          + " область, Україна").latlng,
                                                 radius=10,
                                                 popup=translit(key, "ru", reversed=True)
                                                       + " : " + str(value_dict[key]),
                                                 fill_color=UkrainianData._get_needed_colour(value_dict[key],
                                                                                             max_value),
                                                 color=UkrainianData._get_needed_colour(value_dict[key],
                                                                                        max_value),
                                                 fill_opacity=1.0))
        map_ua.add_child(fg)
        map_ua.add_child(folium.LayerControl())
        return map_ua.get_root().render()

