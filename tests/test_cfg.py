"""
3A - Arrange - act - assert
"""
import os
import unittest

from pytest import raises

from note_extractor.cfg import Config_file

scriptdir = os.path.abspath(os.path.dirname(__file__))
filename_config = os.path.join(scriptdir, 'resources', 'cfg.json')


def test_must_set_default_cfg_when_load_no_cfg_file():
    # Arrange
    default_cfg = Config_file('').default
    print(default_cfg)
    assert Config_file().config == default_cfg


def test_return_error_if_is_folder():
    # Arrange
    filename_config = os.path.join(scriptdir, 'resources')
    error_msg = 'This is a folder, not a config json.'
    with raises(ValueError) as error:
        Config_file(filename_config)
        assert error_msg == error.value.args[0]


def test_return_error_file_dont_exist():
    # Arrange
    filename_config = os.path.join(
        scriptdir, 'resources', 'config_not_exist.json'
    )
    error_msg = 'This file does not exist.'
    with raises(ValueError) as error:
        Config_file(filename_config)
        assert error_msg == error.value.args[0]


def test_return_error_when_invalid_cfg_file():
    # Arrange
    filename_config = os.path.join(scriptdir, 'resources', 'empty_config.json')
    error_msg = 'Invalid config file.'
    with raises(ValueError) as error:
        Config_file(filename_config)
        assert error_msg == error.value.args[0]


def test_change_cfg_invalid_key():
    error_msg = 'This is not a valid key.'
    with raises(ValueError) as error:
        Config_file(filename_config).change_cfg('INVALID_KEY', 'INVALID')
        assert error_msg == error.value.args[0]


def test_change_cfg_not_valid_value():
    error_msg = 'Parameter does not exist.'
    with raises(ValueError) as error:
        Config_file(filename_config).change_cfg(1, 1)
        assert error_msg == error.value.args[0]


def test_change_cfg_invalid_type():
    error_msg = 'Invalid parameter type.'
    with raises(ValueError) as error:
        Config_file(filename_config).change_cfg('COLUMNS', 0.1)
        assert error_msg == error.value.args[0]


def test_change_cfg_valid_parameter_and_value():
    valid_parameter = 'COLUMNS'
    valid_value = 2
    cfg_test = Config_file(filename_config)
    cfg_test.change_cfg(valid_parameter, valid_value)
    assert cfg_test.config[valid_parameter] == valid_value


def test_save_folder_path():
    filename_save = os.path.join(scriptdir, 'resources', 'folder_name')
    error_msg = 'This path is a directory.'
    cfg_test = Config_file('')
    with raises(ValueError) as error:
        cfg_test.save(filename_save)
        assert error_msg == error.value.args[0]


def test_save_valid_path():
    filename_save = os.path.join(scriptdir, 'resources', 'new_file.json')
    if os.path.exists(filename_save):
        os.remove(filename_save)
    cfg_test = Config_file('')
    cfg_test.save(filename_save)
    assert os.path.exists(filename_save)


def test_validate_function():
    filename_save = os.path.join(
        scriptdir, 'resources', 'cfg_incomplete_save.json'
    )
    filename_load = os.path.join(scriptdir, 'resources', 'cfg_incomplete.json')
    if os.path.exists(filename_save):
        os.remove(filename_save)
    cfg_test = Config_file(filename_load)
    cfg_test.save(filename_save)
    assert os.path.exists(filename_save)
