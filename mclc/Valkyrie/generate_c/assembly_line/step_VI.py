'''
Compile C program.
'''

# pylint: disable=unused-wildcard-import
import random, string, datetime, pathlib, shutil, os, subprocess

from ....Atributaries.modules.ast_classes import *
from .pgfs import fun_def

gcc_options = [
    '-c',                           # Compile or assemble the source files, but do not link.
    '-mcpu=cortex-m3',              # Specifies the name of the target ARM processor.
    '-mthumb',                      # Generate Thumb code.
    '-Og',                          # Optimize debugging experience.
    '-Wall',                        # Enables all the warnings.
    '-fdata-sections',              # Place each data item into its own section.
    '-ffunction-sections',          # Place each function item into its own section.
    '-g',                           # Produce debugging information.
    '-gdwarf-2',                    # Produce debugging information in DWARF-2 format.
    # '-Wa,-a,-ad,-alms=program.lst'  # Options passed to assembler
    #                                 #     Enable listing output from the assembler.
    #                                 #         d omit debugging directives.
    #                                 #         l include assembly.
    #                                 #         m include macro expansions
    #                                 #         s include symbols
    #                                 #         =FILE  list to FILE
]

as_options = [
    '-x', 'assembler-with-cpp',     # Specify the language of the following input files.
    '-c',
    '-mcpu=cortex-m3',
    '-mthumb',
    '-Og',
    '-Wall',
    '-fdata-sections',
    '-ffunction-sections',
    '-g',
    '-gdwarf-2',
]

ld_options = [
    '-mcpu=cortex-m3',
    '-mthumb',
    
    '-specs=nano.specs',            # Override built-in specs with the contents of nano.specs .
    '-lc', '-lm', '-lnosys',        # Search the libraries [ c, m, nosys ] when linking.

    # '-Wl,-Map=machine-code-on-flash.map,--cref',
    '-Wl,--gc-sections',            # Options passed to linkder
    #                                 #     Print a link map to the file machine-code-on-flash.map
    #                                 #     Print a cross reference table into map file.
    #                                 #     Enable garbage collection of unused input sections.
]


gcc_bin_str = 'arm-none-eabi-gcc'

def process(gc):
    code = gc.sb.build()
    
    # bd : building directory
    bd = pathlib.Path('.').joinpath('build')

    if bd.exists():
        if bd.is_file():
            os.remove(bd)
        else:
            shutil.rmtree(bd, ignore_errors=True)
    bd.mkdir()

    # cp : c program
    cp = bd.joinpath('program.c').absolute()
    cp.write_text(code)

    # of : object file
    of = bd.joinpath('program.o').absolute()


    process_args = []
    process_args.append(gcc_bin_str)
    process_args.extend(gcc_options)
    process_args.append('-o')
    process_args.append(str(of))
    process_args.append(str(cp))
    proc_res = subprocess.run(process_args)
    if proc_res.returncode != 0:
        error('compiling failed')

    # sof : startup file object file
    sof = pathlib.Path(__file__).parent.parent.joinpath('resources/startup_stm32f103xb.o').absolute()

    # ldf : link script file
    
    ldf = pathlib.Path(__file__).parent.parent.joinpath('resources/STM32F103C8Tx_FLASH.ld').absolute()

    # ef : elf file
    ef = bd.joinpath('program.elf').absolute()


    process_args = []
    process_args.append(gcc_bin_str)
    process_args.extend(ld_options)
    process_args.extend([
        '-T', str(ldf),
        '-o', str(ef),
        str(of),
        str(sof),
    ])

    proc_res = subprocess.run(process_args)
    if proc_res.returncode != 0:
        error('compiling failed')
