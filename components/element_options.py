def element_options(options):
    if isinstance(options, dict):
        return [{"label": key, "value": val}
                for key, val in options.items()]
    else:
        return [{"label": x, "value": x}
                for x in options]
