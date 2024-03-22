from typing import List
from circuit_shader import exports
from circuit_shader.imports import circuit_common

GRID_SIZE_SMALL = 10
GRID_SIZE_LARGE = 100


class GeometryShader(exports.GeometryShader):
    def transform(
        self,
        circuit_node: circuit_common.CircuitNode,
        geometry: List[circuit_common.GeometryElement],
    ) -> List[circuit_common.GeometryElement]:
        # The `document` node is the top-level node. Continue until
        # this node is reached to add the grid.
        if not isinstance(
            circuit_node.element,
            circuit_common.CircuitElementDocumentCircuitElement,
        ):
            return geometry

        document = circuit_node.element.value

        grid = []

        # Vertical grid lines
        for x in range(
            round(document.canvas_bounds.top_left.x / GRID_SIZE_SMALL),
            round(document.canvas_bounds.bottom_right.x / GRID_SIZE_SMALL),
        ):
            grid.append(
                make_grid_line(
                    x * GRID_SIZE_SMALL,
                    document.canvas_bounds.top_left.y,
                    x * GRID_SIZE_SMALL,
                    document.canvas_bounds.bottom_right.y,
                    x % 10 == 0,
                )
            )

        # Horizontal grid lines
        for y in range(
            round(document.canvas_bounds.top_left.y / GRID_SIZE_SMALL),
            round(document.canvas_bounds.bottom_right.y / GRID_SIZE_SMALL),
        ):
            grid.append(
                make_grid_line(
                    document.canvas_bounds.top_left.x,
                    y * GRID_SIZE_SMALL,
                    document.canvas_bounds.bottom_right.x,
                    y * GRID_SIZE_SMALL,
                    y % 10 == 0,
                )
            )

        return grid + geometry


def make_grid_line(
    x1: float, y1: float, x2: float, y2: float, major: bool
) -> circuit_common.GeometryElement:
    return circuit_common.GeometryElement(
        circuit_common.GeometryItemLineGeometry(
            circuit_common.LineGeometry(
                circuit_common.Point(x1, y1),
                circuit_common.Point(x2, y2),
                1.5 if major else 0.5,
                circuit_common.GeometryStyle(
                    circuit_common.SolidColorStyle(
                        circuit_common.Color(200, 200, 200, 255)
                    )
                ),
            )
        ),
        circuit_common.GeometryFlags.BACKGROUND,
    )
