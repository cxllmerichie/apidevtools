from argparse import ArgumentParser as _ArgumentParser
from zipfile import ZipFile as _ZipFile
from os import rename as _rename


def create(path: str = '.', name: str = 'template'):
    with _ZipFile('template.zip', 'r') as template_zip_file:
        template_zip_file.extractall(path)
    _rename(f'{path}\\template', f'{path}\\{name}')


if __name__ == '__main__':
    parser = _ArgumentParser()
    parser.add_argument('--path')
    parser.add_argument('--name')
    args = parser.parse_args()
    args = {'path': args.path, 'name': args.name}

    create(args.get('path'), args.get('name'))
