#!/usr/bin/env python3
import time
import win32com.client as win32
from pathlib import Path
import sys


def run_sas_egp(egp_path, eg_version='7.1'):

    # Check if project file exists
    if not Path(egp_path).exists():
        raise FileNotFoundError(f'File not found {egp_path}')
    # egp_path = Path(os.path.abspath(egp_path))

    start_time = time.time()

    if eg_version.startswith('8'):
        eg_version = '8.1'

    try:
        print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Opening SAS EG {eg_version}')
        eg = win32.Dispatch(f'SASEGObjectModel.Application.{eg_version}')

        print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Opening project {egp_path}')
        project = eg.Open(egp_path, "")

        print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Running project {egp_path}')
        project.Run()

        print(f'SAS project took {time.time() - start_time} seconds to run.')
        print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Closing project')
        project.Close()
    except:
        print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Error running project {egp_path}')
        sys.exit(1)


if __name__ == '__main__':
    pass