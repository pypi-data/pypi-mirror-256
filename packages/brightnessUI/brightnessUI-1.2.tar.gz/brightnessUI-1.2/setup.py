from setuptools import find_packages
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as file:
    LONG_DESCRIPTION = file.read()

setup(
    name='brightnessUI',
    version='1.2',

    packages=find_packages(),

    include_package_data = True,

    description='A simple UI to change screen backlight for ubuntu',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://gitee.com/shu-peixuan/brightnessUI.git',

    author='Peixuan Shu',
    author_email='shupeixuan@qq.com',
    license='BSD',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: BSD License',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Programming Language :: Python :: 3'
    ],

    keywords='A simple UI to tune screen backlight for ubuntu',

    install_requires=[
        'PyQt5',
    ],

    entry_points = {
        'console_scripts': [
            'brightness-ui = brightnessUI.main:main',
            'brightness-ui-install = brightnessUI.install.install_brightness_ui:main',
        ]
    }

    # $ sudo pip3 install -e .
)
