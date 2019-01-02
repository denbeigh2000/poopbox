# poopbox
> develop locally, build remotely.

## Must have
 - Project-local dotfile with configuration
 - Forward commands to remote machine over ssh
 - Push and pull wrappers (rsync?) to send code to/from remote machine
 - Ability to exclude directories from sync

### Command line tools
 - `p` "pee": for running a command remotely
 - `poopbox`: access to more tools - sync, push etc
    - `poopbox push` -> pushes changes to remotely
    - `poopbox pull` -> pulls changes from remote
    - `poopbox sync` -> push then pull
    - `poopbox shell` -> open interactive shell in remote target, wrapped in sync - useful for initial remote configuration
    - `poopbox config` -> get and set config options

## Should do
 - [ ] Hook interface and loading
    - [ ] Python virtualenv/setup.py hook
    - [ ] Go GOPATH/dep hook
    - [ ] Ruby/RVM hook? (i don't know much about ruby dev)
 - [ ] CLI flag to skip arguments
 - [ ] File lock
   - [ ] Sync operations
   - [ ] Interactive shell

## Nice to have
 - [x] Setup (get an environment to a working state) - Small users don't need much
        setup, most can use config management
   - [x] basic script provisioning would be good to instantiate our environment at
         the same time - `poopbox init` feels awkward
 - [x] Ability to swap out rsync for syncing (looking at you, monorepos)
 - [ ] Support [lsyncd](https://axkibe.github.io/lsyncd/) as a sync option
   - [ ] lsyncd does not support hook at the end of the sync action - it's just streaming
         files to rsync through stdin. Use [SIGSTOP/SIGCONT](https://github.com/axkibe/lsyncd/issues/432#issuecomment-294343687)?

### Perf ideas
 - [ ] Use controlmasters
 - [ ] Minimise file changes by recording sync time by [modifying file](https://stackoverflow.com/a/8986162)
 - [ ] `poopd` daemon to manage a remote work session
     - [ ] `poopd` cli tool, and associated Target
     - [ ] Manages forked processes
         - [ ] Starts tmux window in remote directory over SSH
            - [ ] Made in remote directory
            - [ ] Runs on individual remote sockfile
            - [ ] Connections made to remote tmux with [libtmux](http://libtmux.git-pull.com/en/stable/) when running
                    remote commands
             - [ ] Need to gracefully handle connection failure
         - [ ] Forks long-lived SSH session to forward local sockfile to remote
         - [ ] Forks long-lived lsyncd process
             - [ ] Generate config file from YAML
             - [ ] Ability to let user specify custom lsyncd config file?
