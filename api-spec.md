# API Spec

This document describes what the API endpoints should look like once they are implemented. 

## GET `/garden` 

Get the current state of the garden. If a tile is empty there will be no tile object for it. It is also possible that there are multiple tile objects with the same location. They will have non overlapping plant and crop dates. 

        {
            "size": {
                "width": 5, 
                "height": 4
            }, 
            "tiles": [
                {
                    "location": {
                        "x": 0, 
                        "y": 0
                    }, 
                    "plant": {
                        "name": "Rhabarber",
                        "type": "Ausdauernde Gemüsearten"
                    },
                    "plant_date": "03.03.2016",
                    "crop_date": "03.05.2016",
                    "duration": 8,
                    "proposal": true
                }
            ]
        }

- `size`: The size of the garden in tiles. Size of a tile is irrelevant (at the moment). Let's say it is 1 square meter. 
- `tiles`: An array of tiles. For each location there can exists multiple tiles with non overlapping plant and crop dates. 
- `tiles.location`: The location of this tile. The coordinates are in 0..<size.x and 0..<size.y respectively. 
- `tiles.plant`: What plant is plannted at this tile. 
- `tiles.plant_date`: The date when this plant was planted.
- `tiles.crop_date`: The estimated crop date based on the duration and plant_date. 
- `tiles.duration`: The duration that is planned that the plant needs to grow. 
- `tiles.proposal`: Wheter this tile is proposal or if it is already confirmed by the user. 