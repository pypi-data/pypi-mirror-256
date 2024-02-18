# tests/test_parsing.py
import pytest
from wardleymap.wardleymap import WardleyMap


def test_parse_title():
    map_definition = "title Example Map"
    wm = WardleyMap(map_definition)
    assert wm.title == "Example Map"


def test_parse_component():
    map_definition = """
    component Component [0.5, 0.5]
    """
    wm = WardleyMap(map_definition)
    assert "Component" in wm.nodes
    assert wm.nodes["Component"]["vis"] == 0.5
    assert wm.nodes["Component"]["mat"] == 0.5


def test_parse_edge():
    map_definition = """
    component A [0.2, 0.2]
    component B [0.8, 0.8]
    component A -> component B
    """
    wm = WardleyMap(map_definition)
    #assert ("B", "A") in wm.edges
