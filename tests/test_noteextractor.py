"""
3A - Arrange - act - assert
"""
import copy
import os
import re
import shutil

import fitz
from pytest import raises

import note_extractor.utils as ne_utils
from note_extractor.noteextractor import NoteExtractor

scriptdir = os.path.abspath(os.path.dirname(__file__))
filename = os.path.join(scriptdir, 'resources', 'PDF_WIKI.pdf')
filename_zero_highlights = os.path.join(
    scriptdir, 'resources', 'PDF_WIKI_zero_highlights.pdf'
)
filename_config = os.path.join(scriptdir, 'resources', 'cfg.json')
imported_template = os.path.join(
    scriptdir, 'resources', 'imported_template.txt'
)
folder_name = os.path.join(scriptdir, 'resources', 'folder_name')
print(scriptdir)

if os.path.exists('path'):
    shutil.rmtree('path')

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


def test_count_highlights_must_correct_number_of_highlights():
    number_highlights_file = 22
    loaded_notes = NoteExtractor(filename)
    verified_number_annotations = loaded_notes.count_highlights
    print(number_highlights_file)
    assert number_highlights_file == verified_number_annotations


def test_note_exctract_must_have_intersection_level_argument():
    error_msg = 'Intersection level needed.'

    with raises(ValueError) as error:
        NoteExtractor(filename).notes_extract()
        assert error_msg == error.value.args[0]


def test_note_exctract_must_have_intersection_level_argument():
    error_msg = 'Intersection level must be beteween 0.0 and 1.0.'
    intersection_level = 5.0

    with raises(ValueError) as error:
        NoteExtractor(filename).notes_extract(intersection_level)
        assert error_msg == error.value.args[0]


def test_note_exctract_must_have_intersection_level_double_argument():
    error_msg = 'Intersection level must be beteween 0.0 and 1.0.'
    intersection_level = 5.0

    with raises(ValueError) as error:
        NoteExtractor(filename).notes_extract(intersection_level)
        assert error_msg == error.value.args[0]


def test_note_extract_must_create_highlight_files_with_n_entries():
    intersection_level = 0.5
    loaded_notes = NoteExtractor(filename)
    loaded_notes.notes_extract(intersection_level)
    highlights = loaded_notes.highlights
    number_highlights_file = loaded_notes.count_highlights
    assert number_highlights_file == len(highlights)


def test_import_template_path_must_exist():
    error_msg = 'This file does not exist.'
    template_not_exist = os.path.join(
        scriptdir, 'resources', 'not_exist_imported_template.txt'
    )

    with raises(ValueError) as error:
        loaded_notes = NoteExtractor()
        loaded_notes.import_template(template_not_exist)
        assert error_msg == error.value.args[0]


def test_import_template_moved_file():
    loaded_notes = NoteExtractor()
    template_folders = loaded_notes.config['TEMPLATE_FOLDER']
    template_folder_name = os.path.join(template_folders, 'folder_name/')
    if os.path.exists(template_folder_name):
        shutil.rmtree(template_folder_name)
    loaded_notes.import_template(imported_template)
    assert 'imported_template.txt' in loaded_notes.templates


def test_import_template_file_and_folder():
    # Name of the folder name
    folder_name_base = os.path.basename(folder_name)
    loaded_notes = NoteExtractor()
    template_folders = loaded_notes.config['TEMPLATE_FOLDER']
    template_folder_name = os.path.join(template_folders, 'folder_name/')
    if os.path.exists(template_folder_name):
        shutil.rmtree(template_folder_name)
    loaded_notes.import_template(imported_template)
    loaded_notes.import_template(folder_name)
    assert os.path.exists(template_folder_name)
    assert 'imported_template.txt' in loaded_notes.templates
    assert folder_name_base not in loaded_notes.templates


