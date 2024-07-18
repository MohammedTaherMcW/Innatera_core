# Copyright (c) 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=line-too-long,too-many-arguments,too-many-locals


import json
import os
import shutil

import click

from platformio import fs
from platformio.package.commands.install import install_project_dependencies
from platformio.package.manager.platform import PlatformPackageManager
from platformio.platform.exception import UnknownBoard
from platformio.platform.factory import PlatformFactory
from platformio.project.config import ProjectConfig
from platformio.project.exception import UndefinedEnvPlatformError
from platformio.project.helpers import is_platformio_project
from platformio.project.integration.generator import ProjectGenerator
from platformio.project.options import ProjectOptions


def validate_boards(ctx, param, value):  # pylint: disable=unused-argument
    pm = PlatformPackageManager()
    for id_ in value:
        try:
            pm.board_config(id_)
        except UnknownBoard as exc:
            raise click.BadParameter(
                "`%s`. Please search for board ID using `platformio boards` "
                "command" % id_
            ) from exc
    return value


@click.command("init", short_help="Initialize a project or update existing")
@click.option(
    "--project-dir",
    "-d",
    default=os.getcwd,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
)
@click.option(
    "--spine-dir",
    "-sl",
    default=None,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
)
@click.option(
    "-b", "--board", "boards", multiple=True, metavar="ID", callback=validate_boards
)
@click.option("--ide", type=click.Choice(ProjectGenerator.get_supported_ides()))
@click.option("-e", "--environment", help="Update existing environment")
@click.option(
    "-O",
    "--project-option",
    "project_options",
    multiple=True,
    help="A `name=value` pair",
)
@click.option("--sample-code", is_flag=True)
@click.option("--no-install-dependencies", is_flag=True)
@click.option("--env-prefix", default="")
@click.option("-s", "--silent", is_flag=True)
def project_init_cmd(
    project_dir,
    spine_dir,
    boards,
    ide,
    environment,
    project_options,
    sample_code,
    no_install_dependencies,
    env_prefix,
    silent,
):
    project_dir = os.path.abspath(project_dir)
    is_new_project = not is_platformio_project(project_dir)
    if is_new_project:
        if not silent:
            print_header(project_dir)
        init_base_project(project_dir, spine_dir)

    with fs.cd(project_dir):
        if environment:
            update_project_env(environment, project_options)
        elif boards:
            update_board_envs(project_dir, boards, project_options, env_prefix)

        generator = None
        config = ProjectConfig.get_instance(os.path.join(project_dir, "platformio.ini"))
        if ide:
            config.validate()
            # init generator and pick the best env if user didn't specify
            generator = ProjectGenerator(config, environment, ide, boards)
            if not environment:
                environment = generator.env_name

        # resolve project dependencies
        if not no_install_dependencies and (environment or boards):
            install_project_dependencies(
                options=dict(
                    project_dir=project_dir,
                    environments=[environment] if environment else [],
                    silent=silent,
                )
            )

        if environment and sample_code:
            init_sample_code(config, environment)

        if generator:
            if not silent:
                click.echo(
                    "Updating metadata for the %s IDE..." % click.style(ide, fg="cyan")
                )
            generator.generate()

        if is_new_project:
            init_cvs_ignore()

    if not silent:
        print_footer(is_new_project)

def print_header(project_dir):
    click.echo("The following files/directories have been created in ", nl=False)
    try:
        click.secho(project_dir, fg="cyan")
    except UnicodeEncodeError:
        click.secho(json.dumps(project_dir), fg="cyan")
    click.echo("%s - Put project header files here" % click.style("include", fg="cyan"))
    click.echo(
        "%s - Put project specific (private) libraries here"
        % click.style("lib", fg="cyan")
    )
    click.echo("%s - Put project source files here" % click.style("src", fg="cyan"))
    click.echo(
        "%s - Project Configuration File" % click.style("platformio.ini", fg="cyan")
    )


def print_footer(is_new_project):
    action = "initialized" if is_new_project else "updated"
    return click.secho(
        f"Project has been successfully {action}!",
        fg="green",
    )


