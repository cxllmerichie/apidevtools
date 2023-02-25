import subprocess
import os
from dotenv import load_dotenv


if __name__ == '__main__':
    assert load_dotenv('../.env')

    VERSION: str = '2.0.0'
    PYPI_USERNAME: str = os.getenv('PYPI_USERNAME')
    PYPI_PASSWORD: str = os.getenv('PYPI_PASSWORD')

    file = os.path.abspath('compose.yml')
    commands = [
        'python -m build',
        f'python -m twine upload ../dist/apidevtools-{VERSION}*'
    ]
    for command in commands:
        print(f'{command}')
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = process.communicate()
        print(f'{out.decode()}')
