import logging
import dotenv
import subprocess
import tomli
import os


if __name__ == '__main__':
    assert dotenv.load_dotenv('.env')

    with open('../pyproject.toml', 'r') as file:
        toml = tomli.loads(file.read())

    VERSION: str = toml['project']['version']
    PYPI_USERNAME: str = '__token__'
    PYPI_PASSWORD: str = os.getenv('PYPI_TOKEN')

    commands = [
        {'orig': 'python -m build ../ --outdir ../dist', 'alt': 'Building...'},
        {'orig': f'python -m twine upload ../dist/apidevtools-{VERSION}* -u{PYPI_USERNAME} -p{PYPI_PASSWORD}', 'alt': 'Uploading...'}
    ]
    for command in commands:
        logging.info(command['alt'])
        process = subprocess.Popen(command['orig'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = process.communicate()
        print(f'{out.decode()}')
