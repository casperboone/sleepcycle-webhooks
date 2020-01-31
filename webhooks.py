from requests import request

import config


class Webhooks:
    @staticmethod
    def on():
        request(config.get('webhooks.turn_on.method'), config.get('webhooks.turn_on.url'))

    @staticmethod
    def off():
        request(config.get('webhooks.turn_off.method'), config.get('webhooks.turn_off.url'))

    @staticmethod
    def change_brightness(brightness):
        request(
            config.get('webhooks.set_brightness.method'),
            config.get('webhooks.set_brightness.url'),
            params={config.get('webhooks.set_brightness.brightness_parameter_name'): brightness},
            data={config.get('webhooks.set_brightness.brightness_parameter_name'): brightness}
        )
