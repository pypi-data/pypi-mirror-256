#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module inherits constants for Denon AVR receivers.

:copyright: (c) 2021 by Oliver Goetz.
:license: MIT, see LICENSE for more details.
"""

import re
from collections import namedtuple

import attr

# Attr constants
DENON_ATTR_SETATTR = [attr.setters.validate, attr.setters.convert]

# Types for constants
ReceiverType = namedtuple("ReceiverType", ["type", "port"])
DescriptionType = namedtuple("DescriptionType", ["port", "url"])
ReceiverURLs = namedtuple(
    "ReceiverURLs",
    [
        "appcommand",
        "appcommand0300",
        "status",
        "mainzone",
        "deviceinfo",
        "netaudiostatus",
        "tunerstatus",
        "hdtunerstatus",
        "command_sel_src",
        "command_fav_src",
        "command_power_on",
        "command_power_standby",
        "command_volume_up",
        "command_volume_down",
        "command_set_volume",
        "command_mute_on",
        "command_mute_off",
        "command_sel_sound_mode",
        "command_netaudio_post",
        "command_set_all_zone_stereo",
        "command_pause",
        "command_play",
    ],
)
TelnetCommands = namedtuple(
    "TelnetCommands",
    [
        "command_sel_src",
        "command_fav_src",
        "command_power_on",
        "command_power_standby",
        "command_volume_up",
        "command_volume_down",
        "command_set_volume",
        "command_mute_on",
        "command_mute_off",
        "command_sel_sound_mode",
        "command_set_all_zone_stereo",
        "command_pause",
        "command_play",
        "command_multieq",
        "command_dynamiceq",
        "command_reflevoffset",
        "command_dynamicvol",
        "command_tonecontrol",
        "command_bass",
        "command_treble",
    ],
)

# AVR-X search patterns
DEVICEINFO_AVR_X_PATTERN = re.compile(
    r"(.*AV(C|R)-(X|S).*|.*SR500[6-9]|.*SR60(07|08|09|10|11|12|13)|."
    r"*SR70(07|08|09|10|11|12|13)|.*SR501[3-4]|.*NR1604|.*NR1710)"
)

DEVICEINFO_COMMAPI_PATTERN = re.compile(r"(0210|0220|0250|0300|0301)")

# Receiver types
AVR_NAME = "avr"
AVR_X_NAME = "avr-x"
AVR_X_2016_NAME = "avr-x-2016"

AVR = ReceiverType(type=AVR_NAME, port=80)
AVR_X = ReceiverType(type=AVR_X_NAME, port=80)
AVR_X_2016 = ReceiverType(type=AVR_X_2016_NAME, port=8080)
VALID_RECEIVER_TYPES = (AVR, AVR_X, AVR_X_2016)

DESCRIPTION_TYPES = {
    AVR_NAME: DescriptionType(port=8080, url="/description.xml"),
    AVR_X_NAME: DescriptionType(port=8080, url="/description.xml"),
    AVR_X_2016_NAME: DescriptionType(
        port=60006, url="/upnp/desc/aios_device/aios_device.xml"
    ),
}

SOURCE_MAPPING = {
    "TV AUDIO": "TV",
    "iPod/USB": "USB/IPOD",
    "Bluetooth": "BT",
    "Blu-ray": "BD",
    "CBL/SAT": "SAT/CBL",
    "NETWORK": "NET",
    "Media Player": "MPLAY",
    "AUX": "AUX1",
    "Tuner": "TUNER",
    "FM": "TUNER",
    "SpotifyConnect": "Spotify Connect",
}

CHANGE_INPUT_MAPPING = {
    "Favorites": "FAVORITES",
    "Flickr": "FLICKR",
    "Internet Radio": "IRADIO",
    "Media Server": "SERVER",
    "Online Music": "NET",
    "Spotify": "SPOTIFY",
}

TELNET_SOURCES = {
    "CD",
    "PHONO",
    "TUNER",
    "DVD",
    "BD",
    "TV",
    "SAT/CBL",
    "MPLAY",
    "GAME",
    "HDRADIO",
    "NET",
    "PANDORA",
    "SIRIUSXM",
    "SOURCE",
    "LASTFM",
    "FLICKR",
    "IRADIO",
    "IRP",
    "SERVER",
    "FAVORITES",
    "AUX1",
    "AUX2",
    "AUX3",
    "AUX4",
    "AUX5",
    "AUX6",
    "AUX7",
    "BT",
    "USB/IPOD",
    "USB DIRECT",
    "IPOD DIRECT",
}

TELNET_MAPPING = {
    "FAVORITES": "Favorites",
    "FLICKR": "Flickr",
    "IRADIO": "Internet Radio",
    "IRP": "Internet Radio",
    "SERVER": "Media Server",
    "SPOTIFY": "Spotify",
}

# Sound modes
ALL_ZONE_STEREO = "ALL ZONE STEREO"

SOUND_MODE_MAPPING = {
    "MUSIC": [
        "PLII MUSIC",
        "DTS NEO:6 MUSIC",
        "DTS NEO:6 M",
        "DTS NEO:X M",
        "DOLBY D +NEO:X M",
        "DTS NEO:X MUSIC",
        "DOLBY PL2 MUSIC",
        "DOLBY PL2 M",
        "PLIIX MUSIC",
        "DOLBY PL2 X MUSIC",
    ],
    "MOVIE": [
        "PLII MOVIE",
        "PLII CINEMA",
        "DTS NEO:X CINEMA",
        "DTS NEO:X C",
        "DTS NEO:6 CINEMA",
        "DTS NEO:6 C",
        "DOLBY D +NEO:X C",
        "PLIIX CINEMA",
        "DOLBY PLII MOVIE",
        "MULTI IN + VIRTUAL:X",
        "DOLBY PL2 CINEMA",
        "DOLBY PL2 C",
        "DOLBY PL2 X MOVIE",
        "DOLBY PL2 MOVIE",
    ],
    "GAME": [
        "PLII GAME",
        "DOLBY D +NEO:X G",
        "DOLBY PL2 GAME",
        "DOLBY PL2 G",
        "DOLBY PL2 X GAME",
        "DOLBY PLII GAME",
    ],
    "AUTO": ["None"],
    "STANDARD": ["None2"],
    "VIRTUAL": ["VIRTUAL"],
    "MATRIX": ["MATRIX"],
    "ROCK ARENA": ["ROCK ARENA"],
    "JAZZ CLUB": ["JAZZ CLUB"],
    "VIDEO GAME": ["VIDEO GAME"],
    "MONO MOVIE": ["MONO MOVIE"],
    "DIRECT": ["DIRECT"],
    "PURE DIRECT": ["PURE_DIRECT", "PURE DIRECT"],
    "DOLBY DIGITAL": [
        "DOLBY DIGITAL",
        "DOLBY D + DOLBY SURROUND",
        "DOLBY D+DS",
        "DOLBY D+ +DS",
        "DOLBY DIGITAL +",
        "STANDARD(DOLBY)",
        "DOLBY SURROUND",
        "DOLBY D + +DOLBY SURROUND",
        "NEURAL",
        "NEURAL:X",
        "DOLBY HD",
        "DOLBY HD + DOLBY SURROUND",
        "MULTI IN + DSUR",
        "MULTI IN + NEURAL:X",
        "MULTI IN + DOLBY SURROUND",
        "DOLBY D + NEURAL:X",
        "DOLBY DIGITAL + NEURAL:X",
        "DOLBY DIGITAL + + NEURAL:X",
        "DOLBY ATMOS",
        "DOLBY AUDIO - DOLBY SURROUND",
        "DOLBY TRUEHD",
        "DOLBY AUDIO - DOLBY DIGITAL PLUS",
        "DOLBY AUDIO - TRUEHD + DSUR",
        "DOLBY AUDIO - DOLBY TRUEHD",
        "DOLBY AUDIO - TRUEHD + NEURAL:X",
        "DOLBY AUDIO - DD + NEURAL:X",
        "DOLBY AUDIO - DD + DSUR",
        "DOLBY AUDIO - DD+   + NEURAL:X",
        "DOLBY AUDIO - DD+   + DSUR",
        "DOLBY AUDIO-DD+ +DSUR",
        "DOLBY AUDIO - DOLBY DIGITAL",
        "DOLBY AUDIO-DSUR",
        "DOLBY AUDIO-DD+DSUR",
        "DOLBY PRO LOGIC",
    ],
    "DTS SURROUND": [
        "DTS SURROUND",
        "DTS NEURAL:X",
        "STANDARD(DTS)",
        "DTS + NEURAL:X",
        "MULTI CH IN",
        "DTS-HD MSTR",
        "DTS VIRTUAL:X",
        "DTS-HD + NEURAL:X",
        "DTS-HD",
        "DTS + VIRTUAL:X",
        "DTS + DOLBY SURROUND",
        "DTS-HD + DOLBY SURROUND",
        "DTS-HD + DSUR",
        "DTS:X MSTR",
    ],
    "AURO3D": ["AURO-3D"],
    "AURO2DSURR": ["AURO-2D SURROUND"],
    "MCH STEREO": [
        "MULTI CH STEREO",
        "MULTI_CH_STEREO",
        "MCH STEREO",
        "MULTI CH IN 7.1",
    ],
    "STEREO": ["STEREO"],
    ALL_ZONE_STEREO: ["ALL ZONE STEREO"],
}

# Receiver sources
NETAUDIO_SOURCES = {
    "AirPlay",
    "Online Music",
    "Media Server",
    "iPod/USB",
    "Bluetooth",
    "Internet Radio",
    "Favorites",
    "SpotifyConnect",
    "Flickr",
    "NET/USB",
    "Music Server",
    "NETWORK",
    "NET",
}
TUNER_SOURCES = {"Tuner", "TUNER"}
HDTUNER_SOURCES = {"HD Radio", "HDRADIO"}
PLAYING_SOURCES = set().union(*[NETAUDIO_SOURCES, TUNER_SOURCES, HDTUNER_SOURCES])

# Image URLs
STATIC_ALBUM_URL = "http://{host}:{port}/img/album%20art_S.png"
ALBUM_COVERS_URL = "http://{host}:{port}/NetAudio/art.asp-jpg?{hash}"

# General URLs
APPCOMMAND_URL = "/goform/AppCommand.xml"
APPCOMMAND0300_URL = "/goform/AppCommand0300.xml"
DEVICEINFO_URL = "/goform/Deviceinfo.xml"
NETAUDIOSTATUS_URL = "/goform/formNetAudio_StatusXml.xml"
TUNERSTATUS_URL = "/goform/formTuner_TunerXml.xml"
HDTUNERSTATUS_URL = "/goform/formTuner_HdXml.xml"
COMMAND_NETAUDIO_POST_URL = "/NetAudio/index.put.asp"
COMMAND_PAUSE = "/goform/formiPhoneAppDirect.xml?NS9B"
COMMAND_PLAY = "/goform/formiPhoneAppDirect.xml?NS9A"


# Main Zone URLs
STATUS_URL = "/goform/formMainZone_MainZoneXmlStatus.xml"
MAINZONE_URL = "/goform/formMainZone_MainZoneXml.xml"
COMMAND_SEL_SRC_URL = "/goform/formiPhoneAppDirect.xml?SI"
COMMAND_FAV_SRC_URL = "/goform/formiPhoneAppDirect.xml?ZM"
COMMAND_POWER_ON_URL = "/goform/formiPhoneAppPower.xml?1+PowerOn"
COMMAND_POWER_STANDBY_URL = "/goform/formiPhoneAppPower.xml?1+PowerStandby"
COMMAND_VOLUME_UP_URL = "/goform/formiPhoneAppDirect.xml?MVUP"
COMMAND_VOLUME_DOWN_URL = "/goform/formiPhoneAppDirect.xml?MVDOWN"
COMMAND_SET_VOLUME_URL = "/goform/formiPhoneAppVolume.xml?1+{volume:.1f}"
COMMAND_MUTE_ON_URL = "/goform/formiPhoneAppMute.xml?1+MuteOn"
COMMAND_MUTE_OFF_URL = "/goform/formiPhoneAppMute.xml?1+MuteOff"
COMMAND_SEL_SM_URL = "/goform/formiPhoneAppDirect.xml?MS"
COMMAND_SET_ZST_URL = "/goform/formiPhoneAppDirect.xml?MN"

# Zone 2 URLs
STATUS_Z2_URL = "/goform/formZone2_Zone2XmlStatus.xml"
COMMAND_SEL_SRC_Z2_URL = "/goform/formiPhoneAppDirect.xml?Z2"
COMMAND_FAV_SRC_Z2_URL = "/goform/formiPhoneAppDirect.xml?Z2"
COMMAND_POWER_ON_Z2_URL = "/goform/formiPhoneAppPower.xml?2+PowerOn"
COMMAND_POWER_STANDBY_Z2_URL = "/goform/formiPhoneAppPower.xml?2+PowerStandby"
COMMAND_VOLUME_UP_Z2_URL = "/goform/formiPhoneAppDirect.xml?Z2UP"
COMMAND_VOLUME_DOWN_Z2_URL = "/goform/formiPhoneAppDirect.xml?Z2DOWN"
COMMAND_SET_VOLUME_Z2_URL = "/goform/formiPhoneAppVolume.xml?2+{volume:.1f}"
COMMAND_MUTE_ON_Z2_URL = "/goform/formiPhoneAppMute.xml?2+MuteOn"
COMMAND_MUTE_OFF_Z2_URL = "/goform/formiPhoneAppMute.xml?2+MuteOff"

# Zone 3 URLs
STATUS_Z3_URL = "/goform/formZone3_Zone3XmlStatus.xml"
COMMAND_SEL_SRC_Z3_URL = "/goform/formiPhoneAppDirect.xml?Z3"
COMMAND_FAV_SRC_Z3_URL = "/goform/formiPhoneAppDirect.xml?Z3"
COMMAND_POWER_ON_Z3_URL = "/goform/formiPhoneAppPower.xml?3+PowerOn"
COMMAND_POWER_STANDBY_Z3_URL = "/goform/formiPhoneAppPower.xml?3+PowerStandby"
COMMAND_VOLUME_UP_Z3_URL = "/goform/formiPhoneAppDirect.xml?Z3UP"
COMMAND_VOLUME_DOWN_Z3_URL = "/goform/formiPhoneAppDirect.xml?Z3DOWN"
COMMAND_SET_VOLUME_Z3_URL = "/goform/formiPhoneAppVolume.xml?3+{volume:.1f}"
COMMAND_MUTE_ON_Z3_URL = "/goform/formiPhoneAppMute.xml?3+MuteOn"
COMMAND_MUTE_OFF_Z3_URL = "/goform/formiPhoneAppMute.xml?3+MuteOff"

DENONAVR_URLS = ReceiverURLs(
    appcommand=APPCOMMAND_URL,
    appcommand0300=APPCOMMAND0300_URL,
    status=STATUS_URL,
    mainzone=MAINZONE_URL,
    deviceinfo=DEVICEINFO_URL,
    netaudiostatus=NETAUDIOSTATUS_URL,
    tunerstatus=TUNERSTATUS_URL,
    hdtunerstatus=HDTUNERSTATUS_URL,
    command_sel_src=COMMAND_SEL_SRC_URL,
    command_fav_src=COMMAND_FAV_SRC_URL,
    command_power_on=COMMAND_POWER_ON_URL,
    command_power_standby=COMMAND_POWER_STANDBY_URL,
    command_volume_up=COMMAND_VOLUME_UP_URL,
    command_volume_down=COMMAND_VOLUME_DOWN_URL,
    command_set_volume=COMMAND_SET_VOLUME_URL,
    command_mute_on=COMMAND_MUTE_ON_URL,
    command_mute_off=COMMAND_MUTE_OFF_URL,
    command_sel_sound_mode=COMMAND_SEL_SM_URL,
    command_netaudio_post=COMMAND_NETAUDIO_POST_URL,
    command_set_all_zone_stereo=COMMAND_SET_ZST_URL,
    command_pause=COMMAND_PAUSE,
    command_play=COMMAND_PLAY,
)

ZONE2_URLS = ReceiverURLs(
    appcommand=APPCOMMAND_URL,
    appcommand0300=APPCOMMAND0300_URL,
    status=STATUS_Z2_URL,
    mainzone=MAINZONE_URL,
    deviceinfo=DEVICEINFO_URL,
    netaudiostatus=NETAUDIOSTATUS_URL,
    tunerstatus=TUNERSTATUS_URL,
    hdtunerstatus=HDTUNERSTATUS_URL,
    command_sel_src=COMMAND_SEL_SRC_Z2_URL,
    command_fav_src=COMMAND_FAV_SRC_Z2_URL,
    command_power_on=COMMAND_POWER_ON_Z2_URL,
    command_power_standby=COMMAND_POWER_STANDBY_Z2_URL,
    command_volume_up=COMMAND_VOLUME_UP_Z2_URL,
    command_volume_down=COMMAND_VOLUME_DOWN_Z2_URL,
    command_set_volume=COMMAND_SET_VOLUME_Z2_URL,
    command_mute_on=COMMAND_MUTE_ON_Z2_URL,
    command_mute_off=COMMAND_MUTE_OFF_Z2_URL,
    command_sel_sound_mode=COMMAND_SEL_SM_URL,
    command_netaudio_post=COMMAND_NETAUDIO_POST_URL,
    command_set_all_zone_stereo=COMMAND_SET_ZST_URL,
    command_pause=COMMAND_PAUSE,
    command_play=COMMAND_PLAY,
)

ZONE3_URLS = ReceiverURLs(
    appcommand=APPCOMMAND_URL,
    appcommand0300=APPCOMMAND0300_URL,
    status=STATUS_Z3_URL,
    mainzone=MAINZONE_URL,
    deviceinfo=DEVICEINFO_URL,
    netaudiostatus=NETAUDIOSTATUS_URL,
    tunerstatus=TUNERSTATUS_URL,
    hdtunerstatus=HDTUNERSTATUS_URL,
    command_sel_src=COMMAND_SEL_SRC_Z3_URL,
    command_fav_src=COMMAND_FAV_SRC_Z3_URL,
    command_power_on=COMMAND_POWER_ON_Z3_URL,
    command_power_standby=COMMAND_POWER_STANDBY_Z3_URL,
    command_volume_up=COMMAND_VOLUME_UP_Z3_URL,
    command_volume_down=COMMAND_VOLUME_DOWN_Z3_URL,
    command_set_volume=COMMAND_SET_VOLUME_Z3_URL,
    command_mute_on=COMMAND_MUTE_ON_Z3_URL,
    command_mute_off=COMMAND_MUTE_OFF_Z3_URL,
    command_sel_sound_mode=COMMAND_SEL_SM_URL,
    command_netaudio_post=COMMAND_NETAUDIO_POST_URL,
    command_set_all_zone_stereo=COMMAND_SET_ZST_URL,
    command_pause=COMMAND_PAUSE,
    command_play=COMMAND_PLAY,
)

# Telnet Events
ALL_TELNET_EVENTS = "ALL"
TELNET_EVENTS = {
    "CV",
    "DC",
    "DIM",
    "ECO",
    "HD",
    "MN",
    "MS",
    "MU",
    "MV",
    "NS",
    "NSA",
    "NSE",
    "OP",
    "PS",
    "PV",
    "PW",
    "RM",
    "SD",
    "SI",
    "SLP",
    "SR",
    "SS",
    "STBY",
    "SV",
    "SY",
    "TF",
    "TM",
    "TP",
    "TR",
    "UG",
    "VS",
    "ZM",
    "Z2",
    "Z3",
}
ALL_ZONE_TELNET_EVENTS = {
    "DIM",
    "HD",
    "NS",
    "NSA",
    "NSE",
    "MN",
    "PW",
    "RM",
    "SY",
    "TF",
    "TM",
    "TP",
    "TR",
    "UG",
}

DENONAVR_TELNET_COMMANDS = TelnetCommands(
    command_sel_src="SI",
    command_fav_src="ZM",
    command_power_on="ZMON",
    command_power_standby="ZMOFF",
    command_volume_up="MVUP",
    command_volume_down="MVDOWN",
    command_set_volume="MV{volume:02d}",
    command_mute_on="MUON",
    command_mute_off="MUOFF",
    command_sel_sound_mode="MS",
    command_set_all_zone_stereo="MN",
    command_pause="NS9B",
    command_play="NS9A",
    command_multieq="PSMULTEQ:",
    command_dynamiceq="PSDYNEQ ",
    command_reflevoffset="PSREFLEV ",
    command_dynamicvol="PSDYNVOL ",
    command_tonecontrol="PSTONE CTRL ",
    command_bass="PSBAS ",
    command_treble="PSTRE ",
)

ZONE2_TELNET_COMMANDS = TelnetCommands(
    command_sel_src="Z2",
    command_fav_src="Z2",
    command_power_on="Z2ON",
    command_power_standby="Z2OFF",
    command_volume_up="Z2UP",
    command_volume_down="Z2DOWN",
    command_set_volume="Z2{volume:02d}",
    command_mute_on="Z2MUON",
    command_mute_off="Z2MUOFF",
    command_sel_sound_mode="MS",
    command_set_all_zone_stereo="MN",
    command_pause="NS9B",
    command_play="NS9A",
    command_multieq="PSMULTEQ:",
    command_dynamiceq="PSDYNEQ ",
    command_reflevoffset="PSREFLEV ",
    command_dynamicvol="PSDYNVOL ",
    command_tonecontrol="PSTONE CTRL ",
    command_bass="PSBAS ",
    command_treble="PSTRE ",
)

ZONE3_TELNET_COMMANDS = TelnetCommands(
    command_sel_src="Z3",
    command_fav_src="Z3",
    command_power_on="Z3ON",
    command_power_standby="Z3OFF",
    command_volume_up="Z3UP",
    command_volume_down="Z3DOWN",
    command_set_volume="Z3{volume:02d}",
    command_mute_on="Z3MUON",
    command_mute_off="Z3MUOFF",
    command_sel_sound_mode="MS",
    command_set_all_zone_stereo="MN",
    command_pause="NS9B",
    command_play="NS9A",
    command_multieq="PSMULTEQ:",
    command_dynamiceq="PSDYNEQ ",
    command_reflevoffset="PSREFLEV ",
    command_dynamicvol="PSDYNVOL ",
    command_tonecontrol="PSTONE CTRL ",
    command_bass="PSBAS ",
    command_treble="PSTRE ",
)

# States
POWER_ON = "ON"
POWER_OFF = "OFF"
POWER_STANDBY = "STANDBY"
POWER_STATES = {POWER_ON, POWER_OFF, POWER_STANDBY}
STATE_ON = "on"
STATE_OFF = "off"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"

# Zones
ALL_ZONES = "All"
MAIN_ZONE = "Main"
ZONE2 = "Zone2"
ZONE3 = "Zone3"
VALID_ZONES = {MAIN_ZONE, ZONE2, ZONE3}

# Setup additional zones
NO_ZONES = None
ZONE2_NAME = {ZONE2: None}
ZONE3_NAME = {ZONE3: None}
ZONE2_ZONE3_NAME = {ZONE2: None, ZONE3: None}

# AppCommand related
APPCOMMAND_CMD_TEXT = "cmd_text"
APPCOMMAND_NAME = "name"

# Audyssey parameter
MULTI_EQ_MAP_APPCOMMAND = {"0": "Off", "1": "Flat", "2": "L/R Bypass", "3": "Reference"}
MULTI_EQ_MAP_TELNET = {
    "OFF": "Off",
    "FLAT": "Flat",
    "BYP.LR": "L/R Bypass",
    "AUDYSSEY": "Reference",
    "MANUAL": "Manual",
}
MULTI_EQ_MAP = {**MULTI_EQ_MAP_APPCOMMAND, **MULTI_EQ_MAP_TELNET}
MULTI_EQ_MAP_LABELS_APPCOMMAND = {
    value: key for key, value in MULTI_EQ_MAP_APPCOMMAND.items()
}
MULTI_EQ_MAP_LABELS_TELNET = {value: key for key, value in MULTI_EQ_MAP_TELNET.items()}

REF_LVL_OFFSET_MAP_APPCOMMAND = {"0": "0dB", "1": "+5dB", "2": "+10dB", "3": "+15dB"}
REF_LVL_OFFSET_MAP_TELNET = {"0": "0dB", "5": "+5dB", "10": "+10dB", "15": "+15dB"}
REF_LVL_OFFSET_MAP = {**REF_LVL_OFFSET_MAP_APPCOMMAND, **REF_LVL_OFFSET_MAP_TELNET}
REF_LVL_OFFSET_MAP_LABELS_APPCOMMAND = {
    value: key for key, value in REF_LVL_OFFSET_MAP_APPCOMMAND.items()
}
REF_LVL_OFFSET_MAP_LABELS_TELNET = {
    value: key for key, value in REF_LVL_OFFSET_MAP_TELNET.items()
}

DYNAMIC_VOLUME_MAP_APPCOMMAND = {"0": "Off", "1": "Light", "2": "Medium", "3": "Heavy"}
DYNAMIC_VOLUME_MAP_TELNET = {
    "OFF": "Off",
    "LIT": "Light",
    "MED": "Medium",
    "HEV": "Heavy",
}
DYNAMIC_VOLUME_MAP = {**DYNAMIC_VOLUME_MAP_APPCOMMAND, **DYNAMIC_VOLUME_MAP_TELNET}
DYNAMIC_VOLUME_MAP_LABELS_APPCOMMAND = {
    value: key for key, value in DYNAMIC_VOLUME_MAP_APPCOMMAND.items()
}
DYNAMIC_VOLUME_MAP_LABELS_TELNET = {
    value: key for key, value in DYNAMIC_VOLUME_MAP_TELNET.items()
}
