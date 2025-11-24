"""
The "Jump Speed" Plugin
fork from original by Blacky_BPG
"""

import l10n
import functools
import myNotebook as nb

_ = functools.partial(l10n.Translations.translate, context=__file__)

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import sys
import time
from l10n import Locale

this = sys.modules[__name__]  # For holding module globals

try:
    from config import config
except ImportError:
    config = dict()

APP_VERSION = "25.11.24_b2149"

CFG_DISTANCE = "JumpSpeed_distance"
CFG_JUMPS = "JumpSpeed_jumps"
CFG_TIME = "JumpSpeed_time"
CFG_DESIGN = "theme"
COLOR_NORM = ("#000000", "#80FFFF", "#80FFFF")


class Jump(object):
    """
    Represent a jump
    """

    distance = 0.0
    time = 0


class JumpSpeed(object):
    """
    The main class for the jumpspeed plugin
    """

    speed_widget = None
    rate_widget = None
    dist_widget = None
    saved_distance = 0
    saved_jumps = 0
    saved_time = 0
    start_time = 0
    appdesign = 0
    jumps = []

    def reset(self):
        """
        Reset button pressed
        !! disabled for better visuals in app
        """
        self.jumps = []
        self.saved_distance = 0
        self.saved_jumps = 0
        self.saved_time = 0
        self.start_time = 0
        self.update_window()

    def load(self):
        """
        Load saved distance from config
        """
        if config.get_int(CFG_DESIGN):
            self.appdesign = config.get_int(CFG_DESIGN)
        else:
           self.appdesign = 0

        saved = config.get_str(CFG_DISTANCE)
        if not saved:
            self.saved_distance = 0.0
        else:
            self.saved_distance = float(saved)

        savedJ = config.get_str(CFG_JUMPS)
        if not savedJ:
            self.saved_jumps = 0.0
        else:
            self.saved_jumps = float(savedJ)

        savedT = config.get_str(CFG_TIME)
        if not savedT:
            self.saved_time = 0.0
        else:
            self.saved_time = float(savedT)

    def save(self):
        """
        Save the saved distance to config
        :return:
        """
        config.set(CFG_DISTANCE, str(self.saved_distance + self.trip_distance()))
        config.set(CFG_JUMPS, str(self.saved_jumps + self.alljumps()))
        config.set(CFG_TIME, str(self.saved_time + self.sincetime()))

    def start_data(self, totaldistance, totaljumps, totaltime):
        """
        """
        if self.saved_distance == 0:
            self.saved_distance = totaldistance

        self.saved_jumps = totaljumps
        self.saved_time = totaltime / 3600
        self.update_window()
        self.save()

    def jump(self, distance):
        """
        Record a jump
        """
        if self.start_time == 0:
            self.start_time = time.time()

        data = Jump()
        data.distance = distance
        data.time = time.time()
        self.jumps.append(data)
        self.update_window()
        self.save()

    def alljumps(self):
        """
        Overall jumps
        :return overall jumps for trip
        """
        if len(self.jumps) > 0:
            return len(self.jumps)
        else:
            return 0

    def starttime(self):
        """
        start timer for daily statistics
        """
        self.start_time = time.time()
        self.update_window()

    def sincetime(self):
        """
        """
        if self.start_time > 0:
            return (time.time() - self.start_time) / 3600
        else:
            return 1

    def trip_distance(self):
        """
        Measure how far we've jumped
        :return sum of all distances for trip:
        """
        return sum([x.distance for x in self.jumps])

    def rate(self):
        """
        Get the jump/hr rate
        :return jump overall jump rate per hour:
        """
        if self.alljumps() > 0:
            return (self.saved_jumps + self.alljumps()) / (self.saved_time + self.sincetime())
        elif self.saved_jumps > 0 and self.saved_time > 0:
            return self.saved_jumps / self.saved_time
        else:
            return 0

    def ratenow(self):
        """
        Get the jump/hr rate
        :return jump rate for trip per hour:
        """
        if self.alljumps() > 0 and self.sincetime() > 0:
            return self.alljumps() / self.sincetime()
        else:
            return 0

    def speed(self):
        """
        Get the jump speed in ly/hr
        :return overall jump speed rate per hour:
        """
        if self.trip_distance() > 0 and self.alljumps() > 0 and self.sincetime() > 0:
            return (self.saved_distance + self.trip_distance()) / (self.saved_time + self.sincetime())
        elif self.saved_distance > 0 and self.saved_time > 0:
            return self.saved_distance / self.saved_time
        else:
            return 0

    def speednow(self):
        """
        Get the jump speed in ly/hr
        :return jump speed rate for trip per hour:
        """
        if self.trip_distance() > 0 and self.alljumps() > 0 and self.sincetime() > 0:
            return self.trip_distance() / self.sincetime()
        else:
            return 0

    def update_window(self):
        """
        Update the EDMC window
        """
        self.update_jumpspeed_dist()
        self.update_jumpspeed_rate()
        self.update_jumpspeed_speed()

    def update_jumpspeed_rate(self):
        """
        Set the jump rate rate in the EDMC window
        """
        msg = " {}".format(Locale.string_from_number(self.rate(), 2))
        self.rate_widget["foreground"] = COLOR_NORM[self.appdesign]
        self.rate_widget.after(0, self.rate_widget.config, {"text": msg})
        msgnow = " {}  |".format(Locale.string_from_number(self.ratenow(), 2))
        self.ratenow_widget["foreground"] = COLOR_NORM[self.appdesign]
        self.ratenow_widget.after(0, self.ratenow_widget.config, {"text": msgnow})

    def update_jumpspeed_speed(self):
        """
        Set the jump speed rate in the EDMC window
        """
        msg = " {}".format(Locale.string_from_number(self.speed(), 2))
        self.speed_widget["foreground"] = COLOR_NORM[self.appdesign]
        self.speed_widget.after(0, self.speed_widget.config, {"text": msg})
        msgnow = " {}  |".format(Locale.string_from_number(self.speednow(), 2))
        self.speednow_widget["foreground"] = COLOR_NORM[self.appdesign]
        self.speednow_widget.after(0, self.speednow_widget.config, {"text": msgnow})

    def update_jumpspeed_dist(self):
        """
        Set the jump speed rate in the EDMC window
        """
        msg = " {}".format(Locale.string_from_number(self.trip_distance() + self.saved_distance, 2))
        self.dist_widget["foreground"] = COLOR_NORM[self.appdesign]
        self.dist_widget.after(0, self.dist_widget.config, {"text": msg})
        msgnow = " {}  |".format(Locale.string_from_number(self.trip_distance(), 2))
        self.distnow_widget["foreground"] = COLOR_NORM[self.appdesign]
        self.distnow_widget.after(0, self.distnow_widget.config, {"text": msgnow})


