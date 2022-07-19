import sublime
import sublime_plugin

def updateBar(view):
    settings = sublime.load_settings("TODO.sublime-settings")
    targets = settings.get("targets")

    for target in targets:
        try:
            selector = target["selector"]
        except KeyError:
            continue

        identifier = "todo_%s" % selector

        regions = view.get_regions(identifier)

        if (len(regions) == 0):
            view.set_status(identifier, "")
            continue

        view.set_status(identifier, "%s: %i" % (selector, len(regions)))

scope_dict = {
    "red": "region.redish",
    "orange": "region.orangish",
    "yellow": "region.yellowish",
    "green": "region.greenish",
    "cyan": "region.cyanish",
    "blue": "region.bluish",
    "purple": "region.purplish",
    "pink": "region.pinkish"
}

def highlightTodos(view):
    settings = sublime.load_settings("TODO.sublime-settings")
    targets = settings.get("targets")

    if (len(targets) == 0):
        return

    for target in targets:
        try:
            selector = target["selector"]
            color = target["color"]
            to_end = target["to_end"]
        except KeyError:
            continue

        region_selector = "todo_%s" % selector
        view.erase_regions(region_selector)

        if color in scope_dict:
            color = scope_dict[color]
        else:
            continue

        if (selector.endswith(":") != True):
            selector += ":"

        if to_end == True:
            selector += ".*$"

        regions = view.find_all(selector, 0)

        view.add_regions(region_selector,
            regions,
            color,
            "fold_closed",
            512+256+32,
        )

class TODO(sublime_plugin.EventListener):
    def on_init(self, views):
        for view in views:
            highlightTodos(view)
            updateBar(view)

    def on_modified_async(self, view):
        highlightTodos(view)
        updateBar(view)

    def on_load_async(self, view):
        highlightTodos(view)
        updateBar(view)
