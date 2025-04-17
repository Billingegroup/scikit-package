import re
import shutil
from pathlib import Path

import requests

# All cookie-cutter hooks run on project root, but good to enforce
ROOT = Path.cwd()


def __gen_init__(module_name):
    """Generate __init__.py file for namespace module."""
    __init__ = f"""#!/usr/bin/env python
##############################################################################
#
# (c) {% now 'utc', '%Y' %} The Trustees of Columbia University in the City of New York.
# All rights reserved.
#
# File coded by: Billinge Group members and community contributors.
#
# See GitHub contributions for a more detailed list of contributors.
# https://github.com/{{ cookiecutter.github_org }}/{{ cookiecutter.github_repo_name }}/graphs/contributors
#
# See LICENSE.rst for license information.
#
##############################################################################
\"\"\"Blank namespace package for module {module_name}.\"\"\"


from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

# End of file
"""
    return __init__


def __gen_setuppy__():
    base_module_name = "{{ cookiecutter.project_name }}".split('.')[-1].strip()
    setuppy = """#!/usr/bin/env python

# Extensions script for {{ cookiecutter.project_name }}

import os
import re
import sys
import glob
from setuptools import setup
from setuptools import Extension

# Define extension arguments here
ext_kws = {
        'libraries' : [],
        'extra_compile_args' : [],
        'extra_link_args' : [],
        'include_dirs' : [],
}

""" + f"""def create_extensions():
    \"Initialize Extension objects for the setup function.\"
    ext = Extension('{{ cookiecutter.package_dir_name }}.{base_module_name}',
                    glob.glob('src/extensions/*.cpp'),
                    **ext_kws)
    return [ext]


# Extensions not included in pyproject.toml
setup_args = dict(
    ext_modules = [],
)


if __name__ == '__main__':
    setup_args['ext_modules'] = create_extensions()
    setup(**setup_args)

"""
    return setuppy


def add_supermodules(ROOT, name):
    """Add module packages for each leading period."""
    src_dir = ROOT / "src"
    c_dir = src_dir  # Current directory

    package_dir_name = "{{ cookiecutter.package_dir_name }}"
    cp_dir = c_dir / package_dir_name  # Current package directory

    # Get the necessary modules given the period spacings
    module_names = name.split(".")
    for i, module in enumerate(module_names):
        module_names[i] = module.strip().lower()

    # The last module is not a namespace module
    ns_module_names = module_names[:-1]

    # Create a subdirectory for each parsed module
    for ns_module_name in ns_module_names:
        # Create module directory and move files
        d_dir = c_dir / ns_module_name  # Destination directory
        try:
            d_dir.mkdir(parents=False, exist_ok=False)
        # Should never occur as the parent directory is tracked by c_dir
        except FileNotFoundError:
            print(f"Parent directory {c_dir} not found. This is likely an issue with cookiecutter.")
        # Should never occur from how we do our naming
        except FileExistsError:
            print(f"Duplicate directory names {d_dir} found. This is likely an issue with cookiecutter.")
        shutil.move(cp_dir, d_dir)

        # Make __init__.py file
        init_file = d_dir / "__init__.py"
        with open(init_file, "w") as ifile:
            ifile.write(__gen_init__(ns_module_name))
        c_dir = c_dir / ns_module_name
        cp_dir = c_dir / package_dir_name

    # Rename the final destination module
    cp_dir.rename(c_dir / module_names[-1])

def wrapper_setup():
    """Generate setup.py file for C extensions."""
    src_dir = ROOT / "src"
    ext_dir = src_dir / "extensions"
    try:
        ext_dir.mkdir(parents=False, exist_ok=False)
    # Should never occur as the parent directory is src
    except FileNotFoundError:
        print(f"Parent directory {src_dir} not found. This is likely an issue with cookiecutter.")
    # Can occur if user names the package extensions
    except FileExistsError:
        print(f"Duplicate directory names {src_dir} found. You cannot name your project 'extensions*'.")

    # Make __init__.py file
    setuppy_file = ROOT / "setup.py"
    with open(setuppy_file, "w") as spfile:
        spfile.write(__gen_setuppy__())

