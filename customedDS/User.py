from customedDS.CustomSet import CustomSet

class User:
    """
    User class representing a social media user.

    Attributes:
    - user_id (int): The unique identifier for the user.
    - name (str): The name of the user.
    - followers (CustomSet): A set containing user IDs of followers.
    - posts (list): A list containing the user's posts.

    Methods:
    - add_follower(follower_id): Add a follower to the user.
    - add_post(post): Add a post to the user's posts.
    """

    def __init__(self, user_id, name):
        """
        Initialize a User instance.

        Parameters:
        - user_id (int): The unique identifier for the user.
        - name (str): The name of the user.
        """
        self.user_id = user_id
        self.name = name
        self.followers = CustomSet()
        self.posts = []

    def add_follower(self, follower_id):
        """
        Add a follower to the user.

        Parameters:
        - follower_id: The user ID of the follower to be added.
        """
        self.followers.add(follower_id)

    def add_post(self, post):
        """
        Add a post to the user's posts.

        Parameters:
        - post: The post to be added to the user's posts.
        """
        self.posts.append(post)
