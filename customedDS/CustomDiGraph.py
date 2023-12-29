from customedDS.CustomDict import CustomDict
import matplotlib.pyplot as plt
import random
import numpy as np

class CustomDiGraph:
    """
    Directed graph class.

    Attributes:
    - nodes (CustomDict): A dictionary to store nodes and their associated data.
    - edges (CustomDict): A dictionary to store directed edges between nodes.
    """

    def __init__(self):
        """
        Initialize an empty directed graph.
        """
        self.nodes = CustomDict()
        self.edges = CustomDict()

    def add_node(self, node):
        """
        Add a node to the graph.

        Parameters:
        - node: The node to be added to the graph.
        """
        self.nodes.set(node, CustomDict())

    def add_edge(self, source, target):
        """
        Add a directed edge from source to target.

        Parameters:
        - source: The source node of the directed edge.
        - target: The target node of the directed edge.
        """
        if source not in self.nodes:
            self.add_node(source)

        if target not in self.nodes:
            self.add_node(target)

        if source not in self.edges:
            self.edges.set(source, [])
        temp_edges = self.edges.get(source)
        temp_edges.append(target)
        self.edges.set(source, temp_edges)

    def well_separated_layout(self, iterations=50, repulsion_factor=2.0, width=1.0, height=1.0):
        """
            Generate layout positions for nodes with increased repulsion, promoting well separation.

            Parameters:
            - iterations (int): Number of iterations to perform the layout algorithm.
            - repulsion_factor (float): Controls the strength of repulsion between nodes. Higher values increase separation.
            - width (float): Width of the layout space.
            - height (float): Height of the layout space.

            Returns:
            CustomDict: Dictionary containing node positions after the layout.

            Algorithm:
            1. Initialize random positions for each node within the specified layout space.
            2. Perform the specified number of iterations to update node positions.
            3. Calculate repulsive forces between all pairs of nodes, increasing with the repulsion factor.
            4. Update node positions based on the calculated repulsive forces.
            5. Normalize node positions to the [0, 1] range.

            Note: This layout algorithm emphasizes separating nodes by increasing the repulsion between them.
        """
        positions = CustomDict()

        # Initialize random positions within the specified width and height
        for node in self.nodes:
            positions.set(node, [random.uniform(0, width), random.uniform(0, height)])

        for _ in range(iterations):
            displacements = CustomDict()

            # Initialize displacements to zero for each node
            for node in self.nodes:
                displacements.set(node, np.array([0.0, 0.0]))

            # Calculate repulsive forces between all pairs of nodes
            for source in self.nodes:
                for target in self.nodes:
                    if source != target:
                        delta = np.array(positions.get(source)) - np.array(positions.get(target))
                        dist = max(np.linalg.norm(delta), 0.1)
                        force = repulsion_factor / dist  # Increase repulsion force
                        displacements.set(source, displacements.get(source) + force * delta / dist)

            # Update node positions based on calculated displacements
            for node in self.nodes:
                norm = max(np.linalg.norm(displacements.get(node)), 0.1)
                positions.set(node, positions.get(node) + (displacements.get(node) / norm * min(norm, repulsion_factor)))

        # Normalize positions to [0, 1] range
        x_min, y_min = np.min(positions.Values(), axis=0)
        x_max, y_max = np.max(positions.Values(), axis=0)
        for node, (x, y) in positions.items():
            x = (x - x_min) / (x_max - x_min)
            y = (y - y_min) / (y_max - y_min)
            positions.set(node, [width * x, height * y])

        return positions

    def visualize(self):
        """
        Visualize the graph using matplotlib.

        Visualization Steps:
        1. Get well-separated layout positions using the well_separated_layout method.
        2. Separate x and y coordinates for plotting.
        3. Plot nodes with labels using scatter plot.
        4. Plot edges between nodes.
        5. Add arrowheads to visualize the directed edges.
        6. Display the visualization using matplotlib.

        Note: The well_separated_layout method is used to generate node positions with increased separation.
        """
        # Get well-separated layout-like positions
        pos = self.well_separated_layout()

        # Separate x and y coordinates
        x_coordinates, y_coordinates = zip(*pos.Values())

        # Plot nodes with labels
        plt.scatter(x_coordinates, y_coordinates, color='skyblue', s=200)
        for node, (x, y) in pos.items():
            plt.text(x, y, str(node), ha='center', va='center', color='black', fontweight='bold')

        # Plot edges
        for source, targets in self.edges.items():
            for target in targets:
                x_source, y_source = pos.get(source)
                x_target, y_target = pos.get(target)

                plt.plot([x_source, x_target], [y_source, y_target], color='gray', linestyle='-', linewidth=2)

                # Add arrowhead
                dx = x_target - x_source
                dy = y_target - y_source
                dist = (dx**2 + dy**2)**0.5
                dx /= dist
                dy /= dist
                plt.arrow(
                    x_target - 0.02 * dx, y_target - 0.02 * dy,
                    0.01 * dx, 0.01 * dy,
                    shape='full', lw=0, length_includes_head=True,
                    head_width=0.02, head_length=0.05, color='black'
                )

        plt.yticks([])
        plt.xticks([])
        plt.show()
