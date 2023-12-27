from customedDS.CustomDict import CustomDict
from customedDS.SocialGraph import SocialGraph
import re

def build_graph_netowrk_from_xml(xml_text):
    """
    Build a social graph network from XML text.

    Parameters:
    - xml_text (str): XML representation of the social network.

    Returns:
    - SocialGraph: An instance of the SocialGraph class representing the social network.

    Example:
    >>> xml_text = "<users>...</users>"
    >>> social_graph_instance = build_graph_netowrk_from_xml(xml_text)
    """
    def parse_element(xml, tag):
        """
        Parse an XML element and extract content for a given tag.

        Parameters:
        - xml (str): The XML text.
        - tag (str): The tag to search for.

        Returns:
        - str: The content inside the specified tag.
        """
        match = re.search(r'<{0}.*?>(.*?)</{0}>'.format(tag), xml, re.DOTALL)
        return match.group(1).strip() if match else None

    # Create a SocialGraph instance
    social_graph_instance = SocialGraph()

    # Extract users information from the XML text
    users_match = re.search(r'<users>(.*?)</users>', xml_text, re.DOTALL)
    if users_match:
        users_xml = users_match.group(1)
        user_matches = re.finditer(r'<user>(.*?)</user>', users_xml, re.DOTALL)
        for user_match in user_matches:
            user_xml = user_match.group(1)
            user_id = int(parse_element(user_xml, 'id'))
            user_name = parse_element(user_xml, 'name')

            # Add user and corresponding node to the social graph
            social_graph_instance.add_user(user_id, user_name)
            social_graph_instance.graph.add_node(user_id)

            # Extract followers information
            followers_xml = parse_element(user_xml, 'followers')
            if followers_xml:
                follower_matches = re.finditer(r'<follower>(.*?)</follower>', followers_xml, re.DOTALL)
                for follower_match in follower_matches:
                    follower_xml = follower_match.group(1)
                    follower_id = int(parse_element(follower_xml, 'id'))

                    # Add follower, corresponding edge, and update social graph
                    social_graph_instance.graph.add_edge(follower_id, user_id)
                    social_graph_instance.add_follower(user_id, follower_id)

            # Extract posts information
            posts_xml = parse_element(user_xml, 'posts')
            if posts_xml:
                post_matches = re.finditer(r'<post>(.*?)</post>', posts_xml, re.DOTALL)
                for post_match in post_matches:
                    post_xml = post_match.group(1)
                    post_body = parse_element(post_xml, 'body')

                    # Extract topics information
                    topics_xml = parse_element(post_xml, 'topics')

                    if topics_xml:
                        # Use regular expression to extract topics
                        topics_match = re.findall(r'<topic>\s*(.*?)\s*</topic>', topics_xml, re.DOTALL)
                        # Filter out empty strings and strip whitespace
                        topics = [topic.strip() for topic in topics_match if topic.strip()]

                    bttemp = CustomDict()
                    bttemp.set('body', post_body)
                    bttemp.set('topics', topics)
                    social_graph_instance.add_post(user_id, bttemp)

    return social_graph_instance