def init_base_project(project_dir, spine_dir):
# def init_base_project(project_dir, spine_dir):
    with fs.cd(project_dir):
        config = ProjectConfig()
        config.save()
        dir_to_readme = [
            (config.get("platformio", "src_dir"), init_talamo_scripts),
            (config.get("platformio", "include_dir"), init_include_readme),
            (config.get("platformio", "lib_dir"), init_lib_readme),
            (config.get("platformio", "test_dir"), init_test_readme),
            (project_dir + "/talamo", None),
            (project_dir + "/config", init_config_script),
            (project_dir + "/", init_makefile_script),
        ]
        for path, cb in dir_to_readme:
            if os.path.isdir(path):
                if cb:
                    cb(path)
                continue
            os.makedirs(path)
            if cb:
                cb(path)
        init_add_spine_folder(project_dir, spine_dir)


def init_config_script(config_dir):
    with open(
        os.path.join(config_dir, "app_defconfig"), mode="w", encoding="utf8"
    ) as fp:
        fp.write(
            """CONFIG_ENABLE_FPU=y
CONFIG_RISCV_ISA_C=y
CONFIG_CONSOLE_ENABLE=y
CONFIG_LOG_LEVEL_INFO=y
CONFIG_PLL_INIT=y
CONFIG_T1_CPR=y
CONFIG_CYCLE_COUNTER_CV32E40P=y
CONFIG_GPIO=y
CONFIG_UART=y
CONFIG_CROSS_COMPILE="$(HOME)/.platformio/packages/toolchain-spine/bin/riscv32-corev-elf-"
            """
        )


def init_makefile_script(make_dir):
    with open(os.path.join(make_dir, "Makefile"), mode="w", encoding="utf8") as fp:
        fp.write(
            """
# Makefile

# Define the build directory
BUILD_DIR ?= $(CURDIR)/.pio/build/innetra_board

# Spine directory
export SPINE_DIR := $(HOME)/.platformio/packages/framework-innetra

# Object files
obj-y += src/main.o

VPATH += src

# Application name
export APP := $(notdir $(CURDIR))

# Include the wrapper Makefile
-include $(SPINE_DIR)/scripts/Makefile.wrapper

            """
        )


def init_talamo_scripts(talamo_dir):
    import os
    import subprocess

    with open(os.path.join(talamo_dir, "main.c"), mode="w", encoding="utf8") as fp:
        fp.write(
            """
/**
 * @file
 *
 * @brief Hello World T1 application
 *
 * This application only sends text to the console to demonstrate
 * the build and boot flow for the T1 processor.
 *
 * @copyright (C) Copyright 2024 Innatera Nanosystems B.V.
 **/
#include "utils/console_io.h"
#include "drivers/inn_hal.h"
#include "drivers/inn_cpr.h"

#define TYPER_SPEED_MS  30
#define CURSOR_DELAY_MS 300

static void typer(const char *str)
{
    while (*str) {
        print_char(*str++);
        hal_delay_ms(TYPER_SPEED_MS);
    }
}

static void blinking_cursor(unsigned int reps)
{
    for (int n = 0; n < reps; n++) {
        print_char('_');
        hal_delay_ms(CURSOR_DELAY_MS);
        print_char('\\b');
        print_char(' ');
        print_char('\\b');
        hal_delay_ms(CURSOR_DELAY_MS);
    }
}

int main(void)
{
    typer("___\\n");
    typer("\\nWelcome Innaterian!");
    blinking_cursor(1);
    typer("\\n");
    blinking_cursor(3);
    typer("\\nThis is a demonstration of the build and boot flow for the");
    typer("\\nInnatera's Spiking Neural Processor T1, the ultra-low power");
    typer("\\nneuromorphic microcontroller for always-on sensing applications.");
    blinking_cursor(2);
    typer("\\n");
    typer("\\nThe processor uses an ultra-low-power spiking neural network");
    typer("\\nengine and a nimble RISC-V processor core to form a single-chip");
    typer("\\nsolution for processing sensor data quickly and efficiently.");
    blinking_cursor(2);
    typer("\\n");
    typer("\\nThe development kit contains more applications that demonstrate");
    typer("\\nthe capabilities of the Neural Network accelerators available in T1.");
    blinking_cursor(1);
    typer("\\n");
    typer("\\nHave fun spiking!");
    blinking_cursor(2);
    typer("\\n\\n");

    print_string(" _|_|_|  _|      _|  _|      _|    _|_|    _|_|_|_|_|  _|_|_|_|  _|_|_|      _|_|   \\n");
    print_string("   _|    _|_|    _|  _|_|    _|  _|    _|      _|      _|        _|    _|  _|    _| \\n");
    print_string("   _|    _|  _|  _|  _|  _|  _|  _|_|_|_|      _|      _|_|_|    _|_|_|    _|_|_|_| \\n");
    print_string("   _|    _|    _|_|  _|    _|_|  _|    _|      _|      _|        _|    _|  _|    _| \\n");
    print_string(" _|_|_|  _|      _|  _|      _|  _|    _|      _|      _|_|_|_|  _|    _|  _|    _| \\n");

    return 0;
}
"""
        )
    with open(os.path.join(talamo_dir, "Makefile"), mode="w", encoding="utf8") as fp:
        fp.write(
            """
obj-y := main.o

##################################
# Kbuild application targets
##################################


export SPINE_DIR := $(realpath ../../dependency)


export APP := $(notdir $(shell pwd))


-include $(SPINE_DIR)/scripts/Makefile.wrapper

            """
        )


