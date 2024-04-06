from typing import List
from colorsys import rgb_to_hls, hls_to_rgb
from circuit_shader import exports
from circuit_shader.imports import circuit_common

# (1.0: darker) -> (0.0: lighter)
DARK_LEVEL = 0.8


class GeometryShader(exports.GeometryShader):
    def transform(
        self,
        circuit_node: circuit_common.CircuitNode,
        geometry: List[circuit_common.GeometryElement],
    ) -> List[circuit_common.GeometryElement]:
        # The `document` node is the top-level node. Continue until
        # this node is reached to do all the color conversion at once.
        if not isinstance(
            circuit_node.element,
            circuit_common.CircuitElementDocumentCircuitElement,
        ):
            return geometry

        document = circuit_node.element.value

        # Add a dark background, and convert the style of each
        # element to the dark theme.
        return [
            circuit_common.GeometryElement(
                circuit_common.GeometryItemRectangleGeometry(
                    circuit_common.RectangleGeometry(
                        document.canvas_bounds.top_left.x,
                        document.canvas_bounds.top_left.y,
                        document.canvas_bounds.bottom_right.x
                        - document.canvas_bounds.top_left.x,
                        document.canvas_bounds.bottom_right.y
                        - document.canvas_bounds.top_left.y,
                        0.0,
                        None,
                        circuit_common.GeometryStyle(
                            circuit_common.SolidColorStyle(
                                circuit_common.Color(0, 0, 0, 255)
                            )
                        ),
                    )
                ),
                circuit_common.GeometryFlags.BACKGROUND,
                [],
            )
        ] + [to_dark_theme(x) for x in geometry]


def to_dark_theme(x: circuit_common.GeometryElement) -> circuit_common.GeometryElement:
    # Convert both the stroke and fill styles, if present.

    if hasattr(x.geometry.value, "stroke_style"):
        x.geometry.value.stroke_style = style_to_dark(x.geometry.value.stroke_style)

    if hasattr(x.geometry.value, "fill_style"):
        x.geometry.value.fill_style = style_to_dark(x.geometry.value.fill_style)

    return x


def style_to_dark(
    style: circuit_common.GeometryStyle | None,
) -> circuit_common.GeometryStyle | None:
    # Only SolidColorStyle is supported.
    # Any other styles will not be converted to dark theme.
    if not isinstance(style, circuit_common.GeometryStyleSolidColor):
        return None

    # Convert to HLS color space
    hsv_color = rgb_to_hls(
        style.value.color.r / 255,
        style.value.color.g / 255,
        style.value.color.b / 255,
    )

    # Reduce L and convert back to RGB
    dark_mode_color = hls_to_rgb(
        hsv_color[0], 1.0 - DARK_LEVEL * hsv_color[1], hsv_color[2]
    )

    # Create a SolidColorStyle representing this color.
    return circuit_common.GeometryStyleSolidColor(
        circuit_common.SolidColorStyle(
            circuit_common.Color(
                round(255 * dark_mode_color[0]),
                round(255 * dark_mode_color[1]),
                round(255 * dark_mode_color[2]),
                style.value.color.a,
            )
        )
    )
