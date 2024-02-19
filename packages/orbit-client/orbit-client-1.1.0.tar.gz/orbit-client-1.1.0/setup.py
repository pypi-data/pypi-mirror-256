"""orbit distutils configuration."""
from setuptools import setup
VERSION = {}
with open("orbit/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = [
    'binaryornot>=0.4.4',
    'Jinja2>=2.7,<4.0.0',
    'click>=7.0,<9.0.0',
    'pyyaml>=5.3.1',
    'jinja2-time>=0.2.0',
    'python-slugify>=4.0.0',
    'requests>=2.23.0',
]

setup(
    name='orbit-client',
    version=VERSION["__version__"],
    description=(
        'A command-line utility that creates projects from project templates.'
    ),
    long_description=readme,
    long_description_content_type='text/markdown',
    author='haonv',
    url='https://gitlab.ftech.ai/nlp/va/template/orbit',
    packages=['orbit'],
    package_dir={'orbit': 'orbit'},
    entry_points={'console_scripts': ['orbit-client = orbit.__main__:main']},
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=requirements,
    license='Apache License 2.0',
    zip_safe=False,
    keywords=[
        "orbit"
        "Python",
        "projects",
        "project templates",
        "Jinja2",
        "skeleton",
        "scaffolding",
        "project directory",
        "package",
        "packaging",
    ],
)
