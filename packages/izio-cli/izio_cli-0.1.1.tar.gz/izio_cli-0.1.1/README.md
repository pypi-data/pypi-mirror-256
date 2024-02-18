# Izio CLI Project

## Description

Izio CLI is a comprehensive command-line interface tool designed to facilitate the management and automation of various aspects of Izio&Co software development projects, particularly focused on Flutter and .NET Core solutions. It streamlines the process of setting up new projects, modules, and pages, handling project dependencies, and maintaining a consistent project structure.

## Features

### Flutter Project Management

>Easily create new Flutter projects with predefined modules and pages.

### .NET Core Solution Setup

> Initialize .NET Core solutions with standard project structure and dependencies.

### Project Automation

> Automate repetitive tasks such as creating submodules, adding references, and more.

## Installation

To install the Izio CLI, you can use pipx to install the package from the PyPI repository. Run the following command in your terminal:

```bash
pipx install izio-cli
```

## Usage

After installing, you can use the Izio CLI commands as follows:

To create a new Flutter project:

```bash
izio new-project --project "project_name" --path "path/to/flutter/project"
```

To create a new Flutter module:

```bash
izio new-module --module "module_name" --path "path/to/flutter/project"
````

To create a new Flutter page:

```bash
izio new-page --page "page_name" --module "module_name" --path "path/to/flutter/project"
```

To create a new .NET Core solution:

```bash
izio createNetCoreSolution --projectName "project_name" --solution "solution_name"
````

For more detailed usage, refer to the Documentation.
