from hilti_profis.Config import MasterModule
from .Custom import Custom
from .Ledger import Ledger

class AnchorPlate(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','AnchorPlate']
        submodules_list = [
            Custom(basefile=basefile),
            Ledger(basefile=basefile)
        ]
        super().__init__(basefile, headerpath, submodules_list)