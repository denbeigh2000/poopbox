#!/usr/bin/env python3

# from poopbox.sync import SyncTarget, SyncError
# from .git_rsyncd_lib.git_rsyncd import full_sync, sync_pull
# from .git_rsyncd_lib.mbzl import get_sync_back_globs
# 
# DEFAULT_WB_CONFIG = 'devbox/client/evil_writeback_config.py'
# 
# class GitRSyncdSyncTarget(SyncTarget):
#     def __init__(self, hostname: Text, remote_dir: Text,
#                  writeback_config: Text = DEFAULT_WB_CONFIG) -> None:
# 
#         self.writeback_config_path = writeback_config
# 
#         self.wb_files = None  # type: Optional[Text]
# 
#         super().__init__(hostname, remote_dir)
# 
#     def _push(self, files: Optional[Iterable[Text]] = None) -> None:
# 
#         raise NotImplementedError('_push() must be subclassed')
# 
#     def _pull(self, files: Optional[Iterable[Text]] = None) -> None:
#         if self.wb_files is None:
#             raise SyncError('pull operation must be done after sync')
