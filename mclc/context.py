from pathlib import Path

src_dir = Path('.').joinpath('mcl-src').absolute()

btru = None

blks = {
    'system-init': src_dir.joinpath('system-init'),
    'system-mainloop': src_dir.joinpath('system-mainloop')
}