#!/usr/bin/env python

# This tool has been copied from
# https://github.com/vinayak-mehta/pdftopng/blob/main/scripts/wheel_repair.py
# and extended to supported hierarchical folder architecture with mulitple .pyd
# to update, and to move all the DLL in a common folder *package*.lib installed
# jointly with the package itself, similarly to auditwheel on Linux platform.
# (see also https://discuss.python.org/t/delocate-auditwheel-but-for-windows/2589/9).

# Additionally adapted from
# https://github.com/Wandercraft/jiminy/blob/648c0ec918ca2c2f734a32bada1dbfaf6226de48/build_tools/wheel_repair.py
# added sorting of pyd and dll files such that repaired dlls pointing to their own
# dependencies aren't rewritten without references to the dependency later on. This
# should be cleaned up later, and could be replaced with smarter heuristics i.e.
# for all pyds, find the unique dlls they depend on. For all unique dlls find their
# dependencies and repair. Repair pyds to point to the repaired dlls, don't copy and
# overwrite the newly repaired dll.

import os
import shutil
import pathlib
import argparse
import hashlib
import zipfile
import tempfile
from collections import OrderedDict

import pefile
from machomachomangler.pe import redll
import taichi as ti


def hash_filename(filepath, blocksize=65536):
    hasher = hashlib.sha256()

    with open(filepath, "rb") as afile:
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)

    root, ext = os.path.splitext(filepath)
    return f"{os.path.basename(root)}-{hasher.hexdigest()[:8]}{ext}"


def find_dll_dependencies(dll_filepath, lib_dir):
    dll_deps = {}
    pe = pefile.PE(dll_filepath)
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        entry_name = entry.dll.decode("utf-8")
        if entry_name in os.listdir(lib_dir):
            dll_deps.setdefault(
                os.path.basename(dll_filepath), set()).add(entry_name)
            nested_dll_deps = find_dll_dependencies(
                os.path.join(lib_dir, entry_name), lib_dir)
            dll_deps.update(nested_dll_deps)
            print(nested_dll_deps)
    return dll_deps


def mangle_filename(old_filename, new_filename, mapping):
    with open(old_filename, "rb") as f:
        buf = f.read()
    new_buf = redll(buf, mapping)
    with open(new_filename, "wb") as f:
        f.write(new_buf)


def fix(WHEEL_FILE, WHEEL_DIR="dist/wheelhouse/"):
    taichi_path = ti.__path__[0]
    DLL_DIR = os.path.join(taichi_path, '_lib', 'c_api', 'bin')

    wheel_name = os.path.basename(WHEEL_FILE)
    repaired_wheel = os.path.join(os.path.abspath(WHEEL_DIR), wheel_name)
    
    old_wheel_dir = tempfile.mkdtemp()
    new_wheel_dir = tempfile.mkdtemp()
    package_name = wheel_name.split("-")[0]
    bundle_name = package_name + ".libs"
    bundle_path = os.path.join(new_wheel_dir, bundle_name)
    os.makedirs(bundle_path)
    
    with zipfile.ZipFile(WHEEL_FILE, "r") as wheel:
        wheel.extractall(old_wheel_dir)
        wheel.extractall(new_wheel_dir)
        pyd_rel_paths = [os.path.normpath(path)
                         for path in wheel.namelist() if path.endswith(".pyd")]
    
    dll_dependencies = {}
    for rel_path in pyd_rel_paths:
        abs_path = os.path.join(old_wheel_dir, rel_path)
        dll_dependencies.update(find_dll_dependencies(abs_path, DLL_DIR))
    
    # sort pyds first
    pyds = []
    dlls = []
    for dll, dependencies in dll_dependencies.items():
        if dll.endswith(".pyd"):
            pyds.append((dll, dependencies))
        elif dll.endswith(".dll"):
            dlls.append((dll, dependencies))
    
    dll_dependencies = OrderedDict(pyds + dlls)
    
    for dll, dependencies in dll_dependencies.items():
        mapping = {}
    
        if dll.endswith(".pyd"):
            rel_path = next(path for path in pyd_rel_paths if path.endswith(dll))
    
        for dep in dependencies:
            hashed_name = hash_filename(os.path.join(DLL_DIR, dep))  # already basename
            if dll.endswith(".pyd"):
                bundle_rel_path = os.path.join(
                    "..\\" * rel_path.count(os.path.sep), bundle_name)
                mapping[dep.encode("ascii")] = os.path.join(
                    bundle_rel_path, hashed_name).encode("ascii")
            else:
                mapping[dep.encode("ascii")] = hashed_name.encode("ascii")
            shutil.copy(
                os.path.join(DLL_DIR, dep),
                os.path.join(bundle_path, hashed_name))
    
        if dll.endswith(".pyd"):
            old_name = os.path.join(old_wheel_dir, rel_path)
            new_name = os.path.join(new_wheel_dir, rel_path)
        else:
            old_name = os.path.join(DLL_DIR, dll)
            hashed_name = hash_filename(os.path.join(DLL_DIR, dll))  # already basename
            new_name = os.path.join(bundle_path, hashed_name)
    
        mangle_filename(old_name, new_name, mapping)
    
    pathlib.Path(os.path.dirname(repaired_wheel)).mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(repaired_wheel, "w", zipfile.ZIP_DEFLATED) as new_wheel:
        for root, dirs, files in os.walk(new_wheel_dir):
            new_root = os.path.relpath(root, new_wheel_dir)
            for file in files:
                new_wheel.write(
                    os.path.join(root, file), os.path.join(new_root, file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--py', type=str)
    parser.add_argument('--version', type=str)
    args = parser.parse_args()

    fix(f'dist/brainpylib-{args.version}-cp{args.py}-cp{args.py}-win_amd64.whl')

