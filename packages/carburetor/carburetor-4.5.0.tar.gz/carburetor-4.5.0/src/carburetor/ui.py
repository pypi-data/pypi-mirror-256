# Part of Carburetor project
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020-2023.

"""
handle ui related stuff
"""

from gi.repository import Adw, Gdk, Gio, Gtk
from tractor import checks, control, db

from . import config
from . import handler


def initialize_builder() -> None:
    """
    connect builder to files and handlers
    """
    resource = Gio.resource_load(config.s_data_dir + "/res.gresource")
    Gio.resources_register(resource)
    prefix = "/io/frama/tractor/carburetor/gtk/"
    builder.add_from_resource(prefix + "main.ui")
    builder.add_from_resource(prefix + "preferences.ui")
    builder.add_from_resource(prefix + "help-overlay.ui")


def get(obj: str):
    """
    get object from ui
    """
    return builder.get_object(obj)


def css() -> None:
    """
    apply css to ui
    """
    css_provider = Gtk.CssProvider()
    prefix = "/io/frama/tractor/carburetor/gtk/"
    css_provider.load_from_resource(prefix + "style.css")
    display = Gdk.Display.get_default()
    Gtk.StyleContext.add_provider_for_display(
        display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
    )


def notify(text: str) -> None:
    """
    show toast
    """
    overlay = get("ToastOverlay")
    toast = Adw.Toast()
    toast.set_title(text)
    overlay.add_toast(toast)


def set_orbi(state: str) -> None:
    """
    Set the main window icon
    """
    page = get("MainPage")
    match state:
        case "load":
            page.set_icon_name("orbistarting")
        case "dead":
            page.set_icon_name("orbidead")
        case "stop":
            page.set_icon_name("orbioff")
        case "run":
            page.set_icon_name("orbion")


def set_description(text: str) -> None:
    """
    set description on main page
    """
    page = get("MainPage")
    page.set_description(text)


def set_progress_bar(percentage: int) -> None:
    """
    set progressbar percentage
    """
    progress_bar = get("ProgressBar")
    fraction = float(percentage) / 100
    progress_bar.set_fraction(fraction)


def add_to_terminal(line: str) -> None:
    """
    add line to termianl in sidebar overlay
    """
    if line.startswith("2") or line.startswith("3m"):
        line = line[2:]  # temporary workaround for color characters
    terminal_text = get("TermText")
    buffer = terminal_text.get_buffer()
    buffer.insert(buffer.get_end_iter(), f"\n{line}\n")


def set_to_stopped(app) -> None:
    """
    set status to stopped
    """
    page = get("MainPage")
    set_orbi("stop")
    page.set_title(config._("Stopped"))
    page.set_description("")
    button = get("SplitButton")
    text_start = config._("_Connect")
    style = button.get_style_context()
    style.remove_class("destructive-action")
    style.add_class("suggested-action")
    button.set_label(text_start)
    action_menu = button.get_popover()
    action_menu.set_sensitive(False)
    button = get("CancelButton")
    button.set_visible(False)
    dconf = config.dconf
    dconf.reset("pid")
    if app:  # don't run on startup
        notify(config._("Tractor is stopped"))


def set_to_running(app) -> None:
    """
    set status to connected
    """
    page = get("MainPage")
    get_listener = control.get_listener
    set_orbi("run")
    page.set_title(config._("Running"))
    page.set_description(
        f"{config._('Socks Port')}: {get_listener('socks')[1]}\n"
        f"{config._('DNS Port')}: {get_listener('dns')[1]}\n"
        f"{config._('HTTP Port')}: {get_listener('httptunnel')[1]}\n"
    )
    button = get("SplitButton")
    text_stop = config._("_Disconnect")
    style = button.get_style_context()
    style.remove_class("suggested-action")
    style.add_class("destructive-action")
    button.set_label(text_stop)
    action_menu = button.get_popover()
    action_menu.set_sensitive(True)
    button = get("CancelButton")
    button.set_visible(False)
    if app:  # don't run on startup
        notify(config._("Tractor is running"))


def set_run_status(app=None) -> None:
    """
    set status of conection
    """
    if checks.running():
        set_to_running(app)
    else:
        set_to_stopped(app)
    button = get("SplitButton")
    button.set_sensitive(True)
    progress_bar = get("ProgressBar")
    progress_bar.hide()


def set_pluginrow_sensivity(row=None) -> None:
    """
    set row sensitive if a plugable transport is set
    """
    if not row:
        row = get("PluginRow")
    bridgetype = db.get_val("bridge-type")
    if bridgetype > 1:
        row.set_sensitive(True)
    else:
        row.set_sensitive(False)


def setup_pluginbutton(button=None) -> None:
    """
    set plugin button label and chooser
    """
    if not button:
        button = get("PluginButton")
    chooser = get("PluginChooser")
    filename = Gio.File.new_for_path(db.get_val("plugable-transport"))
    if filename.query_exists():
        basename = filename.get_basename()
        chooser.set_initial_file(filename)
    else:
        basename = config._("None")
    button.set_label(basename)
    button.chooser = chooser


builder = Gtk.Builder(scope_object_or_map=handler)
ui_dir = config.s_data_dir + "/ui"
