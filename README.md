# poopbox
> Develop locally, build and test remotely.

## What is it?

`poopbox` is a tool designed to facilitate building on a remote workstation.
It lets you run tools seamlessly in a remote environment just by placing a YAML
file in the root of your home directory.

### Example

Create a `.poopfile` in the project's root directory:
```
denbeigh at local in ~/build/my_funky_project 
$ cat .poopfile
# vi:syntax=yaml

target:
  excludes:
    - env
    - deps
    - .poopfile
  run:
    type: ssh
    opts:
      hostname: remote
      remote_dir: build/my_funky_project

  sync:
    type: rsync
    opts:
      hostname: remote
      remote_dir: build/my_funky_project
```

Run `poopbox init`. This creates the necessary directories, and tests the host is reachable.
Here we also verify an empty build directory was created with `poopbox shell` - note the
change in hostname.
```
denbeigh at local in ~/dev/my_funky_project
$ ssh remote ls build/my_funky_project 
ls: cannot access 'build/my_funky_project': No such file or directory

denbeigh at local in ~/dev/my_funky_project
$ poopbox init
poopbox is ready to rock n' roll!

denbeigh at local in ~/dev/my_funky_project
$ poopbox shell

denbeigh at remote in ~/build/my_funky_project 
$ ls -a
.  ..
```

Run any required pre-setup for the remote server. `p` or `poopbox push` and `poopbox shell`
may be helpful tools in doing this.
Note running our initalisation script with `p` has installed `deps` on the remote machine,
and not moved them back to the local machine. It has also 
```
denbeigh at local in ~/dev/my_funky_project (env) 
$ p ./init.sh 

denbeigh at local in ~/dev/my_funky_project (env) 
$ p ls -a
.
..
deps
init.sh
lint.sh
project

denbeigh at local in ~/dev/my_funky_project (env) 
$ ls -a
.  ..  env  init.sh  lint.sh  .poopfile  project
```

`poopbox` works out-of-the-box with any host that is able to be reached over ssh.
If you can run `ssh $YOUR_MACHINE` successfully, `$YOUR_MACHINE` can be used in the
`hostname` fields.

Alternatively, if you prefer to use something other than ssh/rsync for eiter

`poopbox` does not concern itself with provisioning - large users should be using
custom config management for their fleet, and small users are likely to have a
long-lived or relatively-easily reproducible environments.
`poopbox shell` can also be used for initial manual configuration of a fresh environment.

## How do I use it?

Create a `.poopfile` in the root of your project directory, see the `sample.poopfile`
for an example.

```
target:
  excludes:
    - env
    - .poopfile
    - .git
    - '*egg_info*'
    - '*__pycache__*'
    - '*.mypy_cache*'
  run:
    type: ssh
    opts:
      hostname: <YOUR_BUILD_SERVER_SSH_DEST_HERE>
      remote_dir: <YOUR_REMOTE_BUILD_DIR_HERE>

  sync:
    type: rsync
    opts:
      hostname: <YOUR_BUILD_SERVER_SSH_DEST_HERE>
      remote_dir: <YOUR_REMOTE_BUILD_DIR_HERE>
```

For very heavyweight use cases, the rsync-based syncing method can be replaced with something
more efficient.