def init_add_spine_folder(project_dir, spine_dir):
    spine_source_location = os.path.abspath(spine_dir) if spine_dir else '/home/inesh/spine_default'
    symlink_location = os.path.join(project_dir, 'spine')
    
    if os.path.exists(symlink_location):
        os.remove(symlink_location)

    os.symlink(spine_source_location, symlink_location)
    print(f"Created symlink from {spine_source_location} to {symlink_location}")


def init_include_readme(include_dir):
    with open(os.path.join(include_dir, "README"), mode="w", encoding="utf8") as fp:
        fp.write(
            """
This directory is intended for project header files.

A header file is a file containing C declarations and macro definitions
to be shared between several project source files. You request the use of a
header file in your project source file (C, C++, etc) located in `src` folder
by including it, with the C preprocessing directive `#include'.

```src/main.c

#include "header.h"

int main (void)
{
 ...
}
```

Including a header file produces the same results as copying the header file
into each source file that needs it. Such copying would be time-consuming
and error-prone. With a header file, the related declarations appear
in only one place. If they need to be changed, they can be changed in one
place, and programs that include the header file will automatically use the
new version when next recompiled. The header file eliminates the labor of
finding and changing all the copies as well as the risk that a failure to
find one copy will result in inconsistencies within a program.

In C, the usual convention is to give header files names that end with `.h'.
It is most portable to use only letters, digits, dashes, and underscores in
header file names, and at most one dot.

Read more about using header files in official GCC documentation:

* Include Syntax
* Include Operation
* Once-Only Headers
* Computed Includes

https://gcc.gnu.org/onlinedocs/cpp/Header-Files.html
""",
        )


def init_lib_readme(lib_dir):
    with open(os.path.join(lib_dir, "README"), mode="w", encoding="utf8") as fp:
        fp.write(
            """
This directory is intended for project specific (private) libraries.
PlatformIO will compile them to static libraries and link into executable file.

The source code of each library should be placed in an own separate directory
("lib/your_library_name/[here are source files]").

For example, see a structure of the following two libraries `Foo` and `Bar`:

|--lib
|  |
|  |--Bar
|  |  |--docs
|  |  |--examples
|  |  |--src
|  |     |- Bar.c
|  |     |- Bar.h
|  |  |- library.json (optional, custom build options, etc) https://docs.platformio.org/page/librarymanager/config.html
|  |
|  |--Foo
|  |  |- Foo.c
|  |  |- Foo.h
|  |
|  |- README --> THIS FILE
|
|- platformio.ini
|--src
   |- main.c

and a contents of `src/main.c`:
```
#include <Foo.h>
#include <Bar.h>

int main (void)
{
  ...
}

```

PlatformIO Library Dependency Finder will find automatically dependent
libraries scanning project source files.

More information about PlatformIO Library Dependency Finder
- https://docs.platformio.org/page/librarymanager/ldf.html
""",
        )


