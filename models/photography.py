class PhotoObject:
    """
    Simple class to hold all information about single photo
    """

    def __init__(self):
        # Relative url. Need this to retrieve email ID or more specific details.
        # BEAWARE! this can be deleted for old photos
        self.url = None
        self.author = None  # Name of photographer as shown in the intranet website
        self.title = None  # Photo caption
        self.total_votes = None  # Total number of votes (if any)
        self.average_votes = None  # Average votes (if any)
        self.creation_date = None  # Date of photo upload
        self.photo_url = None  # Absolute path of photo. BEAWARE! this can be deleted for old photos
        self.author_email = None  # This will not be exact email, because intranet userID's are weirdly formatted
        self.file_name = None  # Name of file in which we have saved photo on local machine

    def get_all(self) -> list:
        """
        Returns all associated information after formatting.
        This function can be directly used in printing into file
        :return: list of all the meta-data
        """
        points = "N/A"  # This is important if someone has run script before voting
        if self.total_votes is not None and self.average_votes is not None:
            points = (float(self.total_votes) * float(self.average_votes))
        else:  # if votes are not available
            self.total_votes = "N/A"
            self.average_votes = "N/A"
        return [self.author,
                self.author_email,
                points,
                self.title,
                self.url,
                self.total_votes,
                self.average_votes,
                self.creation_date,
                self.photo_url]
