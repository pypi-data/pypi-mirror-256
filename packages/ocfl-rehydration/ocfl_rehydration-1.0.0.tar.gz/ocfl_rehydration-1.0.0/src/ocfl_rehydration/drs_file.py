class DrsFile:
    """
    A class representing a DRS file.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.file_id = ""
        self.file_name = ""
        self.file_dir = ""
        self.amd_ids = []

    def get_id(self):
        """
        Returns the id of this file.

        Returns:
            int: The id of this file.
        """
        return self.file_id


    def get_file_name(self):
        """
        Returns the supplied name of the file.

        Returns:
            str: The name of the file.
        """
        return self.file_name
    
    
    def get_file_dir(self):
        """
        Returns the supplied directory containing the file.

        Returns:
            str: The directory containing the file.
        """
        if self.file_dir == '/':
            return ''
        return self.file_dir
    
    def add_amd_id(self, amd_id):
        """
        Adds an amd_id to the list of amd_ids for this file.

        Args:
            amd_id (str): The amd_id to add.
        """
        self.amd_ids.append(amd_id)

    def set_id(self, file_id):
        """
        Sets the id of this file.

        Args:
            file_id (int): The id of this file.
        """
        self.file_id = file_id

    def set_file_name(self, file_name):
        """
        Sets the supplied name of the file.

        Args:
            file_name (str): The name of the file.
        """
        self.file_name = file_name

    def set_file_dir(self, file_dir):
        """
        Sets the supplied directory containing the file.

        Args:
            file_dir (str): The directory containing the file.
        """
        self.file_dir = file_dir