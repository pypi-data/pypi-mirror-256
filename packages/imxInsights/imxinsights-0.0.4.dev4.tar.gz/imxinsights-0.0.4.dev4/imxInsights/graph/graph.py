from typing import List, Optional

import matplotlib.pyplot as plt
from shapely import LineString, Point

from imxInsights.utils.shapely_helpers import offset_linestring


class ImxGraph:
    def __init__(self, graph, imx_situation, micro_link_repo, micro_node_repo, rail_connections_repo, micro_link_connections):
        self.g = graph
        self.imx_situation = imx_situation
        self.micro_link_repo = micro_link_repo
        self.micro_node_repo = micro_node_repo
        self.rail_connections_repo = rail_connections_repo
        self.micro_link_connections = micro_link_connections

    def _get_plot(self):
        fig, ax = plt.subplots()
        length = 2
        for edge in self.g.edges:
            edge_data = self.g.get_edge_data(edge[0], edge[1])
            line_source = self.micro_link_repo.get_by_puic(edge[0]).get_shapely()
            line_target = self.micro_link_repo.get_by_puic(edge[1]).get_shapely()

            if edge_data["current_direction"] == "UPSTREAM":
                point_1 = line_source.interpolate(length)
            elif edge_data["current_direction"] == "DOWNSTREAM":
                point_1 = line_source.interpolate(line_source.length - length)
            else:
                raise ValueError()

            if edge_data["next_direction"] == "UPSTREAM":
                point_2 = line_target.interpolate(line_target.length - length)
            elif edge_data["next_direction"] == "DOWNSTREAM":
                point_2 = line_target.interpolate(length)
            else:
                raise ValueError()

            edge_line = offset_linestring(LineString([Point(point_1.x, point_1.y), Point(point_2.x, point_2.y)]), 0.25, "down")
            plt.annotate("", xy=edge_line.coords[0], xytext=edge_line.coords[-1], arrowprops=dict(facecolor="red", arrowstyle="->"))

        for node in self.g.nodes:
            line = self.micro_link_repo.get_by_puic(node).get_shapely()
            x, y = line.xy
            ax.plot(x, y, linewidth=7.0)

        plt.axis("equal")
        return plt

    def draw_graph(self, path: Optional[List[str]] = None):
        """Draws the graph, optionally highlighting a specified path.

        Args:
            path (Optional[List[str]]): A list of PUICs representing the path to highlight. If None, no path is highlighted.
        """
        plt = self._get_plot()
        plt.show()

    # todo: make path finder microlink lvl
    # todo: make path cutter based on from and to measures
    # todo: make object on path query