def update_workflow():
    """Generate GitHub workflow .yml files with user input."""
    CENTRAL_REPO_ORG = "Billingegroup"
    CENTRAL_REPO_NAME = "release-scripts"
    CENTRAL_WORKFLOW_DIR = ".github/workflows/templates"
    LOCAL_WORKFLOW_DIR = ROOT / ".github" / "workflows"

    workflow_input = {"PROJECT": "{{ cookiecutter.project_name }}",
                      "GITHUB_ADMIN_USERNAME": "{{ cookiecutter.project_owner_github_username }}",
                      "C_EXTENSION": str("{{ cookiecutter.project_needs_c_code_compiled }}"=="Yes").lower(),
                      "HEADLESS": str("{{ cookiecutter.project_has_gui_tests }}"=="Yes").lower(),
                      "VERSION": "v0"}

    def get_central_workflows():
        """Get GitHub workflows from Billingegroup/release-scripts."""
        base_url = f"https://api.github.com/repos/{CENTRAL_REPO_ORG}/{CENTRAL_REPO_NAME}/contents/{CENTRAL_WORKFLOW_DIR}"
        response = requests.get(base_url, timeout=5)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch central workflows: {response.status_code}")

        workflows = {}
        for file in response.json():
            if file['type'] == 'file' and file['name'].endswith('.yml'):
                content_response = requests.get(file['download_url'], timeout=5)
                if content_response.status_code == 200:
                    workflows[file['name']] = content_response.text
        return workflows


    def update_workflow_params(content):
        """Replace placeholder parameters in workflow .yml files with user
        input."""
        def replace_match(match):
            key = match.group(1)
            return str(workflow_input[key])

        pattern = re.compile(r"\{\{\s*(\w+)\s*/\s*([^\s\}]+)\s*\}\}")
        return pattern.sub(replace_match, content)


    def update_local_workflows(central_workflows):
        """Replace existing GitHub workflow files with latest from
        Billingegroup/release-scripts."""
        local_workflows = set(f.name for f in LOCAL_WORKFLOW_DIR.glob("*.yml"))
        central_workflow_names = set(central_workflows.keys())

        for name, content in central_workflows.items():
            local_file = LOCAL_WORKFLOW_DIR / name

            content = update_workflow_params(content)

            with open(local_file, "w", encoding="utf-8") as file:
                file.write(content)

        for name in local_workflows - central_workflow_names:
            (LOCAL_WORKFLOW_DIR / name).unlink()

    try:
        LOCAL_WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)
        central_workflows = get_central_workflows()
        update_local_workflows(central_workflows)
    except Exception as e:
        print(f"Error: {str(e)}")


def main():
    """Execute when user runs cookiecutter."""
    if "." in "{{ cookiecutter.project_name }}":
        add_supermodules(ROOT, "{{ cookiecutter.package_dir_name }}")
    if "{{ cookiecutter.project_needs_c_code_compiled }}" == "Yes":
        wrapper_setup()
    update_workflow()
    print(f"""
    Congratulations! A new Python project is created!
    Enter the directory with `cd {{cookiecutter.project_name}}`.

    Are you starting a new project? Build your project and docs next:
    https://billingegroup.github.io/scikit-package/new-project-guide.html#build-project

    Are you migrating an existing project? Move files to the new directory next:
    https://billingegroup.github.io/scikit-package/migration-guide.html#move-files

    If you have any additional questions, please read our FAQ section or leave issues below:

    FAQ: https://billingegroup.github.io/scikit-package/frequently-asked-questions
    GitHub issues: https://github.com/Billingegroup/scikit-package/issues
    """)

    # Dynamically check if the user has selected a non-default Python version
    max_python_version = "3.13"
    min_pyhton_version = "3.11"

    if ("{{ cookiecutter.minimum_supported_python_version }}" != min_pyhton_version
        or "{{ cookiecutter.maximum_supported_python_version }}" != max_python_version):
        print(
            "ACTION REQUIRED (non-default Python versions): You've entered Python versions outside of the default according to "
            "https://scientific-python.org/specs/spec-0000/. Please consider specifying Python versions following the instructions in the link below:\n"
            "\nFAQ: https://Billingegroup.github.io/cookiecutter/frequently-asked-questions.html#github-actions\n"
        )

if __name__ == '__main__':
    main()
