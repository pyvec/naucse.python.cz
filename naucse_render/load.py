from pathlib import Path
import functools

import yaml


@functools.lru_cache()
def _read_yaml(path):
    print('Loading', path)
    with path.open(encoding='utf-8') as f:
        return yaml.safe_load(f)


def read_yaml(*path_parts):
    base_path = Path('.').resolve()

    yaml_path = base_path.joinpath(*path_parts).resolve()

    # Guard against '..' in the course_slug
    if base_path not in yaml_path.parents:
        raise ValueError(f'Invalid course path')

    return dict(_read_yaml(yaml_path))
