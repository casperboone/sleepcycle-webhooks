# SleepCycle webhooks via Hue emulation

A small application that emulates a Hue bridge for SleepCycle to communicate with.
Incoming requests from SleepCycles are sent out to user-specified webhooks.

The code is written to work with SleepCycle, however, it is likely that it will also work with other software or devices that connect with Hue bridges.

For a large part, the code is based on earlier work by [Magicus](https://github.com/magicus/ha-local-echo) and [blocke](git@github.com:blocke/ha-local-echo.git).
This application is a generalization and partial rewrite of their implementation for [Home Assistant](https://www.home-assistant.io/).

## Installation

It is assumed that you already have a working Python 3 installation.
We also assume that Python and pip are available using `python` and `pip`.
Note that for some Python 3 installations this might be `python3` and `pip3`.

The first step is to install the dependencies using: 
```
$ pip install -r requirements.txt
```

Now copy `config_example.yaml` to `config.yaml`, and enter the required configuration options.
Note that using port 80 is required for SleepCycle to find the emulator.
You might first want to check if this port is already in use for a local webserver.


## Usage

After the [installation](#installation), you can start the emulator by running: 
```
python emulator.py
```
(note that running on port 80 requires root access on some platforms, prepend the command with `sudo` if that is the case)

You should now be able to find the emulated Hue bridge in the SleepCycle app.
Select the `Webhook Dummy Light` light.
When you start your alarm clock, you should now see an incoming "turn off" request being logged.

## SleepCycle behavior

SleepCycle calls the configured webhooks at the moments described below.

* **Set alarm** After setting your alarm, SleepCycle will turn off the dummy light (and thus call the "turn off" webhook).
* **Start of wake-up window** At the start of the wake-up window SleepCycle will turn on the dummy light. It will also set the brightness to 58,8% of the desired brightness level set in the SleepCycle app (this is 150 when it is set to the maximum of 255).
* **Alarm rings** When the (first) alarm rings it will set the brightness to the maximum value.

## Use Case

Personally, I use this emulator together with [Homey](http://homey.app/).
Because SleepCycle requires the webserver to run on port 80, I could not run the emulator on Homey itself, and am therefore running it on a Raspberry Pi.
I have set up four flows in Homey that accept incoming webhooks and that do the following:

* When I set my alarm, Homey turns all my lights and other devices off.
* When SleepCycle's wake-up window starts, it sends a turn on request. Homey then slowly turns on my lights (during 20 minutes, the length of my wake up window) and it starts the ['t Koffiehuis](https://open.spotify.com/playlist/37i9dQZF1DWYPwGkJoztcR?si=wx8JNW0sQSuV5NI2ekXYLQ) playlist on my speakers.
* When my alarm clock rings (i.e. when SleepCycle sets the brightness to the maximum value), Homey turns on my microwave/oven after a few seconds, since I regularly use it in the morning (sadly it cannot control my coffee machine yet). 

## Credits

- [Casper Boone](https://github.com/casperboone)
- [Magicus](https://github.com/magicus)
- [blocke](https://github.com/blocke)
- [All Contributors](../../contributors)

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.
