"""
3A - Arrange - act - assert
"""
import os
import shutil
import unittest
from importlib import reload

from pytest import raises

import note_extractor.utils as note_utils
from note_extractor.cfg import Config_file

scriptdir = os.path.abspath(os.path.dirname(__file__))
filename_config = os.path.join(scriptdir, 'resources', 'cfg.json')
empty_file_config = os.path.join(scriptdir, 'resources', 'empty_config.json')


def test_import_not_exist_config():
    config = note_utils.load_config_file('not_exist_file_config.txt')
    assert config.config == Config_file().config


def test_substitute_rn_linebreaks():
    """Tests if the rn linebreaks are eliminated"""
    input_string = 'aaaaaa\r\ndaadadf\r\n'
    output_string = input_string.replace('\r\n', '\n')
    assert note_utils.cleanup_text(input_string) == output_string


def test_substitute_r_linebreaks():
    input_string = 'aaaaaa\rdaadadf\r'
    output_string = input_string.replace('\r', '\n')
    assert note_utils.cleanup_text(input_string) == output_string


def test_merge_lines_empty_line():
    eval_string = 'Lorem\nipsum\n\n\naaaaa\n'
    waited_result = 'Lorem ipsum aaaaa'
    assert note_utils.merge_lines(eval_string) == waited_result


def test_colors_to_hls_list():
    color_evaluted = [1.0, 1.0, 0.0]
    hsl_color = (60 / 360, 1.0, 0.5)
    assert note_utils.convert_to_hls(color_evaluted) == hsl_color


def test_colors_to_hls_default():
    color_evaluted = (1.0, 0.5)
    hsl_color = (60 / 360, 1.0, 0.5)
    reload(note_utils)
    assert note_utils.convert_to_hls(color_evaluted) == hsl_color


def test_colors_names_default():
    """Test if the colors' are correctly setted"""
    colors_rgb = {
        'Black': [0.0, 0.0, 0.0],
        'White': [1.0, 1.0, 1.0],
        'Gray': [0.5, 0.5, 0.5],
        'Red': [1.0, 0.0, 0.0],
        'Orange': [255 / 255, 153 / 255, 0.0],
        'Yellow': [255 / 255, 255 / 255, 0.0],
        'Green': [0.0, 1.0, 0.0],
        'Cyan': [0.0, 1.0, 1.0],
        'Blue': [0.0, 0.0, 1.0],
        'Purple': [128 / 255, 0, 128 / 255],
        'Magenta': [1.0, 192 / 255, 203 / 255],
        'Magenta': [1.0, 0.0, 1.0],
        'Yellow': [1.0],
    }
    for color_name in colors_rgb:
        color_rgb = colors_rgb[color_name]
        color_hsl = note_utils.convert_to_hls(color_rgb)
        assert note_utils.colors_names(color_hsl) == color_name
    # Another red cases
    color_rgb = [1.0, 15 / 255, 20 / 255]
    color_hsl = note_utils.convert_to_hls(color_rgb)
    # Exceptional cases
    assert note_utils.colors_names(color_hsl) == 'Red'
    color_hsl = (1.0, 0.0)
    assert note_utils.colors_names(color_hsl) == 'none'
