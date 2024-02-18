from gwss.download import download_file
import resolver

class Unpkg:

    base_url = 'https://unpkg.com'

    def __init__(self, package, version, file, s_or_s):
        """
        Make sure every filename is correct before going through the entirety
        of the function
        :param package:
        :param version:
        :param file:
        :param s_or_s:
        """
        self.package = package
        self.version = version
        self.file = file
        self.s_or_s = s_or_s

        self.url = self.base_url + "%()s"


    def unpkg_dl(self, dest_dir):
        download_file(self.url, self.package, self.file, self.version, self.s_or_s, dest_dir)