def prefs_changed(cmdr, is_beta):
    jumpspeed = this.jumpspeed
    jumpspeed.appdesign = config.get_int(CFG_DESIGN)
    jumpspeed.update_window()

def plugin_start():
    jumpspeed = JumpSpeed()
    jumpspeed.load()
    this.jumpspeed = jumpspeed


def plugin_start3(plugindir):
    jumpspeed = JumpSpeed()
    jumpspeed.load()
    this.jumpspeed = jumpspeed


def plugin_app(parent):
    """
    Create a pair of TK widgets for the EDMC main window
    """
    jumpspeed = this.jumpspeed

    frame = tk.Frame(parent)

    jumpspeed.rate_widget = tk.Label(frame, text="...", justify=tk.RIGHT)
    rate_label = tk.Label(frame, text=_("Jumps/Hour:").encode('iso-8859-1'), justify=tk.LEFT)
    rate_label.grid(row=0, column=0, sticky=tk.W)
    jumpspeed.rate_widget.grid(row=0, column=2, sticky=tk.E)
    rateT_label = tk.Label(frame, text=_("Jumps").encode('iso-8859-1'), justify=tk.LEFT)
    rateT_label.grid(row=0, column=4, sticky=tk.W)

    jumpspeed.ratenow_widget = tk.Label(frame, text="", justify=tk.RIGHT)
    jumpspeed.ratenow_widget.grid(row=0, column=1, sticky=tk.E)

    jumpspeed.speed_widget = tk.Label(frame, text="...", justify=tk.RIGHT)
    speed_label = tk.Label(frame, text=_("Distance/Hour:").encode('iso-8859-1'), justify=tk.LEFT)
    speed_label.grid(row=1, column=0, sticky=tk.W)
    jumpspeed.speed_widget.grid(row=1, column=2, sticky=tk.E)
    speedT_label = tk.Label(frame, text="Ly", justify=tk.LEFT)
    speedT_label.grid(row=1, column=4, sticky=tk.W)

    jumpspeed.speednow_widget = tk.Label(frame, text="", justify=tk.RIGHT)
    jumpspeed.speednow_widget.grid(row=1, column=1, sticky=tk.E)

    jumpspeed.dist_widget = tk.Label(frame, text="...", justify=tk.RIGHT)
    dist_label = tk.Label(frame, text=_("Overall dist.:").encode('iso-8859-1'), justify=tk.LEFT)
    dist_label.grid(row=2, column=0, sticky=tk.W)
    jumpspeed.dist_widget.grid(row=2, column=2, sticky=tk.E)
    distT_label = tk.Label(frame, text="Ly", justify=tk.LEFT)
    distT_label.grid(row=2, column=4, sticky=tk.W)

    jumpspeed.distnow_widget = tk.Label(frame, text="", justify=tk.RIGHT)
    jumpspeed.distnow_widget.grid(row=2, column=1, sticky=tk.E)

    """
    reset_btn = tk.Button(frame, text="Reset", command=jumpspeed.reset)
    reset_btn.grid(row=2, column=1, sticky=tk.W)
    """

    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    frame.columnconfigure(3, weight=0)

    jumpspeed.update_window()
    return frame


def dashboard_entry(cmdr, is_beta, entry):
    this.jumpspeed.update_window()


def journal_entry(cmdr, is_beta, system, station, entry, state):
    """
    Process a journal event
    :param cmdr:
    :param system:
    :param station:
    :param entry:
    :param state:
    :return:
    """
    if "event" in entry:
        if "Shutdown" in entry["event"]:
            this.jumpspeed.save()
            this.jumpspeed.reset()
            this.jumpspeed.load()
        elif "LoadGame" in entry["event"]:
            this.jumpspeed.starttime()
        elif "Statistics" in entry["event"]:
            this.jumpspeed.start_data(entry["Exploration"]["Total_Hyperspace_Distance"], entry["Exploration"]["Total_Hyperspace_Jumps"], entry["Exploration"]["Time_Played"])
        elif "FSDJump" in entry["event"]:
            this.jumpspeed.jump(entry["JumpDist"])

        this.jumpspeed.update_window()
