import os
from itertools import product
import argparse

parser = argparse.ArgumentParser(description='Generate files based on combinations of options.')
parser.add_argument('output_folder', type=str, help='The output folder where files will be created.')
parser.add_argument('--file_mode', type=str, default='x', choices=['x', 'w'], help='x=Will throw error if the file already exists; w=Will replace the contents of the file;.')
args = parser.parse_args()

def printVariations(output_folder, content, *option_lists):
    combinations = product(*option_lists)

    os.makedirs(output_folder, exist_ok=True)

    for combo in combinations:
        filename = "-".join(combo)
        filepath = os.path.join(output_folder, filename)
        try:
            with open(filepath, args.file_mode) as f:
                f.write(content)
                print(f"File '{filepath}' has been created.")
                pass
        except Exception as err:
            print(err)

linuxOptions = [
    ["Linux"], ["x86_64"], ["gcc", "g++"], ["11", "13"], ["17"], ["Debug", "Release"]
]

linuxContent = '''{% set os, arch, build_type, compiler, compiler_version, cpp_std = profile_name.split("-") %}

[settings]
os={{ os }}
arch={{ arch }}
build_type={{ build_type }}
compiler={{ compiler }}
compiler.version={{ compiler_version }}
compiler.libcxx=libstdc++11
compiler.cppstd={{ cpp_std }}

[buildenv]
CXX=/usr/bin/g++-{{ compiler_version }}
CC=/usr/bin/gcc-{{ compiler_version }}
'''

windowsProfile = '''{% set os, arch, compiler, compiler_version, runtime, cpp_std, build_type = profile_name.split("-") %}

[settings]
os={{ os }}
arch={{ arch }}
build_type={{ build_type }}
compiler={{ compiler }}
compiler.version={{ compiler_version }}
compiler.runtime={{ runtime }}
compiler.cppstd={{ cpp_std }}
'''

windowsOptions = [
    ["Windows"], ["x86_64"], ["msvc"], ["192"], ["dynamic", "static"], ["17"], ["Debug", "Release"]
]

printVariations(args.output_folder, linuxContent, *linuxOptions)
printVariations(args.output_folder, windowsProfile, *windowsOptions)