def test_import_template_folder():
    folder_name_base = os.path.basename(folder_name)
    loaded_notes = NoteExtractor()
    template_folders = loaded_notes.config['TEMPLATE_FOLDER']
    files_folder = os.listdir(template_folders)
    template_folder_name = os.path.join(template_folders, 'folder_name/')
    if os.path.exists(template_folder_name):
        os.removedirs(template_folder_name)
    loaded_notes.import_template(folder_name)
    print(files_folder)
    print(loaded_notes.templates)
    assert os.path.exists(template_folder_name)


def test_remove_template_must_work():
    loaded_notes = NoteExtractor()
    loaded_notes.import_template(imported_template)
    assert 'imported_template.txt' in loaded_notes.templates
    loaded_notes.remove_template('imported_template.txt')
    assert 'imported_template.txt' not in loaded_notes.templates


def test_remove_template_error_name_not_exist():
    error_msg = 'This template does not exist.'
    loaded_notes = NoteExtractor()
    with raises(ValueError) as error:
        loaded_notes.remove_template('template_does_not_exist.txt')
        assert error_msg == error.value.args[0]


def test_rename_template_must_work():
    loaded_notes = NoteExtractor()
    loaded_notes.import_template(imported_template)
    assert 'imported_template.txt' in loaded_notes.templates
    loaded_notes.rename_template('imported_template.txt', 'novo_template.txt')
    print(loaded_notes.config)
    assert 'novo_template.txt' in loaded_notes.templates


def test_rename_template_error_name_not_exist():
    error_msg = 'This template does not exist.'
    loaded_notes = NoteExtractor()
    with raises(ValueError) as error:
        loaded_notes.rename_template(
            'imported_template.txt', 'novo_template.txt'
        )
        assert error_msg == error.value.args[0]


def test_adjust_date_must_work():
    loaded_notes = NoteExtractor(filename)
    loaded_notes.notes_extract()
    loaded_notes.adjust_date()
    highlights = loaded_notes.highlights
    for annot in highlights:
        date_created = re.sub('D:', '', annot['created'])
        date_modified = re.sub('D:', '', annot['modified'])
        regex_pattern_date = (
            '([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2})([0-9]{2}).*'
        )
        regex_export_date = r'\1-\2-\3 \4:\5:\6'
        date_created = re.sub(
            regex_pattern_date, regex_export_date, date_created
        )
        date_modified = re.sub(
            regex_pattern_date, regex_export_date, date_modified
        )
        assert annot['created'] == date_created
        assert annot['modified'] == date_modified


def test_adjust_color_to_names():
    loaded_notes = NoteExtractor(filename)
    loaded_notes.notes_extract()
    loaded_notes.adjust_color()
    highlights = loaded_notes.highlights
    for annot in highlights:
        color = annot['color']
        color_hls = ne_utils.convert_to_hls(color)
        colors = ne_utils.colors_names(color_hls)
        assert colors == annot['color_name']


def test_adjust_text():
    loaded_notes = NoteExtractor(filename)
    loaded_notes.notes_extract()
    loaded_notes.adjust_text()
    highlights = loaded_notes.highlights
    for annot in highlights:
        text = annot['content']
        text = ne_utils.cleanup_text(text)
        text = ne_utils.merge_lines(captured_text=text, remove_hyphens=True)
        assert text == annot['content']


def test_extract_image_without_annotations():
    resource_folder = os.path.join(scriptdir, 'resources', 'location')
    img_folder_name = 'imgs'
    image_folder = os.path.join(resource_folder, img_folder_name)

    if os.path.exists(resource_folder):
        shutil.rmtree(resource_folder)

    os.mkdir(resource_folder)
    os.mkdir(image_folder)

    loaded_notes = NoteExtractor(filename_zero_highlights)
    loaded_notes.notes_extract()
    loaded_notes.extract_image(
        location=resource_folder, folder=img_folder_name
    )

    assert 1 == 1


