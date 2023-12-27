from CustomDict import CustomDict
from CustomSet import CustomSet
from CustomDiGraph import CustomDiGraph
from customedDS.User import User

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
        if user_id in self.users.Keys() and follower_id in self.users.Keys():
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
        return CustomSet()

    def suggested_follows(self, user_id):
        """Suggest followers for a user in the social graph."""
        if user_id not in self.users:
            return CustomSet()
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

    def print_network_analysis(self):
        """Print a network analysis report for the social graph."""
        print("Network Analysis:")
        print("-" * 30)

        # Most Influential User
        influential_user = self.most_influential_user()
        if influential_user:
            print("Most Influential User:")
            print(f"User ID: {influential_user.user_id}")
            print(f"Name: {influential_user.name}")
            print(f"Number of Followers: {len(influential_user.followers)}")
        else:
            print("No influential user found.")
        print("-" * 30)

        # Most Active User
        active_user_id = self.most_active_user()
        if active_user_id:
            active_user = self.users.get(active_user_id)
            print("Most Active User:")
            print(f"User ID: {active_user_id}")
            print(f"Name: {active_user.name}")
            print(f"Active Score: {len(active_user.followers)}")
        else:
            print("No active user found.")
        print("-" * 30)

        # Mutual Followers
        user1_id, user2_id = 3, 2
        mutual_followers = self.mutual_followers(user1_id, user2_id)
        print(f"Mutual Followers between User {user1_id} and User {user2_id}:")
        print([follower for follower in mutual_followers])
        print("-" * 30)

        # Suggested Follows
        user_id = 1
        suggested_follows = self.suggested_follows(user_id)
        print(f"Suggested Follows for User {user_id}:")
        print([suggested for suggested in suggested_follows])

        # Posts by Topic
        topic = "economy"
        posts_by_topic = self.search_posts_by_topic(topic)
        print(f"Posts with Topic '{topic}':")
        for post in posts_by_topic:
            print(post)
        print("-" * 30)
