from typing import List
from circuit_shader import exports
from circuit_shader.imports import circuit_common

CONNECTION_SIZE = 6.0


class GeometryShader(exports.GeometryShader):
    def transform(
        self,
        circuit_node: circuit_common.CircuitNode,
        geometry: List[circuit_common.GeometryElement],
    ) -> List[circuit_common.GeometryElement]:
        # Only match connection elements that Cirucit Diagram has determined
        # should be visible.
        if (
            isinstance(
                circuit_node.element,
                circuit_common.CircuitElementConnectionCircuitElement,
            )
            and circuit_node.element.value.visible
        ):
            connection = circuit_node.element.value

            # Create a square with the centre at the connection point.
            square_connection = circuit_common.GeometryElement(
                circuit_common.GeometryItemRectangleGeometry(
                    circuit_common.RectangleGeometry(
                        connection.location.x - CONNECTION_SIZE / 2.0,
                        connection.location.y - CONNECTION_SIZE / 2.0,
                        CONNECTION_SIZE,
                        CONNECTION_SIZE,
                        0.0,
                        None,
                        circuit_common.GeometryStyle(
                            circuit_common.SolidColorStyle(
                                circuit_common.Color(0, 0, 0, 255)
                            )
                        ),
                    )
                ),
                circuit_common.GeometryFlags(0),
                [],
            )

            # Render just the square. Any existing geometry associated with this
            # node is discarded.
            return [square_connection]
        return geometry
