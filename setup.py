"""Various setup utilities."""

import os
import subprocess

import distutils.cmd
from setuptools import setup
from server import news_fetcher


def run_command(command, shell=False):
    try:
        subprocess.check_call(command, shell=shell)
    except subprocess.CalledProcessError as e:
        print command, " failed with exit code ", e.returncode
        return False
    return True


class TestCommand(distutils.cmd.Command):
    description = "Runs the linter and all the tests."
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        if run_command("flake8 server/"):
            run_command("py.test --cov=server", shell=True)


class UpdateDatabaseCommand(distutils.cmd.Command):
    """Runs Flake8 linter on all of the Python source files."""

    description = 'Updates the database.'
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run the command."""
        news_fetcher.update_database()


def read(file_name):
    """Read the file with a relative path to this file."""
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name="MuDimA",
    version="0.0.1",
    author="MuDimA Team",
    author_email="mmw125@gmail.com",
    description="Mutidimensional News Analysis.",
    license="GNU",
    keywords="news analysis",
    url="https://github.com/mmw125/MuDimA",
    packages=['server'],
    long_description=read('README.md'),
    cmdclass={
        'update_database': UpdateDatabaseCommand,
        'test': TestCommand,
    },

)
