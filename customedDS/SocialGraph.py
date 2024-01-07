from customedDS.CustomSet import CustomSet
from customedDS.CustomDict import CustomDict
from customedDS.User import User
from customedDS.CustomDiGraph import CustomDiGraph

class SocialGraph:
    """
    Social graph class representing a network of users and their relationships.

    Attributes:
    - users (CustomDict): A dictionary to store User objects, keyed by user ID.
    - graph (CustomDiGraph): A directed graph to represent relationships between users.

    Methods:
    - visualize_graph(): Visualize the social graph using the graph's visualization method.
    - add_user(user_id, name): Add a user to the social graph.
    - add_follower(user_id, follower_id): Add a follower to a user in the social graph.
    - add_post(user_id, post): Add a post to a user's posts in the social graph.
    - most_influential_user(): Find the most influential user in the social graph.
    - most_active_user(): Find the most active user in the social graph.
    - mutual_followers(user_id1, user_id2): Find mutual followers between two users in the social graph.
    - suggested_follows(user_id): Suggest followers for a user in the social graph.
    - search_posts_by_topic(topic): Search for posts with a specific topic in the social graph.
    - print_network_analysis(): Print a network analysis report for the social graph.
    """

    def __init__(self):
        """Initialize an empty SocialGraph."""
        self.users = CustomDict()
        self.graph = CustomDiGraph()

    def visualize_graph(self):
        """
        Visualize the social graph using matplotlib.

        Uses the well-separated layout algorithm in the graph to generate node positions.
        """
        self.graph.visualize()

    def add_user(self, user_id, name):
        """
        Add a user to the social graph.

        Parameters:
        - user_id: The unique identifier for the user.
        - name: The name of the user.
        """
        if user_id not in self.users.Keys():
            self.users.set(user_id, User(user_id, name))
            self.graph.add_node(user_id)

    def add_follower(self, user_id, follower_id):
        """
        Add a follower to a user in the social graph.

        Parameters:
        - user_id: The unique identifier for the user.
        - follower_id: The unique identifier for the follower.
        """
        if user_id in self.users.Keys():                 # and follower_id in self.users.Keys()
            temp_user = self.users.get(user_id)
            temp_user.add_follower(follower_id)
            self.users.set(user_id, temp_user)
            self.graph.add_edge(follower_id, user_id)

    def add_post(self, user_id, post):
        """
        Add a post to a user's posts in the social graph.

        Parameters:
        - user_id: The unique identifier for the user.
        - post: A dictionary representing the post with keys 'body' and 'topics'.
        """
        if user_id in self.users.Keys():
            temp_user = self.users.get(user_id)
            temp_user.add_post(post)
            self.users.set(user_id, temp_user)

    def most_influential_user(self):
        """Find the most influential user in the social graph."""
        return max(self.users.Values(), key=lambda user: len(user.followers), default=None)

    def most_active_user(self):
        """Find the most active user in the social graph."""
        active_score = CustomDict()
        for user_id, user in self.users.items():
            active_score.set(user_id, len(user.followers) + sum(len(self.users.get(follower_id).followers) for follower_id in user.followers))

        return max(active_score, key=active_score.get, default=None)

    def mutual_followers(self, user_id1, user_id2):
        """Find the mutual followers between two users in the social graph."""
        if user_id1 in self.users and user_id2 in self.users:
            return self.users.get(user_id1).followers.intersection(self.users.get(user_id2).followers)
        return None

    def suggested_follows(self, user_id):
        """Suggest followers for a user in the social graph."""
        if user_id not in self.users:
            return None
        suggested = CustomSet()
        for follower_id in self.users.get(user_id).followers:
            suggested.update(self.users.get(follower_id).followers)

        return suggested.difference(self.users.get(user_id).followers).difference(CustomSet([user_id]))

    def search_posts_by_topic(self, topic):
        """Search for posts with a specific topic in the social graph."""
        posts_with_topic = []
        for user in self.users.Values():
            for post in user.posts:
                # Check if the topic is in the post's topics
                if topic.lower() in [t.lower() for t in post.get('topics')]:
                    posts_with_topic.append(post.get('body'))
        return posts_with_topic

    def print_network_analysis(self, user1_id=None, user2_id=None, topic=None):
        """
        Perform a network analysis on the social graph.

        Parameters:
        - user1_id (int): User ID for the first user.
        - user2_id (int): User ID for the second user.
        - topic (str): Topic for searching posts.

        Returns:
        - list: A list of strings containing the network analysis results.
        """
        try:
            user1_id = int(user1_id)
        except:
            user1_id = "Invalid Id1"

        try:
            user2_id = int(user2_id)
        except:
            user2_id = "Invalid Id2"

        result = []
        result.append("-" * 30)

        # Most Influential User
        influential_user = self.most_influential_user()
        if influential_user:
            result.append("Most Influential User:")
            result.append(f"User ID: {influential_user.user_id}")
            result.append(f"Name: {influential_user.name}")
            result.append(f"Number of Followers: {len(influential_user.followers)}")
        else:
            result.append("No influential user found.")
        result.append("-" * 30)

        # Most Active User
        active_user_id = self.most_active_user()
        if not active_user_id:
            if user1_id:
                active_user_id = user1_id

        if active_user_id:
            active_user = self.users.get(active_user_id)
            result.append("Most Active User:")
            result.append(f"User ID: {active_user_id}")
            result.append(f"Name: {active_user.name}")
            result.append(f"Active Score: {len(active_user.followers)}")
        else:
            result.append("No active user found.")
        result.append("-" * 30)

        if user1_id == "Invalid Id1":
            result.append("Invalid User ID1.")
            if user2_id == "Invalid Id2":
                result.append("Invalid User ID2.")
        else:
            if  user2_id != "Invalid Id2":
                # Mutual Followers
                if isinstance(user1_id, int) and isinstance(user2_id, int):
                    mutual_followers = self.mutual_followers(user1_id, user2_id)
                    if mutual_followers == None:
                        result.append(f"{user1_id}, {user2_id} : These users are not in the social \nnetwork (at least one of them). \nCan't Find mutual followers for \nNOT existing users.")
                    else:
                        if len(mutual_followers) == 0:
                            result.append(f"{user1_id}, {user2_id} : These user IDs don't \nhave any mutual followers.")
                        else:
                            result.append(f"Mutual followers between user {user1_id} and user {user2_id}:")
                            result.append([follower for follower in mutual_followers])
                else:
                    result.append("Mutual followers: Specify user1_id and user2_id to find mutual followers.")
            else:
                result.append("Invalid User ID2.")
            result.append("-" * 30)

            # Suggested Follows
            if user1_id:
                suggested_follows = self.suggested_follows(user1_id)
                if suggested_follows == None:
                    result.append(f"{user1_id} : This user ID is not in the social network. \nCan't suggest follows for NOT existing users.")
                else:
                    if len(suggested_follows) == 0:
                        result.append(f"No suitable suggestions found for the given user ID: {user1_id}")
                    else:
                        result.append(f"Suggested follows for user {user1_id}:")
                        result.append([suggested for suggested in suggested_follows])
            else:
                result.append("Suggested follows: Specify user_id to get suggested follows.")
        result.append("-" * 30)

        # Posts by Topic
        if topic:
            posts_by_topic = self.search_posts_by_topic(topic)
            if len(posts_by_topic) == 0:
                result.append(f"No posts with topic: {topic} were found.")
            else:
                result.append(f"Posts with topic '{topic}':")
                result.extend(posts_by_topic)
        else:
            result.append("Posts by topic: Specify a topic to search for posts.")
        result.append("-" * 30)

        return result
