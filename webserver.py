import json

import flask
import config
from webhooks import Webhooks

app = flask.Flask(__name__)


def run():
    ip = config.get('network.listen_ip')
    port = config.get('network.http_port')

    print("Starting Flask on {0}:{1}...".format(ip, port))

    app.run(host=ip, port=port, threaded=True, use_reloader=False)


DUMMY_LIGHT = {
    'state': {
        'on': False,
        'bri': 0,
        'hue': 0,
        'sat': 0,
        'effect': 'none',
        'ct': 0,
        'alert': 'none',
        'reachable': True
    },
    'type': 'Dimmable light',
    'name': "Webhook Dummy Light",
    'modelid': 'LWB004',
    'manufacturername': 'Philips',
    'uniqueid': 123,
    'swversion': '66012040'
}

DUMMY_LIGHTS = {DUMMY_LIGHT['uniqueid']: DUMMY_LIGHT}

DUMMY_CONFIG = {
    'name': 'HA-Echo',
    'mac': '00:00:47:11:bb:ee',
    'dhcp': True,
    'ipaddress': config.get('network.listen_ip'),
    'netmask': '255.255.255.0',
    'gateway': '0.0.0.0',
    'proxyaddress': '',
    'proxyport': 0,
    'swversion': '01003372',
    'swupdate': {
        'updatestate': 0,
        'url': '',
        'text': '',
        'notify': False
    },
    'linkbutton': False,
    'portalservices': False
}


@app.route('/description.xml', strict_slashes=False, methods=['GET'])
def hue_description_xml():
    with open('resources/description.xml', 'r') as file:
        return flask.Response(
            file.read().format(config.get('network.listen_ip'), config.get('network.http_port')),
            mimetype='text/xml'
        )


@app.route('/api/<token>/lights', strict_slashes=False, methods=['GET'])
def hue_api_lights(token):
    return flask.Response(json.dumps(DUMMY_LIGHTS), mimetype='application/json')


@app.route('/api/<token>/lights/<int:id_num>', strict_slashes=False, methods=['GET'])
def hue_api_individual_light(token, id_num):
    return flask.Response(json.dumps(DUMMY_LIGHTS[id_num]), mimetype='application/json')


@app.route('/api/<token>', strict_slashes=False, methods=['GET'])
def hue_api_full_config(token):
    return flask.Response(json.dumps({'lights': DUMMY_LIGHTS, 'config': DUMMY_CONFIG}), mimetype='application/json')


@app.route('/api/<token>/lights/<int:id_num>/state', methods=['PUT'])
def hue_api_put_light(token, id_num):
    request_json = flask.request.get_json(force=True)
    print("PUT {0}/state: {1}".format(id_num, request_json))

    # Turn on
    if 'on' in request_json and request_json['on']:
        Webhooks.on()

        return flask.Response(json.dumps([{'success': {'/lights/{0}/state/on'.format(id_num): True}}]),
                              mimetype='application/json', status=200)

    # Turn off
    if 'on' in request_json and not request_json['on']:
        Webhooks.off()

        return flask.Response(json.dumps([{'success': {'/lights/{0}/state/on'.format(id_num): False}}]),
                              mimetype='application/json', status=200)

    # Change brightness
    if 'bri' in request_json:
        Webhooks.change_brightness(request_json['bri'])

        return flask.Response(json.dumps([{'success': {'/lights/{0}/state/bri': request_json['bri']}}]),
                              mimetype='application/json', status=200)

    print("Unhandled API request: {0}".format(request_json))
    flask.abort(500)


@app.route('/api/<token>/groups', strict_slashes=False)
@app.route('/api/<token>/groups/0', strict_slashes=False)
def hue_api_groups_0(token):
    print("ERROR: If /api/groups is requested it usually means it failed to parse /api/lights.")
    return flask.abort(500)


@app.route('/api/', strict_slashes=False, methods=['POST'])
def hue_api_create_user():
    """
    Assign a dummy username when it is requested.
    """
    request_json = flask.request.get_json(force=True)

    if 'devicetype' not in request_json:
        return flask.abort(500)

    return flask.Response(json.dumps([{'success': {'username': '12345678901234567890'}}]), mimetype='application/json')


@app.route('/api/(null)', strict_slashes=False, methods=['GET'])
@app.route('/api', strict_slashes=False, methods=['GET'])
def hue_api_create_user_null():
    """
    Assign a dummy username when it is requested.
    """
    return flask.Response(json.dumps([{'success': {'username': '12345678901234567890'}}]), mimetype='application/json')
