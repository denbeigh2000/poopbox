# poopbox
> Develop locally, build and test remotely.

## What is it?

`poopbox` is a tool designed to facilitate building on a remote workstation.
It lets you run tools seamlessly in a remote environment just by placing a YAML
file in the root of your home directory.

## Quickstart
```
$ cp poopbox/sample.poopfile $MY_REPOSITORY_ROOT/.poopfile

# update your remote host and build directory
$ cd $MY_REPOSITORY/ && vim .poopfile

# make sure your machine is sshable and has a valid directory
$ ssh YOUR_REMOTE_HOST mkdir -p YOUR REMOTE_DIRECTORY

# write code
$ vim mycode.py

# execute commands remotely!
$ p python test_my_code.py

# open an interactive shell!
$ poopbox shell
```
