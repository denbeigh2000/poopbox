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
 - [ ] Move transient operational files to .poopbox folder
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
 - [ ] Persist an SSH session to run commands with
   - [ ] Keeps an initialised shell in a detached process
   - [ ] Create hidden files in the root directory, pipe stdin/stdout/stderr through them
   - [ ] Attach to files when running next command
   - [ ] Recreate ssh connection if timed out/dead (keep pidfile)
   - [ ] We must do intelligent handling to nicely display I/O to the user
     - [ ] intercept stream, looking for sentinel chars?
 - [ ] Use controlmasters
 - [ ] Minimise file changes by recording sync time by [modifying file](https://stackoverflow.com/a/8986162)
