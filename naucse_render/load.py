from pathlib import Path
import functools
import sys

import yaml


@functools.lru_cache()
def _read_yaml(path):
    print('Loading', path, file=sys.stderr)
    with path.open(encoding='utf-8') as f:
        return yaml.safe_load(f)


def read_yaml(base_path, *path_parts, source_key=None):
    yaml_path = base_path.joinpath(*path_parts).resolve()

    # Guard against '..' in the course_slug
    if base_path not in yaml_path.parents:
        raise ValueError(f'Invalid path')

    result = dict(_read_yaml(yaml_path))
    if source_key:
        result[source_key] = '/'.join(path_parts)
    return result
