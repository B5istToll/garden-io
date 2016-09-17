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


def update_garden(path):
    """
    Update the given garden with new proposals.
    :param path: The path where the garden is stored.
    """
    pass


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


    def get_plant_and_crop_date(self, plant):
        """
        Get a (random) plant and crop date for the given plant.
        :param plant:
        :return:
        """
        plant_day = random.randint(1, 28)
        plant_month = random.choice(plant['plant'])
        plant_date = '%.2d.%.2d.2016' % (plant_day, plant_month)

        # Calculate crop date
        crop_day_total = plant_day + plant['duration'] * 7
        crop_day = crop_day_total % 28
        crop_months = plant_month + (crop_day_total - crop_day) / 28
        crop_date = '%.2d.%.2d.2016' % (crop_day, crop_months)

        return (plant_date, crop_date)

