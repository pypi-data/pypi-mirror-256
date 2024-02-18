import os
import shutil
from booyah.generators.helpers.io import print_error, print_success
from booyah.generators.base_generator import BaseGenerator
from booyah.generators.helpers.path import new_migration_file_path

BOOYAH_ATTACHMENT_FIELDS = [
    'record_id:integer',
    'record_type',
    'name',
    'key',
    'filename',
    'extension',
    'byte_size:integer',
]

MIGRATION_TEMPLATE_NAME = 'create_table_booyah_attachments.py'
ATTACHMENT_TYPES = ['file', 'image', 'pdf', 'doc', 'attachment']
    
def file_extensions_for(format):
    if format == 'image':
        return ['.png', '.jpg', '.jpeg', '.ico', '.gif', '.bmp']
    elif format == 'pdf':
        return ['.pdf']
    elif format == 'doc':
        return ['.doc', '.rtf', '.docx', '.pdf', '.txt']
    return ['*']

def is_file_field(format):
    return format in ATTACHMENT_TYPES

def attachment_import_string():
    return 'from booyah.models.booyah_attachment import BooyahAttachment'

def attachment_config_prefix(model_name, name):
    return f'BooyahAttachment.configure({model_name}, \'{name}\','

def attachment_config_string(model_name, name, format, bucket):
    file_extensions = file_extensions_for(format)
    if file_extensions:
        return f'{attachment_config_prefix(model_name, name)} bucket=\'{bucket}\', file_extensions={file_extensions})'
    else:
        return f'{attachment_config_prefix(model_name, name)} bucket=\'{bucket}\')'

#  booyah g attachments install
class AttachmentsGenerator(BaseGenerator):
    def __init__(self, target_folder, command, extra_arguments):
        self.target_folder = target_folder
        self.command = command

    def perform(self):
        if self.command == 'install':
            self.install()
        else:
            print(f'Command not found {self.command}')
    
    def install(self):
        print('Installing attachments')
        files_in_folder = os.listdir(self.target_folder)
        
        already_exists = any(file.endswith(MIGRATION_TEMPLATE_NAME) for file in files_in_folder)

        if already_exists:
            print_error(f"Already have the attachments migration ({MIGRATION_TEMPLATE_NAME}).")
        else:
            source_file = os.path.join(self.booyah_root(), 'generators', 'templates', MIGRATION_TEMPLATE_NAME)
            target_file = new_migration_file_path(self.target_folder, MIGRATION_TEMPLATE_NAME)
            shutil.copy2(source_file, target_file)
            print_success('Migration for attachments created successfully!')
        