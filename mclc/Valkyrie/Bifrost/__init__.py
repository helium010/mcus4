from pathlib import Path
from io import BytesIO

import usb
from pyocd.core.helpers import ConnectHelper
from pyocd.core.target import Target
from pyocd.core.session import Session
from pyocd.probe.stlink_probe import StlinkProbe
from pyocd.probe.stlink.usb import STLinkUSBInterface



from elftools.common.py3compat import maxint, bytes2str
from elftools.dwarf.descriptions import describe_form_class
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

from ...utils import error, print_error


session = None
symbol_table = None


def open_session():

    pack_path = Path('/mnt/desktop/CMSIS-software-pacs/Keil.STM32F1xx_DFP.2.3.0.pack')
    if not pack_path.exists():
        error('CMSIS Pack doesn\'t exist in ' + pack_path.__str__() + '\n1. Download it from https://developer.arm.com/tools-and-software/embedded/cmsis/cmsis-packs/n2. config the path to it in ' + Path(__file__).__str__())

    STLink_v2_dev = usb.core.find(idVendor=0x0483, idProduct=0x3748)

    if STLink_v2_dev is None:
        print_error('STLink is not connected.')
        exit(1)

    STLink_v2_USB_Interface = STLinkUSBInterface(STLink_v2_dev)

    probe = StlinkProbe(STLink_v2_USB_Interface)

    global session
    session = Session(
        probe, options={
            'pack': pack_path.absolute().__str__(),
            'target_override': 'stm32f103c8'
        })

    session.open()

    return session