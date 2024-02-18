import os
import subprocess
from time import sleep

import inquirer
from rich import print
from rich.console import Console
from rich.table import Table
from typer import Context, Exit, Option, Typer

from izio_cli import __version__
from izio_cli.helper.console_helper import create_table
from izio_cli.helper.pattern_helper import getPath, newModule, newPage
from izio_cli.helper.project_helper import (
    getPlatforms,
    getProjectName,
    getProjectPath,
    setupWorkflows,
)
from izio_cli.helper.strings_transformers import to_pascal_case, to_snake_case
from izio_cli.pattern.dot_net_pattern import createNetCoreSolution, addReferences
from izio_cli.pattern.flutter_pattern import (
    create_page,
    createFlutterProj,
    getFlutterPages,
    getModules,
)
from izio_cli.pattern.flutter_pattern import new_module as flutter_new_module

console = Console()
app = Typer()


def version_func(flag):
    if flag:
        print(__version__)
        raise Exit(code=0)


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    version: bool = Option(False, callback=version_func, is_flag=True),
):
    message = """Usage: [b]izio_cli [SUBCOMANDO] [ARGUMENTOS][/]

 There are some subcommands available:

- [b]new-module[/]: Create new module for flutter project
- [b]new-page[/]: Create new module for flutter project

[b]usage Exampless:[/]
izio create-module --module "my module"
izio create-page --page "my page"

[b]to more quick info: [red]izio --help[/]

# [b]Para informações detalhadas: [blue][link=http://notas-musicais.readthedocs.io]acesse a documentação![/]
"""
    if ctx.invoked_subcommand:
        return
    console.print(message)


@app.command()
def new_module(
    path: str = Option("", "--path", "-p", help="Path to the flutter project"),
    module: str = Option("", "--module", "-m", help="Module name"),
):
    """
    Create a new module within a Flutter project.

    This command prompts the user to select or create a new module for a specified Flutter project.
    It also provides an option to create a new page in the module after creation.

    Attributes:
        path (str): The path to the Flutter project. If left empty, the user will be prompted.
        module (str): The name of the module to create. If left empty, the user will be prompted.

    Examples:

        izio new-module --module "my Module" --path "path/to/flutter/project"
        {create a new module in the flutter project called "my_module"}

    """
    # Verify if the path exists
    path = getPath(path)

    # Create a list of modules
    modules = getModules(path)
    if not module:
        module = inquirer.list_input("Select a module", choices=modules)

        if module == "Cancel":
            raise Exit(code=0)

        if module == "New Module":
            module = newModule(modules)
            result = flutter_new_module(path, module)
            console.print(create_table(result))
    else:
        module = newModule(modules, module)
        result = flutter_new_module(path, module)
        console.print(create_table(result))

    confirm = inquirer.confirm(
        f"Do you want to create a new page in module {module}?", default=True
    )
    if not confirm:
        raise Exit(code=0)
    else:
        new_page(path, module=module, page="")

    return module


@app.command()
def new_page(
    path: str = Option("", "--path", "-p", help="Path to the flutter project"),
    module: str = Option("", "--module", "-m", help="Module name"),
    page: str = Option("", "--page", "-p", help="Page name"),
):
    """
    Create a new page within a module of a Flutter project.

    This command allows the creation of a new page in a specified module of a Flutter project.
    If module or page names are not provided, the user will be prompted.

    Args:

        path (str): The path to the Flutter project. If left empty, the user will be prompted.
        module (str): The name of the module where the page will be created. If left empty, the user will be prompted.
        page (str): The name of the page to be created. If left empty, the user will be prompted.

    Examples:

        izio createpage --module "my_module" --page "my_page" --path "path/to/flutter/project"
    """

    # Verify if the path exists
    path = getPath(path)

    # Create a list of modules
    modules = getModules(path)

    if not module:
        module = inquirer.list_input("Select a module", choices=modules)

        if module == "Cancel":
            raise Exit(code=0)

        if module == "New Module":
            module = newModule(modules)
            result = flutter_new_module(path, module)
            console.print(create_table(result))
    else:
        # Verify if the module exists
        module = to_snake_case(module)

        if module not in modules:
            module = newModule(modules, module)
            result = flutter_new_module(path, module)
            console.print(create_table(result))

    if not page:
        page = inquirer.text("Enter the page name")
        page = to_pascal_case(page)
        print(f"Page name: {page}")
    else:
        page = to_pascal_case(page)

    pages = getFlutterPages(path, module)
    page = newPage(pages=pages, module=module, page=page)
    create_page(path, module, page)

    return page


@app.command()
def new_project(
    path: str = Option("", "--path", "-p", help="Path to the flutter project"),
    type: str = Option(
        "", "--type", "-t", help="Type of the project (flutter, netCore)"
    ),
    solution: str = Option(
        "IzPay",
        "--solution",
        "-s",
        help="What is the solution you are working on, like: Mangos, Loyalty, IzPay, etc",
    ),
    projectName: str = Option("", "--project-name", "-n", help="Name of the project"),
    platforms: str = Option("", "--platforms", "-l", help="Platforms"),
    description: str = Option(
        "", "--description", "-d", help="Description of the project"
    ),
):
    """Create a new Izio project of either Flutter or .NET type.
    This command initializes a new project, allowing the user to specify various details like project name, type, platforms, and description. The project type can be either Flutter or .NET.

    Attributes:
        path (str): The path where the project will be created. If left empty, the user will be prompted.
        type (str): The type of the project ('flutter' or 'netCore'). If left empty, the user will be prompted.
        solution (str): The solution name for the project. Default is 'IzPay'.
        projectName (str): The name of the project. If left empty, the user will be prompted.
        platforms (str): The platforms for the Flutter project (e.g., 'android,ios,web').
        description (str): A description of the project. If left empty, the user will be prompted.

    Examples:
        ```shell
        izio new-project -n "my_project" -s IzPay -d "my description" -p "path/to/project" -l "android,ios,web"
        {create a new flutter project in Mb.IzPay.flutter.my_project for android, ios, web}
        ```

        ```shell
        izio new-project -t netCore -n "my_dot_det_project" -s IzPay -d "my description" -p "path/to/project" -l "android,ios,web"
        {create a new flutter project in Be.IzPay.netCore.my_dot_det_project for android, ios, web}
        ```
    """

    if not type:
        type = inquirer.list_input(
            "Select the type of project",
            choices=["flutter", "netCore"],
            default="flutter",
        )

    if not projectName:
        confirm, projectName = getProjectName()
        if not confirm or not projectName:
            confirm, projectName = getProjectName()
            if not confirm:
                raise Exit(code=1)
            if not projectName:
                raise ValueError("Project name is required")
    else:
        projectName = to_snake_case(projectName)

    if not description:
        description = inquirer.text("Enter the project description")

    if not path:
        path = getProjectPath(projectName, type=type)
    else:
        path = getProjectPath(projectName, path, type=type)

    if not platforms and type == "flutter":
        platforms = getPlatforms()

    # do not create a new project in the izio_cli folder
    if path != "/Users/saulosenoski/Development/Izio/izio_cli":
        if type == "flutter":
            setupWorkflows(path, projectName, console)
            createFlutterProj(path, projectName, platforms, description, console)
        elif type == "netCore":
            createNetCoreSolution(path, projectName, solution, console)
        else:
            raise ValueError("Type of project not supported")


@app.command(hidden=True)
def testCommand():
    print(os.name)
