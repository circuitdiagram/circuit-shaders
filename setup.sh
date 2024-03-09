#!/usr/bin/env bash
python3 -m venv .venv
source .venv/bin/activate
echo $(pwd)/wit_py/ > $(python -c "import sysconfig; print(sysconfig.get_path('purelib'))")/wit-py.pth
pip install -r requirements.txt
componentize-py -d wit/circuit-shader.wit -w circuit-shader bindings wit_py
touch ./wit_py/circuit_shader/py.typed
