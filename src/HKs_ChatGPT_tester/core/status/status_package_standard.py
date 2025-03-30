#相対パスをこのスクリプトを基準に処理する
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from i_status_package import IStatusPackage
from status_standard import StatusStandard
class StatusPackageStandard(IStatusPackage):
    def __init__(self):
        self.statusStandard = StatusStandard()
