"""
3A - Arrange - act - assert
"""
import os

import fitz
from pytest import raises

from note_extractor.noteextractor import NoteExtractor

scriptdir = os.path.abspath(os.path.dirname(__file__))
filename = os.path.join(scriptdir, 'resources', 'PDF_WIKI.pdf')
filename_config = os.path.join(scriptdir, 'resources', 'cfg.json')
print(scriptdir)

# Tests for add_pdf
def test_add_pdf_must_return_an_error_when_file_do_not_exist():
    # Arrange
    filename = os.path.join(
        scriptdir, 'resources', 'this_file_do_not_exist.pdf'
    )
    error_msg = 'This file does not exist.'

    with raises(ValueError) as error:
        NoteExtractor(file=filename)
        assert error_msg == error.value.args[0]
    print(error)


def test_add_pdf_must_return_an_error_when_file_is_not_pdf():
    # Arrange
    filename = os.path.join(scriptdir, 'resources', 'background.png')
    error_msg = 'This is not a PDF file.'

    with raises(ValueError) as error:
        NoteExtractor(file=filename)
        assert error_msg == error.value.args[0]
    print(error)


def test_add_pdf_must_return_an_error_when_load_folder():
    # Arrange
    filename = os.path.join(scriptdir, 'resources')
    error_msg = 'This path is a folder.'

    with raises(ValueError) as error:
        NoteExtractor(file=filename)
        assert error_msg == error.value.args[0]
    print(error)


def test_add_pdf_must_return_an_error_when_loads_empty_file():
    # Arrange
    filename = os.path.join(scriptdir, 'resources', 'empty_file.pdf')
    error_msg = 'Cannot open empty PDF.'

    with raises(ValueError) as error:
        NoteExtractor(file=filename)
        assert error_msg == error.value.args[0]
    print(error)


# Tests for config file
def test_add_config_must_return_an_error_when_file_do_not_exist():
    # Arrange
    filename_config = os.path.join(scriptdir, 'resources', 'not_exist.json')
    error_msg = f'The config file "{filename_config}" file does not exist.'
    default_load = NoteExtractor(file=filename)

    with raises(ValueError) as error:
        default_load.add_config(filename_config)
        assert error_msg == error.value.args[0]
    print(error)


def test_add_config_must_return_an_error_when_file_is_not_json():
    # Arrange
    filename_config = os.path.join(scriptdir, 'resources', 'background.png')
    error_msg = f'The config file "{filename_config}" file does not exist.'

    with raises(ValueError) as error:
        default_load = NoteExtractor(file=filename)
        default_load.add_config(filename_config)
        assert error_msg == error.value.args[0]
    print(error)


def test_add_config_must_return_an_error_when_load_folder():
    # Arrange
    filename_config = os.path.join(scriptdir, 'resources')
    error_msg = 'This path is a folder.'

    with raises(ValueError) as error:
        default_load = NoteExtractor(file=filename)
        default_load.add_config(filename_config)
        assert error_msg == error.value.args[0]
    print(error)


def test_add_config_must_return_an_error_when_loads_empty_file():
    # Arrange
    filename_config = os.path.join(scriptdir, 'resources', 'empty_config.json')
    error_msg = 'Cannot open empty config.'

    with raises(ValueError) as error:
        default_load = NoteExtractor(file=filename)
        default_load.add_config(filename_config)
        assert error_msg == error.value.args[0]
    print(error)
