import json
from Environment import *
from Constants import *
from Light import Light
from Settings import Settings

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Block):
            return {"type": OBJECT_BLOCK,
                    "colour": obj.colour,
                    "width": obj.width,
                    "height": obj.height,
                    "x": obj.x,
                    "y": obj.y,
                    "tag": obj.tag}
        elif isinstance(obj, SawBlock):
            return {"type": OBJECT_SAW_BLOCK,
                    "x": obj.x,
                    "y": obj.y,
                    "length": obj.rope_height}
        elif isinstance(obj, Light):
            return {"type": OBJECT_LIGHT,
                    "x": obj.x,
                    "y": obj.y,
                    "radius": obj.radius}
        elif isinstance(obj, Settings):
            return {"type": OBJECT_SETTINGS,
                    "level_width": obj.width,
                    "level_height": obj.height,
                    "music": obj.music,
                    "start_position": obj.start_position}

class Decoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.deserialize)

    def deserialize(self, d):
        if d["type"] == OBJECT_BLOCK:
            return Block(d["colour"], d["width"], d["height"], d["x"], d["y"], d["tag"])
        elif d["type"] == OBJECT_SAW_BLOCK:
            return SawBlock(d["x"], d["y"], d["length"])
        elif d["type"] == OBJECT_LIGHT:
            return Light(d["x"], d["y"], d["radius"])
        elif d["type"] == OBJECT_SETTINGS:
            return Settings(d["level_width"], d["level_height"], d["music"], d["start_position"])

