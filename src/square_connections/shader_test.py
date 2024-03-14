from circuit_shader.imports.circuit_common import (
    CircuitElementConnectionCircuitElement,
    CircuitElementWireCircuitElement,
    CircuitNode,
    ConnectionCircuitElement,
    EllipseGeometry,
    GeometryElement,
    GeometryFlags,
    GeometryItemEllipseGeometry,
    GeometryItemRectangleGeometry,
    NodeEffects,
    Point,
    WireCircuitElement,
)
from square_connections.shader import GeometryShader


def test_replace_connection_geometry_with_square():
    input_node = CircuitNode(
        CircuitElementConnectionCircuitElement(
            ConnectionCircuitElement(Point(10, 10), True)
        ),
        NodeEffects(None),
    )
    input_geometry = [
        GeometryElement(
            GeometryItemEllipseGeometry(
                EllipseGeometry(10, 10, 2, 2, None, None, None)
            ),
            GeometryFlags(0),
        )
    ]

    shader = GeometryShader()
    result = shader.transform(input_node, input_geometry)

    assert len(result) == 1
    assert isinstance(result[0].geometry, GeometryItemRectangleGeometry)


def test_ignore_non_connection_elements():
    input_node = CircuitNode(
        CircuitElementWireCircuitElement(WireCircuitElement([])), NodeEffects(None)
    )
    input_geometry = [
        GeometryElement(
            GeometryItemEllipseGeometry(
                EllipseGeometry(10, 10, 2, 2, None, None, None)
            ),
            GeometryFlags(0),
        )
    ]

    shader = GeometryShader()
    result = shader.transform(input_node, input_geometry)

    assert result == input_geometry
