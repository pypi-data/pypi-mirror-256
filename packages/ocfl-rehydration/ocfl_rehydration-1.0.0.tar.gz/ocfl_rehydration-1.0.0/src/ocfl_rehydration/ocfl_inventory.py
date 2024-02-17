import re
import json


import json
import re

class OcflInventory():
    """
    A class representing an OCFL inventory.

    Attributes:
    - inventory (dict): The inventory represented as a dictionary.
    """

    def __init__(self, file):
        """
        Initializes an OcflInventory object.

        Args:
        - file (file): The file object containing the inventory data.
        """
        self.inventory = json.load(file)
        

    def get_descriptor_path(self):
        """
        Returns the path to the descriptor file for the object.

        Returns:
        - str: The path to the descriptor file.

        Raises:
        - Exception: If the descriptor file is not found.
        """
        path_regex = r'^v[0-9]{5}/content/descriptor/.*_mets.xml'
        manifest_files = self._get_manifest_files(path_regex)

        if len(manifest_files) > 0:
            return sorted(manifest_files, reverse=True)[0]

        raise Exception("not-found, descriptor")


    def get_data_path(self, file_id):
        """
        Returns the path to the data file for the given file ID.

        Args:
        - file_id (str): The ID of the file.

        Returns:
        - str: The path to the data file.

        Raises:
        - Exception: If the data file is not found.
        """
        path_regex = r'^data/' + file_id + r'.*'
        digest = self._get_state_files_digest(path_regex=path_regex, version=None)
        return self._get_manifest_path(digest)


    def _get_state_files_digest(self, path_regex, version):
        if version is None:
            version = self.inventory['head']

        state = self.inventory['versions'][version]['state']

        if not isinstance(state, dict):
            raise Exception('Invalid state')

        for digest in state:
            for file in state[digest]:
                if (re.search(path_regex, file)):
                    return digest

        raise Exception("not-found, state file digest for: {} : {}".format(version, path_regex))

    def _get_manifest_path(self, digest):
        manifest = self.inventory['manifest']

        if not isinstance(manifest, dict):
            raise Exception('Invalid manifest')

        for file in manifest[digest]:
            return file

        raise Exception("not-found, manifest file for digest: {}".format(digest))

    def _get_manifest_files(self, path_regex):
        """
        Returns a set of file paths that match the given regular expression.

        Args:
        - path_regex (str): The regular expression to match.

        Returns:
        - set: A set of file paths that match the regular expression.

        Raises:
        - Exception: If the manifest is invalid.
        """
        manifest = self.inventory['manifest']

        if not isinstance(manifest, dict):
            raise Exception('Invalid manifest')
    
        manifest_files = set() 
        for digest in manifest:
            for file in manifest[digest]:
                if (re.search(path_regex, file)):
                    manifest_files.add(file)

        return manifest_files
