import dotenv
import subprocess
import tomli
import os


if __name__ == '__main__':
    assert dotenv.load_dotenv('.env')

    with open('../pyproject.toml', 'r') as file:
        toml = tomli.loads(file.read())

    VERSION: str = toml['project']['version']
    PYPI_USERNAME: str = os.getenv('PYPI_USERNAME')
    PYPI_PASSWORD: str = os.getenv('PYPI_PASSWORD')

    commands = [
        'python -m build ../ --outdir ../dist',
        f'python -m twine upload ../dist/apidevtools-{VERSION}* -u{PYPI_USERNAME} -p{PYPI_PASSWORD}'
    ]
    for command in commands:
        print(f'{command}')
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = process.communicate()
        print(f'{out.decode()}')
