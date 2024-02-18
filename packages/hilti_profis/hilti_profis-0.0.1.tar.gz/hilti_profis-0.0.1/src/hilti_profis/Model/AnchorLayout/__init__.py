from hilti_profis.Config import MasterModule
from .Points import Points

class AnchorLayout(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','AnchorLayout']
        submodules_list = [
            Points(basefile=basefile)
        ]
        super().__init__(basefile, headerpath, submodules_list)