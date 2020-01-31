from functools import reduce

import confuse

config = confuse.Configuration('SleepCycleWebhooks')
config.set_file('config.yaml')


def get(path):
    return reduce(lambda view, part: view[part], path.split('.'), config).get()