def init_test_readme(test_dir):
    with open(os.path.join(test_dir, "README"), mode="w", encoding="utf8") as fp:
        fp.write(
            """
This directory is intended for PlatformIO Test Runner and project tests.

Unit Testing is a software testing method by which individual units of
source code, sets of one or more MCU program modules together with associated
control data, usage procedures, and operating procedures, are tested to
determine whether they are fit for use. Unit testing finds problems early
in the development cycle.

More information about PlatformIO Unit Testing:
- https://docs.platformio.org/en/latest/advanced/unit-testing/index.html
""",
        )


def init_cvs_ignore():
    conf_path = ".gitignore"
    if os.path.isfile(conf_path):
        return
    with open(conf_path, mode="w", encoding="utf8") as fp:
        fp.write(".pio\n")


def update_board_envs(project_dir, boards, extra_project_options, env_prefix):
    config = ProjectConfig(
        os.path.join(project_dir, "platformio.ini"), parse_extra=False
    )
    used_boards = []
    for section in config.sections():
        cond = [section.startswith("env:"), config.has_option(section, "board")]
        if all(cond):
            used_boards.append(config.get(section, "board"))

    pm = PlatformPackageManager()
    modified = False
    for id_ in boards:
        board_config = pm.board_config(id_)
        if id_ in used_boards:
            continue
        used_boards.append(id_)
        modified = True

        envopts = {"platform": board_config["platform"], "board": id_}
        # find default framework for board
        frameworks = board_config.get("frameworks")
        if frameworks:
            envopts["framework"] = frameworks[0]

        for item in extra_project_options:
            if "=" not in item:
                continue
            _name, _value = item.split("=", 1)
            envopts[_name.strip()] = _value.strip()

        section = "env:%s%s" % (env_prefix, id_)
        config.add_section(section)

        for option, value in envopts.items():
            config.set(section, option, value)

    if modified:
        config.save()


def update_project_env(environment, extra_project_options=None):
    if not extra_project_options:
        return
    env_section = "env:%s" % environment
    option_to_sections = {"platformio": [], env_section: []}
    for item in extra_project_options:
        assert "=" in item
        name, value = item.split("=", 1)
        name = name.strip()
        destination = env_section
        for option in ProjectOptions.values():
            if option.scope in option_to_sections and option.name == name:
                destination = option.scope
                break
        option_to_sections[destination].append((name, value.strip()))

    config = ProjectConfig(
        "platformio.ini", parse_extra=False, expand_interpolations=False
    )
    for section, options in option_to_sections.items():
        if not options:
            continue
        if not config.has_section(section):
            config.add_section(section)
        for name, value in options:
            config.set(section, name, value)

    config.save()


def init_sample_code(config, environment):
    try:
        p = PlatformFactory.from_env(environment)
        return p.generate_sample_code(config, environment)
    except (NotImplementedError, UndefinedEnvPlatformError):
        pass

    framework = config.get(f"env:{environment}", "framework", None)
    if framework != ["arduino"]:
        return None
    main_content = """
#include <Arduino.h>

// put function declarations here:
int myFunction(int, int);

void setup() {
  // put your setup code here, to run once:
  int result = myFunction(2, 3);
}

void loop() {
  // put your main code here, to run repeatedly:
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}
"""
    is_cpp_project = p.name not in ["intel_mcs51", "ststm8"]
    src_dir = config.get("platformio", "src_dir")
    main_path = os.path.join(src_dir, "main.%s" % ("cpp" if is_cpp_project else "c"))
    if os.path.isfile(main_path):
        return None
    if not os.path.isdir(src_dir):
        os.makedirs(src_dir)
    with open(main_path, mode="w", encoding="utf8") as fp:
        fp.write(main_content.strip())
    return True
