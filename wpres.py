import click, sh, json, sys

strip_end_char = lambda string: str(string)[:-1]

@click.group()
def cli():
    """This script will save the current state of open windows in a JSON
    object, or load such a state and apply it to open windows."""
    pass

def get_window_ids_list():
    return map(strip_end_char, sh.lsw())

@cli.command()
@click.argument('target', nargs=1, type=click.File('w'))
def save(target):
    """Saves the current window state as a JSON object."""
    windows = get_window_ids_list()

    window_attrs_dict = {}
    for window_id in windows:
        window_attrs = strip_end_char(sh.wattr('bxywh', window_id))
        attr_dict = dict(zip(
                    ['border','x','y','width','height'],
                    map(lambda attr: int(attr), window_attrs.split(' '))))
        window_attrs_dict[window_id] = attr_dict

    target.write(json.dumps(window_attrs_dict))

def apply_window_attrs(window_id, x, y, width, height, border):
    sh.wtp(x, y, width, height, window_id)
    sh.chwb('-s', border, window_id)

@cli.command()
@click.argument('target', nargs=1, type=click.File('r'))
@click.option('--merge/--fail-on-mismatch', default=True,
                help="Whether to only alter windows whose attributes are "
                     "described in the input state object, or whether to "
                     "fail when windows with ids other than those in the "
                     "input state object exist; defaults to only affecting "
                     "existing windows.")
def load(target, merge):
    """Applies a saved window state to the current window state."""
    existing_windows = get_window_ids_list()

    target_contents = target.read()
    load_state = json.loads(target_contents)

    if merge:
        apply_to_ids = set(load_state.keys()) & set(existing_windows)
    else:
        if list(existing_windows) != list(load_state.keys()):
            sys.exit(1)
        else:
            apply_to_ids = list(load_state.keys())

    for window_id in apply_to_ids:
        apply_window_attrs(window_id, **load_state[window_id])