def test_extract_image():
    resource_folder = os.path.join(scriptdir, 'resources', 'location')
    img_folder_name = 'imgs'
    image_folder = os.path.join(resource_folder, img_folder_name)

    if os.path.exists(resource_folder):
        shutil.rmtree(resource_folder)

    os.mkdir(resource_folder)
    os.mkdir(image_folder)

    loaded_notes = NoteExtractor(filename)
    loaded_notes.notes_extract()
    loaded_notes.extract_image(
        location=resource_folder, folder=img_folder_name
    )
    highlights = loaded_notes.highlights

    for annot in highlights:
        has_img = annot['has_img']
        if has_img:
            img_path = os.path.join(resource_folder, annot['img_path'])
            print(img_path)
            assert os.path.exists(img_path)
            assert os.path.isfile(img_path)


def test_extract_image_folder_dont_exists():
    resource_folder = os.path.join(scriptdir, 'resources', 'location')
    img_folder_name = 'imgs'
    image_folder = os.path.join(resource_folder, img_folder_name)

    if os.path.exists(resource_folder):
        shutil.rmtree(resource_folder)

    loaded_notes = NoteExtractor(filename)
    loaded_notes.notes_extract()
    loaded_notes.extract_image(
        location=resource_folder, folder=img_folder_name
    )
    highlights = loaded_notes.highlights

    for annot in highlights:
        has_img = annot['has_img']
        if has_img:
            img_path = os.path.join(resource_folder, annot['img_path'])
            print(img_path)
            assert os.path.exists(img_path)
            assert os.path.isfile(img_path)


def test_extract_ink():
    resource_folder = os.path.join(scriptdir, 'resources', 'location')
    img_folder_name = 'ink'
    image_folder = os.path.join(resource_folder, img_folder_name)

    if os.path.exists(resource_folder):
        shutil.rmtree(resource_folder)

    os.mkdir(resource_folder)
    os.mkdir(image_folder)

    loaded_notes = NoteExtractor(filename)
    loaded_notes.notes_extract()
    loaded_notes.extract_ink(location=resource_folder, folder=img_folder_name)
    highlights = loaded_notes.highlights

    for annot in highlights:
        has_img = annot['has_img']
        if has_img:
            img_path = os.path.join(resource_folder, annot['img_path'])
            print(img_path)
            assert os.path.exists(img_path)
            assert os.path.isfile(img_path)


def test_extract_ink_folder_dont_exist():
    resource_folder = os.path.join(scriptdir, 'resources', 'location')
    img_folder_name = 'ink'
    image_folder = os.path.join(resource_folder, img_folder_name)

    if os.path.exists(resource_folder):
        shutil.rmtree(resource_folder)

    loaded_notes = NoteExtractor(filename)
    loaded_notes.notes_extract()
    loaded_notes.extract_ink(location=resource_folder, folder=img_folder_name)
    highlights = loaded_notes.highlights

    for annot in highlights:
        has_img = annot['has_img']
        if has_img:
            img_path = os.path.join(resource_folder, annot['img_path'])
            print(img_path)
            assert os.path.exists(img_path)
            assert os.path.isfile(img_path)


def test_reorder_notes_custom():
    criteria = ['page', 'start_xy']
    loaded_notes = NoteExtractor(filename)
    loaded_notes.notes_extract()
    highlights = loaded_notes.highlights
    original_descending = copy.deepcopy(highlights)
    original_ascending = copy.deepcopy(highlights)
    loaded_notes.reorder_custom(criteria)
    highlights = loaded_notes.highlights
    original_descending = ne_utils.annots_reorder_custom(
        original_descending, criteria, ascending=False
    )
    original_ascending = ne_utils.annots_reorder_custom(
        original_ascending, criteria
    )
    for i in range(0, len(highlights)):
        content = highlights[i]['content']
        original_content = original_ascending[i]['content']
        assert content == original_content

    loaded_notes.reorder_custom(criteria, ascending=False)
    highlights = loaded_notes.highlights

    for i in range(0, len(highlights)):
        content = highlights[i]['content']
        original_content = original_descending[i]['content']
        assert content == original_content
