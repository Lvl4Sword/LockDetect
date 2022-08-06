#!/usr/bin/env python3
import subprocess
import sys
import typing


FREEDESKTOP_SCREENSAVER = ['dbus-send',
                           '--session',
                           '--dest=org.freedesktop.ScreenSaver',
                           '--type=method_call',
                           '--print-reply',
                           '--reply-timeout=1000',
                           '/ScreenSaver',
                           'org.freedesktop.ScreenSaver.GetActive']
GNOME_SCREENSAVER = ['dbus-send',
                     '--session',
                     '--dest=org.gnome.ScreenSaver',
                     '--type=method_call',
                     '--print-reply',
                     '--reply-timeout=1000',
                     '/ScreenSaver',
                     'org.gnome.ScreenSaver.GetActive']
GNOME3_SCREENSAVER = ['dbus-send',
                      '--session',
                      '--dest=org.gnome.ScreenSaver',
                      '--type=method_call',
                      '--print-reply',
                      '--reply-timeout=1000',
                      '/org/gnome/ScreenSaver',
                      'org.gnome.ScreenSaver.GetActive']
KDE_SCREENSAVER = ['dbus-send',
                   '--session',
                   '--dest=org.kde.screensaver',
                   '--type=method_call',
                   '--print-reply',
                   '--reply-timeout=1000',
                   '/ScreenSaver',
                   'org.freedesktop.ScreenSaver.GetActive']
SCREENSAVERS = {'FREEDESKTOP_SCREENSAVER': {'command': FREEDESKTOP_SCREENSAVER},
                'GNOME_SCREENSAVER': {'command': GNOME_SCREENSAVER},
                'GNOME3_SCREENSAVER': {'command': GNOME3_SCREENSAVER},
                'KDE_SCREENSAVER': {'command': KDE_SCREENSAVER}}


def detect_windows():
    import ctypes
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    result = user32.GetForegroundWindow()
    if result == 0:
        return True
    else:
        return False


def detect_linux(linux_screensaver_command: typing.Optional[str] = None):
    if linux_screensaver_command is None:
        the_command = detect_linux_screensaver_command()
        if the_command is not None:
            linux_screensaver_command = the_command
        else:
            return None, 'detect_linux command is None'
    else:
        if linux_screensaver_command in SCREENSAVERS:
            linux_screensaver_command = SCREENSAVERS[linux_screensaver_command]['command']
        else:
            return None, 'You need to specify a screensaver command from SCREENSAVERS or file a pull request'
    try:
        check_screensaver = subprocess.check_output(linux_screensaver_command,
                                                    stderr=subprocess.DEVNULL).decode().split()[-1]
        if check_screensaver == 'true':
            return True
        elif check_screensaver == 'false':
            return False
        else:
            return None, 'check_screensaver in detect_linux is returning something other than true or false'
    except(TypeError, subprocess.CalledProcessError) as e:
        return None, f'check_screensaver experienced a TypeError or CalledProcessError: {str(e)}'


def detect_linux_screensaver_command():
    for x, y in enumerate(SCREENSAVERS):
        try:
            the_command = SCREENSAVERS[y]['command']
            the_output = subprocess.check_output(the_command, stderr=subprocess.DEVNULL).decode().split()[-1]
            if the_output in ['false', 'true']:
                return the_command
        except subprocess.CalledProcessError as e:
            if 'DBus.Error' in str(e):
                pass
    return None, 'detect_linux_screensaver_command could not come up with your command'


def detect_mac():
    import Quartz
    session_dict = Quartz.CGSessionCopyCurrentDictionary()
    if 'CGSSessionScreenIsLocked' in session_dict.keys():
        return True
    else:
        return False


def locked(linux_command: typing.Optional[str] = None):
    if sys.platform.startswith('win'):
        return detect_windows()
    elif sys.platform.startswith('linux'):
        if linux_command is not None:
            return detect_linux(linux_command)
        else:
            return detect_linux()
    elif sys.platform.startswith('darwin'):
        return detect_mac()
    else:
        return None, 'You are running something other than Linux, Mac, or Windows.'
