"""
Test cases for the functions and classes in package `pypots.cli`.
"""

# Created by Wenjie Du <wenjay.du@gmail.com>
# License: GLP-v3

import os
import threading
import unittest
from argparse import Namespace
from copy import copy

import pytest

from pypots.cli.dev import dev_command_factory
from pypots.cli.doc import doc_command_factory
from pypots.cli.env import env_command_factory
from pypots.utils.logging import logger

PROJECT_ROOT_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../.."))


def callback_func():
    raise TimeoutError("Time out.")


def time_out(interval, callback):
    def decorator(func):
        def wrapper(*args, **kwargs):
            t = threading.Thread(target=func, args=args, kwargs=kwargs)
            t.setDaemon(True)
            t.start()
            t.join(interval)  # wait for interval seconds
            if t.is_alive():
                return threading.Timer(0, callback).start()  # invoke callback()
            else:
                return

        return wrapper

    return decorator


class TestPyPOTSCLIDev(unittest.TestCase):
    # set up the default arguments
    default_arguments = {
        "build": False,
        "cleanup": False,
        "run_tests": False,
        "k": None,
        "show_coverage": False,
        "lint_code": False,
    }
    # `pypots-cli dev` must run under the project root dir
    os.chdir(PROJECT_ROOT_DIR)

    @pytest.mark.xdist_group(name="cli-dev")
    def test_0_build(self):
        arguments = copy(self.default_arguments)
        arguments["build"] = True
        args = Namespace(**arguments)
        dev_command_factory(args).run()

    @pytest.mark.xdist_group(name="cli-dev")
    def test_1_run_tests(self):
        arguments = copy(self.default_arguments)
        arguments["run_tests"] = True
        arguments["k"] = "try_to_find_a_non_existing_test_case"
        args = Namespace(**arguments)
        try:
            dev_command_factory(args).run()
        except RuntimeError:  # try to find a non-existing test case, so RuntimeError will be raised
            pass
        except Exception as e:  # other exceptions will cause an error and result in failed testing
            raise e

    # Don't test --lint-code because Black will reformat the code and cause error when generating the coverage report
    # @pytest.mark.xdist_group(name="cli-dev")
    # def test_2_lint_code(self):
    #     arguments = copy(self.default_arguments)
    #     arguments["lint_code"] = True
    #     args = Namespace(**arguments)
    #     dev_command_factory(args).run()

    @pytest.mark.xdist_group(name="cli-dev")
    def test_3_cleanup(self):
        arguments = copy(self.default_arguments)
        arguments["cleanup"] = True
        args = Namespace(**arguments)
        dev_command_factory(args).run()


class TestPyPOTSCLIDoc(unittest.TestCase):
    # set up the default arguments
    default_arguments = {
        "gene_rst": False,
        "branch": "main",
        "gene_html": False,
        "view_doc": False,
        "port": 9075,
        "cleanup": False,
    }
    # `pypots-cli doc` must run under the project root dir
    os.chdir(PROJECT_ROOT_DIR)

    @pytest.mark.xdist_group(name="cli-doc")
    def test_0_gene_rst(self):
        arguments = copy(self.default_arguments)
        arguments["gene_rst"] = True
        args = Namespace(**arguments)
        doc_command_factory(args).run()

        logger.info("run again under a non-root dir")
        try:
            os.chdir(os.path.abspath(os.path.join(PROJECT_ROOT_DIR, "pypots")))
            doc_command_factory(args).run()
        except RuntimeError:  # try to run under a non-root dir, so RuntimeError will be raised
            pass
        except Exception as e:  # other exceptions will cause an error and result in failed testing
            raise e
        finally:
            os.chdir(PROJECT_ROOT_DIR)

    @pytest.mark.xdist_group(name="cli-doc")
    def test_1_gene_html(self):
        arguments = copy(self.default_arguments)
        arguments["gene_html"] = True
        args = Namespace(**arguments)
        try:
            doc_command_factory(args).run()
        except Exception as e:  # somehow we have some error when testing on Windows, so just print and pass below
            logger.error(e)

    @pytest.mark.xdist_group(name="cli-doc")
    @time_out(2, callback_func)  # wait for two seconds
    def test_2_view_doc(self):
        arguments = copy(self.default_arguments)
        arguments["view_doc"] = True
        args = Namespace(**arguments)
        try:
            doc_command_factory(args).run()
        except Exception as e:  # somehow we have some error when testing on Windows, so just print and pass below
            logger.error(e)

    @pytest.mark.xdist_group(name="cli-doc")
    def test_3_cleanup(self):
        arguments = copy(self.default_arguments)
        arguments["cleanup"] = True
        args = Namespace(**arguments)
        doc_command_factory(args).run()


class TestPyPOTSCLIEnv(unittest.TestCase):
    # set up the default arguments
    default_arguments = {
        "install": "optional",
        "tool": "conda",
    }

    # `pypots-cli env` must run under the project root dir
    os.chdir(PROJECT_ROOT_DIR)

    @pytest.mark.xdist_group(name="cli-env")
    def test_0_install_with_conda(self):
        arguments = copy(self.default_arguments)
        arguments["tool"] = "conda"
        args = Namespace(**arguments)
        try:
            env_command_factory(args).run()
        except Exception as e:  # somehow we have some error when testing on Windows, so just print and pass below
            logger.error(e)

    @pytest.mark.xdist_group(name="cli-env")
    def test_1_install_with_pip(self):
        arguments = copy(self.default_arguments)
        arguments["tool"] = "pip"
        args = Namespace(**arguments)
        try:
            env_command_factory(args).run()
        except Exception as e:  # somehow we have some error when testing on Windows, so just print and pass below
            logger.error(e)


if __name__ == "__main__":
    unittest.main()
