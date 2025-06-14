import tempfile
from pathlib import Path

from scikit_package.cli.update.cf import _update_meta_yaml


def test_update_meta_yaml_realistic():
    original_meta = """{%- set version = "1.0.5" -%}
package:
  name: {{ name|lower }}
  version: {{ version }}

source:
  url: https://pypi.org/packages/source/{{ name[0] }}/{{ name }}/{{ name }}-{{ version }}.tar.gz  # noqa: E501
  sha256: 1b71d398d73800db32b09785af0e7
"""
    new_version = "1.0.6"
    new_sha256 = "123456789abcdef0123456789"
    expected_updated_meta = """{%- set version = "1.0.6" -%}
package:
  name: {{ name|lower }}
  version: {{ version }}

source:
  url: https://pypi.org/packages/source/{{ name[0] }}/{{ name }}/{{ name }}-{{ version }}.tar.gz  # noqa: E501
  sha256: 123456789abcdef0123456789
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        meta_file = Path(tmpdir) / "meta.yaml"
        meta_file.write_text(original_meta)
        _update_meta_yaml(str(meta_file), new_version, new_sha256)
        updated_meta = meta_file.read_text()
        assert updated_meta == expected_updated_meta
