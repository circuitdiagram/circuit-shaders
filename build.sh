#!/usr/bin/env bash

# Create build directory if it doesn't exist
mkdir -p build

src_dir="./src"

# Builds a single shader
build_shader() {
  local shader_name="$1"
  local filename="$src_dir/$shader_name/shader.py"

  if [[ -f "$filename" ]]; then  # Make sure it's a regular file
    echo "Building $shader_name"

    componentize-py -d wit/ -w circuit-shader componentize -p src/$shader_name shader -o build/$shader_name.wasm
    if [[ $? -ne 0 ]]; then
      echo "Error: failed to build $shader_name"
      exit 1
    fi
  else
    echo "Error: shader $shader_name not found"
    exit 1
  fi
}

if [[ $# -eq 0 ]]; then  # If no argument is given, build all shaders
  for filename in "$src_dir"/*/shader.py; do
    if [[ -f "$filename" ]]; then
      shader_name=$(dirname "$filename")
      shader_name=${shader_name##*/}
      build_shader "$shader_name"
    fi
  done
else # If an argument is given, build only the specified shader
  build_shader "$1"
fi
