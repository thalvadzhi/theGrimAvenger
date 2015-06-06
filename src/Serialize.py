import json
from Environment import *
from Constants import *
from Light import Light

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
                    "radius": obj.radius,
                    "screen_x": obj.screen_x,
                    "screen_y": obj.screen_y}

class Decoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.deserialize)

    def deserialize(self, d):
        if d["type"] == OBJECT_BLOCK:
            return Block(d["colour"], d["width"], d["height"], d["x"], d["y"], d["tag"])
        elif d["type"] == OBJECT_SAW_BLOCK:
            return SawBlock(d["x"], d["y"], d["length"])
        elif d["type"] == OBJECT_LIGHT:
            return Light(d["x"], d["y"], d["radius"], d["screen_x"], d["screen_y"])
