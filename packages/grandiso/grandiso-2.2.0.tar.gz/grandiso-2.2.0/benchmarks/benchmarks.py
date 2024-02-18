import networkx as nx
from grandiso import find_motifs  # , find_motifs_iter


class TimeSuite:
    """
    Time benchmarks for motif search operations.
    """

    def setup(self):
        self.small_host = nx.complete_graph(20)
        self.medium_host = nx.complete_graph(45)
        self.large_host = nx.complete_graph(100)
        self.tri = nx.complete_graph(3)

    def time_small_host_triangles(self):
        """Count triangles in a small host graph."""
        # Search triangles
        find_motifs(self.tri, self.small_host)

    def time_medium_host_triangles(self):
        """Count triangles in a medium host graph."""
        # Search triangles
        find_motifs(self.tri, self.medium_host)

    def time_large_host_triangles(self):
        """Count triangles in a large host graph."""
        # Search triangles
        find_motifs(self.tri, self.large_host)


# class MemSuite:
#     def mem_list(self):
#         return [0] * 256
