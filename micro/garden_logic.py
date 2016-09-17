from datetime import date, datetime

from flask import json
import random


def create_garden(width, height, path):
    """
    Create a new garden. I.e. fill it with proposals.
    :param width: Width of the garden in tiles.
    :param height: Height of the garden in tiles.
    :param path: The path where to store the created file.
    """
    plants = Plants()

    # First version selects for each tile a random plant.
    tiles = []

    for h in range(0, height):
        row = []
        for w in range(0, width):
            plant = plants.get_plant(4)
            (plant_date, crop_date) = plants.get_plant_and_crop_date(plant)
            tile = {
                'location': {
                    'x': w,
                    'y': h
                },
                'proposal': True,
                'plant_date': plant_date,
                'crop_date': crop_date,
                'duration': plant['duration'],
                'plant': plant
            }
            row.append(tile)
        tiles.append(row)

    data = {
        'size': {
            'width': width,
            'height': height
        },
        'tiles': tiles
    }

    # Write it to the given path
    with open(path, 'w') as f:
        json.dump(data, f)


def update_garden(path, x, y):
    """
    Update the given garden with new proposals.
    X and Y show the location that should be updated.
    :param path: The path where the garden is stored.
    """
    pass

class Utility:

    date_format = '%d.%m.%Y'

    @staticmethod
    def dates_collide(start1, end1, start2, end2):

        start1 = datetime.strptime(Utility.date_format, start1)
        end1 = datetime.strptime(Utility.date_format, end1)
        start2 = datetime.strptime(Utility.date_format, start2)
        end2 = datetime.strptime(Utility.date_format, end2)

        # Let's order them first
        if start2 > start1:
            tmp_start = start1
            tmp_end = end1
            start1 = start2
            end1 = end2
            start2 = tmp_start
            end2 = tmp_end

        return end1 > start2


class Garden:
    """
    A class to represent a garden.
    """

    def __init__(self, data_path):
        self.data_path = data_path
        with open(data_path) as f:
            self.data = json.load(f)

    def save(self):
        with open(self.data_path, 'w') as f:
            json.dump(self.data, f)

    def plant(self, x, y, plant_name, date):
        """
        Plant a plant at a given location and date.
        """
        plants = Plants()
        plant_info = plants.get_complete_info(plant_name)
        plant_crop_date = plants.get_crop_date(plant_info, date)

        # Remove all plants during that time frame.
        relevant_tiles = self.get_tiles(x, y)
        # Check if these tiles collide with the new planted plant.
        for tile in relevant_tiles:
            if Utility.dates_collide(date, plant_crop_date, tile['plant_date'], tile['crop_date']):
                self.data['tiles'].remove(tile)

        # And finally insert the new plant.
        self.data['tiles'].append({
                'location': {
                    'x': x,
                    'y': y
                },
                'plant': plant_info,
                'plant_date': date,
                'crop_date': plant_crop_date,
                'duration': plant_info['duration'],
                'proposal': False
            })

    def get_tiles(self, x, y):
        """
        Get all tiles with a specific location.
        """
        valid_tiles = filter(lambda tile: tile['location']['x'] == x and tile['location']['y'] == y, self.data['tiles'])
        return list(valid_tiles)


class Plants:
    """
    A class to simply access plants.
    """

    def __init__(self):
        with open('data/plants.json') as f:
            self.data = json.load(f)
            self.plants = self.data['plants']

    def get_plant(self, plant_month, max_duration=0):
        """
        Returns a random plant that can be planted within the given month. If max_duration is bigger than
        zero than a plant is returned that has a duration smaller or equal to max_duration.
        """
        valid_plants = filter(lambda x: plant_month in x['plant'], self.plants)

        # Filter again if a max_duration is given.
        if max_duration > 0:
            valid_plants = filter(lambda x: x['duration'] <= max_duration)

        return random.choice(list(valid_plants))

    def get_complete_info(self, plant_name):
        valid_plants = filter(lambda x: x['name'] == plant_name, self.plants)
        return list(valid_plants)[0]

    def get_plant_and_crop_date(self, plant):
        """
        Get a (random) plant and crop date for the given plant.
        :param plant:
        :return:
        """
        plant_day = random.randint(1, 28)
        plant_month = random.choice(plant['plant'])
        plant_date = '%.2d.%.2d.2016' % (plant_day, plant_month)

        crop_date = self.get_crop_date(plant, plant_date)

        return plant_date, crop_date

    def get_crop_date(self, plant, plant_date):

        day, month, year = plant_date.split('.')

        # Calculate crop date
        crop_day_total = int(day) + plant['duration'] * 7
        crop_day = crop_day_total % 28
        crop_months = int(month) + (crop_day_total - crop_day) / 28
        crop_date = '%.2d.%.2d.2016' % (crop_day, crop_months)
        return crop_date

