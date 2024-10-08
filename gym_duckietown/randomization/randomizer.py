import json
import numpy as np

from ..utils import *
from .. import logger


class Randomizer:
    def __init__(self, randomization_config_fp='default_dr.json', default_config_fp='default.json'):
        try:
            with open(get_file_path('randomization/config', randomization_config_fp, 'json'), mode='r') as f:
                self.randomization_config = json.load(f)
        except:
            logger.warning("Couldn't find {} in randomization/config subdirectory".format(randomization_config_fp))
            self.randomization_config = dict()

        with open(get_file_path('randomization/config', default_config_fp, 'json'), mode='r') as f:
            self.default_config = json.load(f)

        self.keys = set(list(self.randomization_config.keys()) + list(self.default_config.keys()))
        
    def randomize(self):
        """Returns a dictionary of randomized parameters, with key: parameter name and value: randomized
        value
        """
        randomization_settings = dict()
        
        for k in self.keys:
            setting = None
            if k in self.randomization_config:
                randomization_definition = self.randomization_config[k]
                
                if randomization_definition['type'] == 'int':
                    try:
                        low = randomization_definition['low']
                        high = randomization_definition['high']
                        size = randomization_definition.get('size', 1)
                    except:
                        raise IndexError("Please check your randomization definition for: {}".format(k))

                    setting = np.random.randint(low=low, high=high, size=size)

                elif randomization_definition['type'] == 'uniform':
                    try:
                        low = randomization_definition['low']
                        high = randomization_definition['high']
                        size = randomization_definition.get('size', 1)
                    except:
                        raise IndexError("Please check your randomization definition for: {}".format(k))

                    setting = np.random.uniform(low=low, high=high, size=size)

                elif randomization_definition['type'] == 'normal':
                    try:
                        loc = randomization_definition['loc']
                        scale = randomization_definition['scale']
                        size = randomization_definition.get('size', 1)
                    except:
                        raise IndexError("Please check your randomization definition for: {}".format(k))

                    setting = np.random.normal(loc=loc, scale=scale, size=size)

                else:
                    raise NotImplementedError("You've specified an unsupported distribution type")

            elif k in self.default_config:
                randomization_definition = self.default_config[k]
                setting = randomization_definition['default']

            randomization_settings[k] = setting

        return randomization_settings
