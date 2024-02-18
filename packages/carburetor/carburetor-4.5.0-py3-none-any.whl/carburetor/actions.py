# Part of Carburetor project
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020-2023.

"""
actions for carburetor
"""

import os
import re
import signal
from subprocess import PIPE, Popen

from gi.repository import Adw, GLib, Gio
from tractor import bridges, checks, proxy, actions as tactions

from . import config
from . import ui


def add(name: str, function, app) -> None:
    """
    adds functions to app as actions
    """
    action = Gio.SimpleAction.new(name, None)
    action.connect("activate", function, app)
    app.add_action(action)


def do_startup(app) -> None:
    """
    actions to do when starting the app up
    """
    add("preferences", on_preferences, app)
    add("about", on_about, app)
    add("show-help-overlay", on_show_help_overlay, app)
    add("quit", on_quit, app)
    add("connect", on_connect, app)
    add("new_id", on_new_id, app)
    add("check_connection", on_check, app)
    add("toggle_proxy", on_toggle_proxy, app)
    add("cancel", on_cancel, app)
    add("save", on_save, app)


def on_preferences(*argv) -> None:
    """
    show the preferences window
    """
    app = argv[2]
    if not app.prefs:
        prefs_window = ui.get("PreferencesWindow")
        prefs_window.set_transient_for(app.window)
        app.prefs = prefs_window
        action = Gio.SimpleAction.new("save")
        action.connect("activate", on_save)
        action_group = Gio.SimpleActionGroup()
        action_group.add_action(action)
        prefs_window.insert_action_group("app", action_group)
    app.prefs.show()


def on_show_help_overlay(*argv) -> None:
    """
    show the shortcuts window
    """
    app = argv[2]
    if not app.shortcuts:
        shortcuts_window = ui.get("help_overlay_w")
        shortcuts_window.set_transient_for(app.window)
        app.shortcuts = shortcuts_window
    app.shortcuts.show()


def on_about(*argv) -> None:
    """
    show the about window
    """
    app = argv[2]
    if not app.about:
        about_window = Adw.AboutWindow.new_from_appdata(
            "metainfo/io.frama.tractor.carburetor.metainfo.xml"
        )
        about_window.set_developers(["Danial Behzadi <dani.behzi@ubuntu.com>"])
        about_window.set_translator_credits(config._("translator-credits"))
        about_window.set_transient_for(app.window)
        about_window.set_hide_on_close(True)
        app.about = about_window
    app.about.show()


def on_quit(*argv) -> None:
    """
    exit the app
    """
    tactions.kill_tor()
    app = argv[2]
    app.quit()


def on_connect(*argv) -> None:
    """
    clicking on connect button
    """
    app = argv[2]
    button = ui.get("SplitButton")
    button.set_sensitive(False)
    progress_bar = ui.get("ProgressBar")
    ui.set_progress_bar(0)
    progress_bar.show()
    cancel_button = ui.get("CancelButton")
    cancel_button.set_visible(True)
    ui.set_orbi("load")
    page = ui.get("MainPage")
    window = ui.get("MainWindow")
    if checks.running():
        text_stopping = config._("Disconnecting…")
        page.set_title(text_stopping)
        action = "stop"
        window.set_hide_on_close(False)
    else:
        text_starting = config._("Connecting…")
        page.set_title(text_starting)
        action = "start"
        window.set_hide_on_close(True)
    connect(action, app)


def on_new_id(*_, **__) -> None:
    """
    clicking on new id button
    """
    if checks.running():
        tactions.new_id()
        toast = config._("You have a new identity!")
    else:
        toast = config._("Tractor is not running!")
    ui.notify(toast)


def on_check(*argv) -> None:
    """
    checks if tractor is connected or not
    """
    app = argv[2]
    ui.set_orbi("load")
    check = Popen([config.COMMAND, "isconnected"], stdout=PIPE)
    app.io = GLib.io_add_watch(check.stdout, GLib.IO_HUP, connected_hup, app)


def on_toggle_proxy(*_, **__) -> None:
    """
    toggle proxy mode on system
    """
    if checks.proxy_set():
        proxy.proxy_unset()
        toast = config._("Proxy has been unset")
    else:
        proxy.proxy_set()
        toast = config._("Proxy has been set")
    ui.notify(toast)


def on_cancel(*_, **__) -> None:
    """
    abort the connection
    """
    dconf = config.dconf
    pid = dconf.get_int("pid")
    os.killpg(os.getpgid(pid), signal.SIGTERM)
    dconf.reset("pid")


def on_save(*_, **__) -> None:
    """
    clicking on save button in bridges
    """
    textview = ui.get("BridgesTextView")
    buff = textview.get_buffer()
    text = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), 0)
    regex = re.compile(r"^( )*([Bb][Rr][Ii][Dd][Gg][Ee])?( )*", re.MULTILINE)
    bridges_file = bridges.get_file()
    if text == regex.sub("Bridge ", text):
        with open(bridges_file, "w", encoding="utf-8") as file:
            file.write(text)
    else:
        dialog = ui.get("BridgErrorDialog")
        dialog.show()


def connect(action: str, app) -> None:
    """
    connect or disconnect
    """
    task = Popen(
        [config.COMMAND, action, "--verbose"],
        stdout=PIPE,
        start_new_session=True,
    )
    if action == "start":
        config.dconf.set_int("pid", task.pid)
    elif checks.proxy_set():
        proxy.proxy_unset()
    app.io_in = GLib.io_add_watch(task.stdout, GLib.IO_IN, set_progress)
    GLib.io_add_watch(task.stdout, GLib.IO_HUP, thread_finished, app)


def set_progress(stdout, *_) -> bool:
    """
    set progress output on UI
    """
    try:
        line = stdout.readline().decode("utf-8")
        ui.add_to_terminal(line[5:-5])
        if "Bootstrapped" in line:
            valid = re.compile(r".*Bootstrapped .+% \(.*\): ")
            notice = valid.sub("", line)[:-5]
            ui.set_description(notice)
            percentage = line.split(" ")[5]
            ui.set_progress_bar(int(percentage[:-1]))
    except ValueError:
        return False
    return True


def thread_finished(stdout, condition, app) -> bool:
    """
    things to do after process finished
    """
    if condition:
        GLib.source_remove(app.io_in)
        stdout.close()
        ui.set_run_status(app)
        return False
    return True


def connected_hup(stdout, condition, app) -> bool:
    """
    return connection status
    """
    if condition:
        result = stdout.readline().decode("utf-8")
        if "True" in result:
            toast = config._("Tractor is connected")
            ui.set_orbi("run")
        else:
            toast = config._("Tractor couldn't connect")
            ui.set_orbi("dead")
        ui.notify(toast)
        GLib.source_remove(app.io)
        stdout.close()
        return True
    return False
