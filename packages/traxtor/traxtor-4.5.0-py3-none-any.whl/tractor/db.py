# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2023-2024.
"""
Module to get values of keys from gschema
"""

import os

from gi.repository import Gio, GLib


def dconf() -> Gio.Settings:
    """
    connect to gsettings database
    """
    schema = "org.tractor"
    schemas = Gio.SettingsSchemaSource.get_default()
    if not Gio.SettingsSchemaSource.lookup(schemas, schema, False):
        gschema_dir = "/usr/share/glib-2.0/schemas/"
        for directory in GLib.get_system_data_dirs():
            gdir = f"{directory}/glib-2.0/schemas/"
            if os.path.exists(gdir):
                gschema_dir = os.path.abspath(gdir)
                break
        raise FileNotFoundError(
            f"""
        Please compile the "tractor.gschema.xml" file.
        In GNU/Linux you can copy it from
        "{os.path.dirname(os.path.abspath(__file__))}"
        to "{gschema_dir}" and run:
        "sudo glib-compile-schemas {gschema_dir}"
        """
        )

    conf = Gio.Settings.new(schema)
    return conf


def get_val(key: str) -> bool | int | str:
    """
    get the value of the key
    """
    conf = dconf()
    match key:
        case "pid" | "socks-port" | "http-port" | "dns-port" | "bridge-type":
            return conf.get_int(key)
        case "exit-node":
            return conf.get_string(key)
        case "accept-connection":
            return conf.get_boolean(key)
        case "plugable-transport":
            path_list = conf.get_value(key)
            return path_list[get_val("bridge-type")]
        case _:
            raise TypeError("key is not supported")

def set_val(key: str, value: bool | int | str) -> None:
    """
    set a value for the key
    """
    conf = dconf()
    match key:
        case "pid" | "socks-port" | "http-port" | "dns-port" | "bridge-type":
            conf.set_int(key, value)
        case "exit-node":
            conf.set_string(key, value)
        case "accept-connection":
            conf.set_boolean(key, value)
        case "plugable-transport":
            path_list = list(conf.get_value(key))
            path_list[get_val("bridge-type")] = value
            gvar = GLib.Variant("(sssss)", tuple(path_list))
            conf.set_value(key, gvar)
        case _:
            raise TypeError("key is not supported")


def reset(key: str) -> None:
    """
    Reset a key
    """
    dconf().reset(key)


def data_directory() -> str:
    """
    return the data directory for tractor
    """
    return GLib.get_user_config_dir() + "/tractor"
