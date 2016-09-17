from datetime import date, datetime, timedelta

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
                'proposal': True,
                'cropped': False,
                'plant_date': plant_date,
                'crop_date': crop_date,
                'duration': plant['duration'],
                'plant': plant
            }
            row.append([tile])
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


class Utility:

    date_format = '%d.%m.%Y'

    @staticmethod
    def dates_collide(start1, end1, start2, end2):


        start1 = datetime.strptime(start1, Utility.date_format)
        end1 = datetime.strptime(end1, Utility.date_format)
        start2 = datetime.strptime(start2, Utility.date_format)
        end2 = datetime.strptime(end2, Utility.date_format)

        # Let's order them first
        if start2 > start1:
            tmp_start = start1
            tmp_end = end1
            start1 = start2
            end1 = end2
            start2 = tmp_start
            end2 = tmp_end

        return end1 > start2

    @staticmethod
    def sort_tiles(tiles):
        sorted_tiles = sorted(tiles, key=lambda x: datetime.strptime(x['plant_date'], Utility.date_format))
        return sorted_tiles

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

    def get_watering_events(self, plant):
        """
        Get all the watering events.
        """
        delay_table = {
            'monthly': 28,
            'weekly': 7,
            'daily': 1
        }

        start_date = datetime.strptime(plant['plant_date'], Utility.date_format)
        end_date = datetime.strptime(plant['crop_date'], Utility.date_format)
        delta = timedelta(days=delay_table[plant['plant']['watering']])

        events = []
        next_watering = start_date + delta
        while next_watering < end_date:
            events.append({
                'date': next_watering.strftime(Utility.date_format),
                'title': 'Water %s' % plant['plant']['name']
            })

            next_watering = next_watering + delta

        return events


class Garden:
    """
    A class to represent a garden.
    """

    def __init__(self, data_path='./garden.json'):
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
        new_tiles = []
        for tile in relevant_tiles:
            if not Utility.dates_collide(date, plant_crop_date, tile['plant_date'], tile['crop_date']):
                new_tiles.append(tile)

        # And finally insert the new plant.
        new_tiles.append({
            'plant': plant_info,
            'plant_date': date,
            'crop_date': plant_crop_date,
            'duration': plant_info['duration'],
            'proposal': False,
            'cropped': False
        })
        new_tiles = Utility.sort_tiles(new_tiles)

        self.data['tiles'][x][y] = new_tiles

    def crop(self, x, y, crop_date):
        """
        Crop the currently planted plant at the given location.
        """

        for tile in self.data['tiles'][x][y]:
            if not tile['proposal']:
                tile['cropped'] = True
                tile['crop_date'] = crop_date
                break

    def get_tiles(self, x, y):
        """
        Get all tiles with a specific location.
        """
        return self.data['tiles'][x][y]

    def generate_events(self, date):
        """
        Generate events based on the current garden.
        """

        # Generate events from all plants
        events = []
        for x in range(0, len(self.data['tiles'])):
            row = self.data['tiles'][x]
            for y in range(0, len(row)):
                plants = self.data['tiles'][x][y]
                for tile in plants:

                    # Plant event
                    if tile['proposal']:
                        # Add a plant event
                        events.append({
                            'date': tile['plant_date'],
                            'title': 'Plant %s' % tile['plant']['name'],
                            'location': {
                                'x': x,
                                'y': y
                            }
                        })

                    # Crop event
                    if not tile['proposal'] and not tile['cropped']:
                        events.append({
                            'date': tile['crop_date'],
                            'title': 'Crop %s' % tile['plant']['name'],
                            'location': {
                                'x': x,
                                'y': y
                            }
                        })

                    # Watering events
                    p = Plants()
                    watering_events = p.get_watering_events(tile)
                    # Add the location
                    for i in range(0, len(watering_events)):
                        watering_events[i]['location'] = {
                            'x': x,
                            'y': y
                        }
                    events += watering_events

        # Now we need to consolidate the events such that only one entry per day exists.
        consolidated_events = {}
        for event in events:
            date = event['date']
            if date not in consolidated_events:
                consolidated_events[date] = {
                    'date': date,
                    'tasks': []
                }

            # Add the event
            consolidated_events[date]['tasks'].append({
                'title': event['title'],
                'location': event['location']
            })

        consolidated_events = list(consolidated_events.values())
        consolidated_events.sort(key=lambda e: datetime.strptime(e['date'], Utility.date_format))

        return consolidated_events



