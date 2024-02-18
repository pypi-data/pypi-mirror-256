from hilti_profis.Config import MasterModule
from .Custom import Custom

class Profile(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity','Profile']
        submodules_list = [
            Custom(basefile=basefile)
        ]
        super().__init__(basefile, headerpath, submodules_list)