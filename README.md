Circuit Shaders
===============

_Circuit shaders_ are small programs run by [Circuit Diagram](https://www.circuit-diagram.org/)
to modify the appearance of a circuit.

Some examples of what circuit shaders can do are:

- Change the color of circuit elements
- Apply formatting to text
- Render new elements
- Change the thickness of wires
- Change how connection points are rendered

Circuit shaders are WebAssembly modules built on the WebAssembly Component Model. It is possible to write
shaders in a variety of languages, but documentation is only provided for doing so using
[Python](https://github.com/bytecodealliance/componentize-py) at this time.

## Usage

This repository is intended to be used for developing new shaders. To render circuits using existing shaders,
use the Web Editor. You can also browse the available existing shaders in the
[Shader Gallery](https://www.circuit-diagram.org/shaders).

For developing new shaders please see the _Development_ section below.

## Development

This section explains how to build and run shaders locally. These steps are designed to be followed
in a Linux environment. If you are using Windows, you can use WSL for this. In the future, documentation
may be added for other operating systems.

Get started quickly with a pre-configured environment in GitHub Codespaces, or see the _Setup_ section for
the manual setup instructions. When using Codespaces you can skip to the _Run_ instructions below.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/circuitdiagram/circuit-shaders)

### Setup

Building shaders requires Python 3.11 or newer.

```bash
$ python3 --version
Python 3.11.8
```

To set up the virtual environment and build the common shader dependencies, run `source ./setup.sh`. If your
default Python version is older than 3.11, you will need to adjust the commands from this setup file
and run them manually. For example, `python3.11 -m venv .venv` instead of `python3`.

### Run

Circuit shaders can be run in development by first building the Python script as a shader program, then
executing the shader on a circuit using the _Circuit Diagram Shader Tool_.

#### Step 1: Building the Shader

Building involves compiling the shader into a WebAssembly module.

Run the below command from the root of this repository to build a `shader.py` into a `shader.wasm` file:

```bash
# Change `dark_theme` to the name of your shader.
./build.sh dark_theme
```

#### Step 2: Create a Circuit

To run the shader on a circuit, you will need to either create a circuit using the
[Web Editor](https://www.circuit-diagram.org/editor/), or choose from one of the public circuits listed on
[circuit-diagram.org](https://www.circuit-diagram.org/circuits).

Copy the URL of the saved circuit as this will be required for the next step.

For example: https://www.circuit-diagram.org/circuits/ea648c42

#### Step 3: Download the Shader Tool

Download the Circuit Diagram _Shader Tool_ from
[circuit-diagram.org/downloads](https://www.circuit-diagram.org/downloads).

> [!Tip]
> Copy the download URL from the Downloads page above, then run the below command to download the file:
> ```bash
> curl -sLO <URL>
> ```
>
> The download is normally a `.tar.xz` file. You can extract this with the below command:
> ```bash
> tar -xJf ./cd-shader.*.linux-x64.tar.xz && rm ./cd-shader.*.linux-x64.tar.xz
> ```

Run the below command to check the shader tool is working:

```bash
$ ./cd-shader --help
Circuit Diagram shader tool. (c) Circuit Diagram 2024.

Usage: cd-shader run --circuit <CIRCUIT> --shader <FILE>... -o <PATH>
...
```

Sign in to your Circuit Diagram account in the shader tool. If you don't have an account you can create one
for free.

```bash
./cd-shader login
```

This will display a link to open in your browser. Open the link to connect the shader tool to your account.

#### Step 4: Run the Shader

This step will execute the shader and render the circuit as a PNG image.

Please note that fetching the input circuit and rendering the final result are performed by the Circuit Diagram
web service. This means that the _output_ of the shader is sent to Circuit Diagram for final rendering. However,
the shader, and Python code used to build it, are only used locally.

You can now run the shader tool to render the circuit:

```bash
# Replace the URL with the link to your circuit and `dark_theme` with the name of your shader.
./cd-shader run --circuit "https://www.circuit-diagram.org/circuits/ea648c42" \
    --shader ./build/dark_theme.wasm -o ./circuit.png
```

You should now see an image called `circuit.png` in your working directory. If there were any errors running
the shader, they will be printed to the console.

### Python Packages

When installing any new dependencies inside the Python virtual environment, run the below command to
save these to the `requirements.txt` that can be checked into git.

```bash
pip freeze > requirements.txt
```

## License

The shader programs in this repository are licensed under GPLv3. The _Circuit Diagram Shader Tool_
binary (used to execute shaders, not included in this repository) is proprietary and must not be
distributed separately.
