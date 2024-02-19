import ipih

from pih import A
from build_tools import build
from AutomationService.const import SD

build(SD, additional_modules=[A.PTH_FCD_DIST.NAME(A.CT_SR.MOBILE_HELPER.standalone_name)])