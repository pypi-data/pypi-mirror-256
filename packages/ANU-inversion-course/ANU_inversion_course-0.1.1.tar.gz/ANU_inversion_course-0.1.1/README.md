# ANU Inversion Course Package

[![Build](https://github.com/anu-ilab/ANUInversionCourse/actions/workflows/build_wheels.yml/badge.svg?branch=main)](https://github.com/anu-ilab/ANUInversionCourse/actions/workflows/build_wheels.yml)
[![PyPI version](https://badge.fury.io/py/ANU-inversion-course.svg)](https://badge.fury.io/py/ANU-inversion-course)

This package contains resources to be used in the [inversion course practicals](https://github.com/anu-ilab/JupyterPracticals).

## Table of contents
- [Getting started](README.md#getting-started)
  - [Pre-requisites](README.md#1-pre-requisites)
  - [Set up a virtual environment (optional)](README.md#2-set-up-a-virtual-environment-optional)
  - [Installation](README.md#3-installation)
  - [Check](README.md#4-check)
- [Troubleshooting](README.md#troubleshooting)
- [Developer notes](README.md#developer-notes)

## Getting started

### 1. Pre-requisites

Before installing the `ANU-inversion-course` package, make sure you have the following ready:

- A computer with a recent OS.
- OS-specific dependencies including a system package manager:
  - For *Linux* users:
    1. Familiarise yourself with the linux system package manager `apt` / `dnf` / `pacman` / `yast` etc.
  - For *MacOS* users:
    1. Download and install `Xcode` from "App Store" (you'll need to create an Apple account if not already done)
    2. Install the Xcode command line tools by typing this in "Terminal":
       `xcode-select --install; sudo xcodebuild -license; sudo softwareinstall -i -a`
    4. Install a recent package manager e.g. one of `Anaconda` (https://www.anaconda.com/), `MacPorts` (https://www.macports.org/), `HomeBrew` (https://brew.sh/)
  - For *Windows* users:
    1. Install the `Cygwin` package manager (https://www.cygwin.com/)
- Install git, gcc, g++, gfortran and python (3.6+) using the package manager. Use the package manager search facility to find options.
- Install any other software development tools you want using the package manager.
- If necessary add your package manager installation directory to the system PATH environment variable so installed programs can/will be found.

These tools can usually be downloaded in source form and compiled however this should only be necessary if you have an unusual setup.
Don't be tempted by web sites that claim easy one step package installs, install a package manager. Package managers are far superior in almost every way.

### 2. Set up a python virtual environment [optional]

It's recommended to use a python virtual environment (e.g. [`venv`](https://docs.python.org/3/library/venv.html), [`virtualenv`](https://virtualenv.pypa.io/en/latest/), [`mamba`](https://mamba.readthedocs.io/en/latest/) or [`conda`](https://docs.conda.io/en/latest/)) so that ANU-Inversion-Course doesn't conflict with your other Python projects. 

Open a terminal (or a Cygwin shell for Windows users) and refer to the cheat sheet below for how to create, activate, exit and remove a virtual environment. `$ ` is the system prompt.

<details>
  <summary>venv</summary>

  Ensure you have and are using *python >= 3.6*. It may not be called `python` but something like `python3`, `python3.10` etc.

  Use the first two lines below to create and activate the new virtual environment. The other lines are for your
  future reference.

  ```console
  $ python -m venv <path-to-new-env>/inversion_course           # to create
  $ source <path-to-new-env>/inversion_course/bin/activate      # to activate
  $ deactivate                                                  # to exit
  $ rm -rf <path-to-new-env>/inversion_course                   # to remove
  ```
  
</details>

<details>
  <summary>virtualenv</summary>

  Use the first two lines below to create and activate the new virtual environment. The other lines are for your
  future reference.

  ```console
  $ virtualenv <path-to-new-env>/inversion_course -p=3.10       # to create
  $ source <path-to-new-env>/inversion_course/bin/activate      # to activate
  $ deactivate                                                  # to exit
  $ rm -rf <path-to-new-env>/inversion_course                   # to remove
  ```

</details>

<details>
  <summary>mamba</summary>

  Use the first two lines below to create and activate the new virtual environment. The other lines are for your
  future reference.

  ```console
  $ mamba create -n inversion_course python=3.10                # to create
  $ mamba activate inversion_course                             # to activate
  $ mamba deactivate                                            # to exit
  $ mamba env remove -n inversion_course                        # to remove
  ```

</details>

<details>
  <summary>conda</summary>

  Use the first two lines below to create and activate the new virtual environment. The other lines are for your
  future reference.

  ```console
  $ conda create -n inversion_course python=3.10                # to create
  $ conda activate inversion_course                             # to activate
  $ conda deactivate                                            # to exit
  $ conda env remove -n inversion_course                        # to remove
  ```

</details>


### 3. Installation

Type the following in your terminal (or Cygwin shell for Windows users):

```console
$ pip install jupyterlab matplotlib anu-inversion-course
```

### 4. Check
And when you run `jupyter-lab` to do the practicals, make sure you are in the same environment as where your `anu-inversion-course` was installed. You can try to test this by checking if the following commands give you similar result:

```console
$ which pip
<some-path>/bin/pip
$ which jupyter-lab
<same-path>/bin/jupyter-lab
$ pip list | grep ANU-inversion-course
ANU-inversion-course               0.1.0
```

## Troubleshooting

If you find problems *importing* `anu_inversion_course.rf`, try to search for the error message you get. [Here](https://stackoverflow.com/questions/58793399/importerror-library-not-loaded-for-f2py) contains a nice explanation for one possible cause. And here is how to locate `libgfortran`:
```console
gfortran --print-file-name libgfortran.5.dylib # macOS
```

## Developer Notes

Check out [NOTES.md](NOTES.md) if you'd like to contribute to this package.

1. [Getting started](NOTES.md#getting-started)
2. [Cheatsheet](NOTES.md#cheatsheet)
   1. [conda environment](NOTES.md#conda-environment)
   2. [git operations](NOTES.md#git-operations)
   3. [package development](NOTES.md#package-development)
   4. [package metadata](NOTES.md#package-metadata)
   5. [package building test & release](NOTES.md#package-building-test--release)
3. [Adding C/C++ extensions](NOTES.md#adding-cc-extensions)
4. [Adding Fortran extensions](NOTES.md#adding-fortran-extensions)
5. [More references](NOTES.md#more-references)
6. [Appendix - semantic versioning](NOTES.md#appendix-i---sementic-versioning)
7. [Additional Notes about gfortran](NOTES.md#additional-notes-about-gfortran)
