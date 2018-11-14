# poopbox
> Develop locally, build and test remotely.

## What is it?

`poopbox` is a tool designed to facilitate building on a remote workstation.
It lets you run tools seamlessly in a remote environment just by placing a YAML
file in the root of your home directory.

## Quickstart
```
$ cp poopbox/sample.poopfile $MY_REPOSITORY/.poopfile

# update your remote host and build directory
$ cd $MY_REPOSITORY/ && vim .poopfile

# write code
$ vim myproject/mycode.py

# execute commands remotely
$ p python setup.py develop
$ p pytest myproject

# open an interactive shell
$ poopbox shell
```
