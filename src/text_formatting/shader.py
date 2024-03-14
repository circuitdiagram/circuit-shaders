from typing import List
from circuit_shader import exports
from circuit_shader.imports import circuit_common
from pyparsing import Char, Group, Word, ZeroOrMore, nums, printables

# Define grammar for formatted text
plaintext = Word(printables + " ", exclude_chars="_")
subscript1 = Group("_" + Char(nums)("subscript"))
subscript2 = Group("_{" + Word(nums)("subscript") + "}")
lone_underscore = "_"
math_expr = ZeroOrMore(
    plaintext | subscript1 | subscript2 | lone_underscore
).leave_whitespace()


class GeometryShader(exports.GeometryShader):
    def transform(
        self,
        circuit_node: circuit_common.CircuitNode,
        geometry: List[circuit_common.GeometryElement],
    ) -> List[circuit_common.GeometryElement]:
        if isinstance(
            circuit_node.element, circuit_common.CircuitElementDocumentCircuitElement
        ):
            return [adjust_geometry(x) for x in geometry]
        return geometry


def adjust_geometry(geom: circuit_common.GeometryElement):
    if isinstance(geom.geometry, circuit_common.GeometryItemTextGeometry):
        geom.geometry.value.text_runs = [
            x for run in geom.geometry.value.text_runs for x in format_text(run)
        ]
    return geom


def format_text(run: circuit_common.TextRun) -> List[circuit_common.TextRun]:
    try:
        res: List[circuit_common.TextRun] = []
        for match in math_expr.parseString(run.text, parse_all=True):
            if "subscript" in match:
                res.append(
                    circuit_common.TextRun(
                        "{}".format(match["subscript"]),
                        circuit_common.TextRunFormatting(
                            10, circuit_common.TextRunFormattingTypeSubscript()
                        ),
                    )
                )
            else:
                res.append(
                    circuit_common.TextRun(
                        "{}".format(match),
                        circuit_common.TextRunFormatting(
                            10, circuit_common.TextRunFormattingTypeNormal()
                        ),
                    )
                )
        return res
    except Exception:
        return [run]
