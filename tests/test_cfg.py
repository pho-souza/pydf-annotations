"""
3A - Arrange - act - assert
"""
import os

from pytest import raises

from note_extractor.cfg import Config_file

scriptdir = os.path.abspath(os.path.dirname(__file__))
filename = os.path.join(scriptdir, 'resources', 'cfg.json')


def test_must_set_default_cfg_when_load_no_cfg_file():
    # Arrange
    filename = ''
    default_cfg = Config_file('resources/cfg.json').default
    assert Config_file(filename).config == default_cfg
