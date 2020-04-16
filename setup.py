from setuptools import setup

import pman.build_apps

CONFIG = pman.get_config()

APP_NAME = CONFIG['general']['name']

setup(
    name=APP_NAME,
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pylint',
        'pytest-pylint',
    ],
    cmdclass={
        'build_apps': pman.build_apps.BuildApps,
    },
    options={
        'build_apps': {
            'include_patterns': [
                CONFIG['build']['export_dir']+'/**',
                'keybindings.toml',
                'settings.prc',
            ],
            'exclude_patterns': [
                '**/*.py',
                '__py_cache__/**',
            ],
            'rename_paths': {
                CONFIG['build']['export_dir']: 'assets/',
            },
            'gui_apps': {
                APP_NAME: CONFIG['run']['main_file'],
            },
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
            'icons': {
                'run_game': [
                   'assets/icons/icon-256.png',
                   'assets/icons/icon-128.png',
                   'assets/icons/icon-64.png',
                   'assets/icons/icon-48.png',
                   'assets/icons/icon-32.png'
                ]
            },
            'log_filename': '$USER_APPDATA/gridfly/output.log',
        },
    }
)