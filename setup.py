from setuptools import setup

setup(
    name='wpres',
    py_modules=['wpres'],
    install_requires=[
        'Click',
        'sh'
    ],
    entry_points='''
        [console_scripts]
        wpres=wpres:cli
    '''
)
