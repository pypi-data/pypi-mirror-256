from logger import logger
import lastversion
import download
class Get:
    def __init__(self, repo):
        self.repo = repo
        logger.debug('repo set to %(repo)s')

    def version(self):
        try:
            version = lastversion.latest(self.repo)
            assert version is not None
            return version
        except AssertionError:
            logger.debug('repo (%(repo)s) not found?')




