#!/usr/bin/env bash

# Create build directory if it doesn't exist
mkdir -p build

src_dir="./src"

for filename in "$src_dir"/*/shader.py; do
  # Check it's a regular file (not a directory or hidden file)
  if [[ -f "$filename" ]]; then
    shader_name=$(dirname "$filename")
    shader_name=${shader_name##*/}
    echo "Building $shader_name"

    componentize-py -d wit/circuit-shader.wit -w circuit-shader componentize -p src/$shader_name shader -o build/$shader_name.wasm
    if [[ $? -ne 0 ]]; then
      echo "Error: failed to build $shader_name"
      exit 1 
    fi
  fi
done
