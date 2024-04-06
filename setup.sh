#!/usr/bin/env bash
python3 -m venv .venv
source .venv/bin/activate
echo $(pwd)/wit_py/ > $(python -c "import sysconfig; print(sysconfig.get_path('purelib'))")/wit-py.pth
pip install -r requirements.txt
for world in "circuit-shader" "circuit-shader-with-utils"; do
    componentize-py -d wit/ -w $world bindings wit_py
    touch ./wit_py/${world//-/_}/py.typed
done
