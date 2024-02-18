# tests/test_visualisation.py
import pytest
from wardleymap.wardleymap import WardleyMap


def test_visualisation_elements():
    map_definition = """
    title Example Map
    component A [0.2, 0.2]
    """
    wm = WardleyMap(map_definition)
    #fig = wm.generate_map()  # Assuming this method returns a matplotlib figure
    #assert len(fig.axes) > 0  # Check if the figure has axes
    #assert len(fig.axes[0].texts) > 0  # Check if there are any text elements (like titles or labels)
