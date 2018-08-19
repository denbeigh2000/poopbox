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

## Nice to have
 - Setup (get an environment to a working state) - Small users don't need much setup, most can use config management

### For bigger users
 - Ability to swap out rsync for syncing (looking at you, monorepos)
 - Some kind of syncing daemon (need file-level sync granularity)
    - fsnotify with polling fallback?
    - some kind of external syncing tool?
