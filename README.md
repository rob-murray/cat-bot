# cat-bot
Raspberry Pi Python app for scheduled :smile_cat: cat feeder :smile_cat:

This is designed for Raspberry Pi with the hardware below available via its GPIO;

* Continuous rotation servo
* Piezo buzzer
* LED
* Button

The physical setup could be something like a food dispsenser releasing dry food through a funnel with rate of dispersal controlled by a paddle which is then connected to the servo. For example:

```
  +           +
  |           |
  |           |
  |           |
  |           |
  |           |
  |           |
  |           |
  X          XX
  XXX       XX
    XX     XX
        +
      +---+
+       +        +
|                |
+----------------+
```

The continuous rotation servo rotates for a given length of time to deliver a determined amount of food into a bowl below.

It supports multiple feeds per day at specified times or at ad-hoc intevals via the attached button however, you cannot feed the cat more than the permitted number of times per day. When a feed is triggered a buzzer will be sounded to inform the cat and induce regular behaviour of associating the buzzer with feeding time.

### Getting started

#### Dependencies

* Python 2.x
* PIP
* Virtualenv - manage Python environments
* RPi.GPIO - to run on Raspberry Pi


```bash
$ mkvirtualenv cat_bot
//
$ workon cat_bot
```


#### Install dependencies via pip

```bash
$ pip install -r requirements.txt
```

#### Save installed dependencies to pip

```bash
$ pip freeze > requirements.txt
```

### Configuration

Configuration manifests are in `config` directory. There are the following options available:

* `logging_config` - Path to the logging configuration (see below)
* `io_adapter` - The classname of IO adapter. Supports **{LoggingIO|RaspberryPi}** - LoggingIO can be used for dev testing where there is no GPIO.
* `feeds` - An array of `Feed` objects (see below)

The configuration file used can be set by the `APP_ENV` Environment variable, this supports the following values **{development|production}**. The default is `development` if not provided.

#### Logging

Two logging configs suited for development and running on the Pi - `logging-dev.yaml` and `logging-prod.yaml`.

TODO: more logging info

#### Feed

A `Feed` is a meal for the cat. There can be many per day and given times, you cannot feed the cat more than the permitted number of feeds.

A `Feed` can be configured with the following properites:

* `name` - The name of the feed, eg "morning"
* `hour` - The hour of the day at which to feed in 24 hour format
* `minute` - The minute of the day at which to feed
* `quantity` - TODO The quantity of food to be served aka the servo rotation time in secs


### Running

With a valid configuration both of connected GPIO devices and internal configuration the application can be run by executing the wrapper in the `bin/` folder:

```bash
$ bin/cat_bot
# or
$ APP_ENV=production bin/cat_bot
```

