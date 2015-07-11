import unittest
import json
import pygame
from serialize import Encoder, Decoder
from environment import Block, SawBlock
from light import Light
from swinginglight import SwingingLight
from constants import TAG_WALL, TAG_GROUND


class SerializeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))
        cls.value = 10
        cls.block1 = Block((0, 0, 0), cls.value, cls.value,
                           cls.value, cls.value, TAG_GROUND)
        cls.block2 = Block((0, 0, 0), cls.value, cls.value,
                           cls.value, cls.value, TAG_WALL)
        cls.saw_block = SawBlock(cls.value, cls.value, cls.value * 10)
        cls.light = Light(cls.value, cls.value, cls.value,
                          [cls.block1, cls.block2])
        cls.swinging_light = SwingingLight(cls.value, cls.value,
                                           cls.value * 10,
                                           [cls.block1, cls.block2])

    def test_encode_block(self):
        block1 = json.dumps(self.block1, cls=Encoder)
        block2 = json.dumps(self.block2, cls=Encoder)

        block_object1 = json.loads(block1, cls=Decoder)
        block_object2 = json.loads(block2, cls=Decoder)

        self.assertEqual(block_object1.x, self.value)
        self.assertEqual(block_object1.y, self.value)
        self.assertEqual(block_object1.width, self.value)
        self.assertEqual(block_object1.height, self.value)
        self.assertEqual(block_object1.tag, TAG_GROUND)
        self.assertEqual(block_object1.colour, [0, 0, 0])

        self.assertEqual(block_object2.x, self.value)
        self.assertEqual(block_object2.y, self.value)
        self.assertEqual(block_object2.width, self.value)
        self.assertEqual(block_object2.height, self.value)
        self.assertEqual(block_object2.tag, TAG_WALL)
        self.assertEqual(block_object2.colour, [0, 0, 0])

    def test_encode_saw_block(self):
        saw_block = json.dumps(self.saw_block, cls=Encoder)

        saw_block_object = json.loads(saw_block, cls=Decoder)

        self.assertEqual(saw_block_object.x, self.value)
        self.assertEqual(saw_block_object.y, self.value)
        self.assertEqual(saw_block_object.rope_height, self.value * 10)

    def test_encode_light(self):
        light = json.dumps(self.light, cls=Encoder)

        light_object = json.loads(light, cls=Decoder)

        self.assertEqual(light_object.x, self.value)
        self.assertEqual(light_object.y, self.value)
        self.assertEqual(light_object.radius, self.value)

    def test_encode_swinging_light(self):
        swinging_light = json.dumps(self.swinging_light, cls=Encoder)

        swingin_light_object = json.loads(swinging_light, cls=Decoder)

        self.assertEqual(swingin_light_object.x, self.value)
        self.assertEqual(swingin_light_object.y, self.value)
        self.assertEqual(swingin_light_object.rope_length, self.value * 10)

if __name__ == '__main__':
    unittest.main()
