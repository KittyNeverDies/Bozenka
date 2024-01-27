import os

import git


repo = git.Repo(path="D:\\Files\\Documents\\GitHub\\Bozenka")
build = repo.heads[0].commit.hexsha
diff = repo.git.log([f"HEAD..origin/{repo.active_branch}", "--oneline"])
is_updated = True if not diff else False
