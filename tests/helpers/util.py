def get_formatter_options(show_source=False, output_file=None, tee=False):
    obj = object()
    obj.show_source = show_source
    obj.output_file = output_file
    obj.tee = tee
    return obj
