

import ctypes
import hashlib
import os
import pathlib
import subprocess
import time
import numpy as np

from loguru import logger

C2DLL_VCVARSPATH = os.environ.get('C2DLL_VCVARSPATH', 'C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Auxiliary\\Build\\vcvars64.bat')
C2DLL_WORKDIR = os.environ.get('C2DLL_WORKDIR', './__dll__')

BUILD_TEMPLATE = r'''
set NAME=<NAME>
@call "<VCVARSPATH>"
cl.exe /O2 /Oi    /Gm- /GS /Gy /GL /Gd    /Zi   /c  /nologo /W3 /WX- /diagnostics:column /sdl /EHsc /MD ^
/fp:precise /permissive- /TP /FC /errorReport:prompt %NAME%.cpp > %NAME%.log 2>&1
link.exe /OUT:"%NAME%.dll" /INCREMENTAL:NO /NOLOGO /MANIFEST /MANIFESTUAC:NO /manifest:embed /DEBUG /PDB:"%NAME%.pdb" ^
/SUBSYSTEM:WINDOWS /OPT:REF /OPT:ICF /TLBID:1 /DYNAMICBASE /NXCOMPAT /IMPLIB:"%NAME%.lib" /MACHINE:X64 /DLL %NAME%.obj >> %NAME%.log 2>&1
del vc???.pdb %NAME%.obj %NAME%.exp %NAME%.lib
'''
COMMON_HEADER = r'''
#pragma once

#if defined(_MSC_VER)
#define DLL_API extern "C" __declspec(dllexport)
#else
#define DLL_API
#endif

'''

def dllfunc(c_code, name=''):
    root = pathlib.Path(C2DLL_WORKDIR)
    root.mkdir(exist_ok=True)
    hash = hashlib.sha1(c_code.encode('utf-8')).hexdigest()
    name += hash
    
    src_path = root/f'{name}.cpp'
    dll_path = root/f'{name}.dll'
    bat_path = root/f'{name}.bat'
    log_path = root/f'{name}.log'
    if not dll_path.exists():
        t1 = time.time()
        src_path.write_text('#include "common.h"\n\n' + c_code)
        build_temlate = BUILD_TEMPLATE.replace('<NAME>', name).replace('<VCVARSPATH>', C2DLL_VCVARSPATH)
        bat_path.write_text(build_temlate)
        pathlib.Path(root / 'common.h').write_text(COMMON_HEADER)

        logger.debug(f"Building dll {dll_path}...")
        subprocess.run(str(bat_path.absolute()).split(), cwd=str(root), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log = log_path.read_text()
        assert 'error' not in log and dll_path.exists(), f'{dll_path} exists: {dll_path.exists()}\n\n\n{log}'
        logger.debug(f'Built dll: {dll_path.absolute()} (took {time.time() - t1:.2f}s)')

    return ctypes.WinDLL(str(dll_path))

def as_ptr(x):
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    return np.ctypeslib.as_ctypes(x)
