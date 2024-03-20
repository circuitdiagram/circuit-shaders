from circuit_shader.imports.circuit_common import (
    CircuitElementDocumentCircuitElement,
    CircuitNode,
    Color,
    DocumentCircuitElement,
    GeometryElement,
    GeometryFlags,
    GeometryItemTextGeometry,
    GeometryStyle,
    LayoutRect,
    NodeEffects,
    Point,
    SolidColorStyle,
    TextGeometry,
    TextAlignmentTopLeft,
    TextRun,
    TextRunFormatting,
    TextRunFormattingTypeNormal,
    TextRunFormattingTypeSubscript,
)
from text_formatting.shader import GeometryShader

DOCUMENT_NODE = CircuitNode(
    CircuitElementDocumentCircuitElement(
        DocumentCircuitElement(
            LayoutRect(Point(0, 0), Point(10, 10)),
            LayoutRect(Point(0, 0), Point(10, 10)),
        )
    ),
    NodeEffects(None),
)


def test_subscript_1():
    shader = GeometryShader()
    result = shader.transform(DOCUMENT_NODE, generate_geometry("R_1"))

    assert len(result) == 1

    text_geometry = result[0].geometry.value
    assert len(text_geometry.text_runs) == 2

    assert text_geometry.text_runs[0].text == "R"
    assert isinstance(
        text_geometry.text_runs[0].formatting.formatting_type,
        TextRunFormattingTypeNormal,
    )

    assert text_geometry.text_runs[1].text == "1"
    assert isinstance(
        text_geometry.text_runs[1].formatting.formatting_type,
        TextRunFormattingTypeSubscript,
    )


def test_subscript_2():
    shader = GeometryShader()
    result = shader.transform(DOCUMENT_NODE, generate_geometry("R_{12}"))

    assert len(result) == 1

    text_geometry = result[0].geometry.value
    assert len(text_geometry.text_runs) == 2

    assert text_geometry.text_runs[0].text == "R"
    assert isinstance(
        text_geometry.text_runs[0].formatting.formatting_type,
        TextRunFormattingTypeNormal,
    )

    assert text_geometry.text_runs[1].text == "12"
    assert isinstance(
        text_geometry.text_runs[1].formatting.formatting_type,
        TextRunFormattingTypeSubscript,
    )


def test_subscript_3():
    shader = GeometryShader()
    result = shader.transform(DOCUMENT_NODE, generate_geometry("R_12"))

    assert len(result) == 1

    text_geometry = result[0].geometry.value
    assert len(text_geometry.text_runs) == 3

    assert text_geometry.text_runs[0].text == "R"
    assert isinstance(
        text_geometry.text_runs[0].formatting.formatting_type,
        TextRunFormattingTypeNormal,
    )

    assert text_geometry.text_runs[1].text == "1"
    assert isinstance(
        text_geometry.text_runs[1].formatting.formatting_type,
        TextRunFormattingTypeSubscript,
    )

    assert text_geometry.text_runs[2].text == "2"
    assert isinstance(
        text_geometry.text_runs[2].formatting.formatting_type,
        TextRunFormattingTypeNormal,
    )


def test_subscript_4():
    shader = GeometryShader()
    result = shader.transform(DOCUMENT_NODE, generate_geometry("R_1 _"))

    assert len(result) == 1

    text_geometry = result[0].geometry.value
    assert len(text_geometry.text_runs) == 4

    assert text_geometry.text_runs[0].text == "R"
    assert isinstance(
        text_geometry.text_runs[0].formatting.formatting_type,
        TextRunFormattingTypeNormal,
    )

    assert text_geometry.text_runs[1].text == "1"
    assert isinstance(
        text_geometry.text_runs[1].formatting.formatting_type,
        TextRunFormattingTypeSubscript,
    )

    assert text_geometry.text_runs[2].text == " "
    assert isinstance(
        text_geometry.text_runs[2].formatting.formatting_type,
        TextRunFormattingTypeNormal,
    )

    assert text_geometry.text_runs[3].text == "_"
    assert isinstance(
        text_geometry.text_runs[3].formatting.formatting_type,
        TextRunFormattingTypeNormal,
    )


def test_subscript_5():
    shader = GeometryShader()
    result = shader.transform(DOCUMENT_NODE, generate_geometry("Some R_{example} Text"))

    assert len(result) == 1

    text_geometry = result[0].geometry.value
    assert len(text_geometry.text_runs) == 3

    assert text_geometry.text_runs[0].text == "Some R"
    assert isinstance(
        text_geometry.text_runs[0].formatting.formatting_type,
        TextRunFormattingTypeNormal,
    )

    assert text_geometry.text_runs[1].text == "example"
    assert isinstance(
        text_geometry.text_runs[1].formatting.formatting_type,
        TextRunFormattingTypeSubscript,
    )

    assert text_geometry.text_runs[2].text == " Text"
    assert isinstance(
        text_geometry.text_runs[2].formatting.formatting_type,
        TextRunFormattingTypeNormal,
    )


def test_maintain_style():
    style = SolidColorStyle(Color(10, 20, 30, 255))
    shader = GeometryShader()
    result = shader.transform(DOCUMENT_NODE, generate_geometry("R_1", style))

    assert len(result) == 1

    assert result[0].geometry.value.stroke_style is None
    assert result[0].geometry.value.fill_style == style


def generate_geometry(
    text: str,
    fill_style: GeometryStyle | None = GeometryStyle(
        SolidColorStyle(Color(0, 0, 0, 255))
    ),
) -> list[GeometryElement]:
    return [
        GeometryElement(
            GeometryItemTextGeometry(
                TextGeometry(
                    Point(10, 10),
                    TextAlignmentTopLeft(),
                    0.0,
                    [
                        TextRun(
                            text,
                            TextRunFormatting(12.0, TextRunFormattingTypeNormal()),
                        )
                    ],
                    0.0,
                    None,
                    fill_style,
                )
            ),
            GeometryFlags(0),
        )
    ]
