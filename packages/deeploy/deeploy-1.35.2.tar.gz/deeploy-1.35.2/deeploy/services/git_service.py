class GitService(object):
    """
    A class for interacting with a local Git project
    """

    def __init__(self, local_repository_path: str) -> None:
        """Initialise the Git client"""
        from git import Remote, Repo

        self.repository: Repo = Repo(local_repository_path)
        self.branch = self.repository.active_branch
        self.remote: Remote = self.repository.remote("origin")

        if not self.__is_valid_git_project():
            raise Exception("Not a valid git project")

    def get_remote_url(self) -> str:
        return self.remote.url

    def __is_valid_git_project(self) -> bool:
        """Check if the supplied repository is valid"""
        return not self.repository.bare
