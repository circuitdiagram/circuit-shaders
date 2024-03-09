Circuit Shaders
===============

_Circuit shaders_ are small programs that are run by [Circuit Diagram](https://www.circuit-diagram.org/)
to modify the appearance of a circuit.

Some examples of what circuit shaders can do are:

- Change the color of circuit elements
- Apply formatting to text
- Render new elements
- Change the thickness of wires
- Change how connection points are rendered

Circuit shaders are WebAssembly modules built on the WebAssembly Component Model. It is possible to write
shaders in a variety of languages, but documentation is only provided for doing so using Python at this
time.

## Usage

To be added.

## Development

To be added.

When installing any new dependencies inside the Python virtual environment, run the below command to
save these to the `requirements.txt` that can be checked into git.

```bash
pip freeze > requirements.txt
```

## License

The shader programs in this repository are licensed under GPLv3. The _Circuit Diagram Shader Tool_
binary (used to execute shaders, not included in this repository) is proprietary and must not be
distributed separately.
