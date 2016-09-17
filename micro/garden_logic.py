from datetime import date, datetime, timedelta
from tkinter import W

from flask import json
import random

from wheater import Wheater


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
        plant = plants.get_plant(4)
        for w in range(0, width):
            (plant_date, crop_date) = plants.get_plant_and_crop_date(plant)
            tile = {
                'state': 'suggestion',
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

    garden = Garden()
    garden.add_suggestions()
    garden.save()


class Utility:

    date_format = '%Y-%m-%d'

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

        valid_plants = list(valid_plants)
        if len(valid_plants) > 0:
            return random.choice(valid_plants)
        else:
            return None

    def get_follow_plant(self, tile):
        """
        Tries to find a plant that follows to the given tile.
        """
        harvest_date = tile['crop_date']
        day, month, year = harvest_date.split('-')
        month = int(month) + 1
        return self.get_plant(month)


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
        plant_date = datetime(year=2016, month=int(plant_month), day=int(plant_day)).strftime(Utility.date_format)

        crop_date = self.get_crop_date(plant, plant_date)

        return plant_date, crop_date

    def get_crop_date(self, plant, plant_date):

        day, month, year = plant_date.split('-')

        # Calculate crop date
        crop_day_total = int(day) + plant['duration'] * 7
        crop_day = crop_day_total % 28 + 1
        crop_months = int(month) + (crop_day_total - crop_day) / 28
        crop_year = 2016
        if crop_months > 12:
            crop_year += 1
            crop_months = (crop_months % 12) + 1
        crop_date = datetime(year=int(crop_year), month=int(crop_months), day=int(crop_day))
        return crop_date.strftime(Utility.date_format)

    def get_watering_events(self, plant):
        """
        Get all the watering events.
        """

        # We want the watering events only if it is scheduled.
        if plant['state'] not in ['scheduled', 'in_progress']:
            return []

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
                'title': 'Water %s' % plant['plant']['name'],
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

    def update_state(self, x, y, z, new_state):
        self.data['tiles'][x][y][z]['state'] = new_state

    def get_tiles(self, x, y):
        """
        Get all tiles with a specific location.
        """
        return self.data['tiles'][x][y]

    def add_suggestions(self):
        p = Plants()
        for x in range(0, len(self.data['tiles'])):
            row = self.data['tiles'][x]
            for y in range(0, len(row)):
                plants = self.data['tiles'][x][y]
                last_plant = plants[-1]

                # Try to find a plant that grows after this one.
                follow_plant = p.get_follow_plant(last_plant)
                if follow_plant is not None:
                    plant_date, crop_date = p.get_plant_and_crop_date(follow_plant)
                    self.data['tiles'][x][y].append({
                        'state': 'suggestion',
                        'plant_date': plant_date,
                        'crop_date': crop_date,
                        'duration': follow_plant['duration'],
                        'plant': follow_plant
                    })


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
                    if tile['state'] == 'scheduled':
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
                    if tile['state'] in ['scheduled', 'in_progress', 'ready_to_harvest']:
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
            d = event['date']
            if d not in consolidated_events:
                consolidated_events[d] = {
                    'date': d,
                    'tasks': []
                }

            # Add the event
            consolidated_events[d]['tasks'].append({
                'title': event['title'],
                'location': event['location']
            })

        consolidated_events = list(consolidated_events.values())
        consolidated_events.sort(key=lambda e: datetime.strptime(e['date'], Utility.date_format))

        # Filter the events. We want only events after the given date.
        filter_date = datetime.strptime(date, Utility.date_format)
        final_events = list(filter(lambda e: datetime.strptime(e['date'], Utility.date_format) >= filter_date, consolidated_events))

        # Add weather data to the next 10 days.
        weather = Wheater()
        rain = weather.get_rain_prediction()
        today = datetime.now()
        day = timedelta(days=1)
        next_10_days = []
        for i in range(0, 10):
            next_10_days.append((today + i*day).strftime(Utility.date_format))

        print(next_10_days)

        for i in range(0, 10):
            event = final_events[i]
            print(event['date'])

            for k in range(0, 10):
                if event['date'] == next_10_days[k]:
                    event['rain_amount'] = rain[k]

        return final_events



