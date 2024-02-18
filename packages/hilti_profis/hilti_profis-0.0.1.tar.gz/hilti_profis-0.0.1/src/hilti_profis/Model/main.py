from hilti_profis.Config import MasterModule
from .AnchorPlate import AnchorPlate
from .AnchorLayout import AnchorLayout
from .Anchor import Anchor
from .BaseMaterial import BaseMaterial
from .Loads import Loads
from .Options import Options
from .Profile import Profile
from .ShearLug import ShearLug
from .Stiffeners import Stiffeners
from .Welds import Welds

class DesignModel(MasterModule):
    def __init__(self, basefile: dict) -> None:
        headerpath = ['ProjectDesignConcreteEntity',]
        submodules_list = [
            AnchorPlate(basefile=basefile),
            AnchorLayout(basefile=basefile),
            Anchor(basefile=basefile),
            BaseMaterial(basefile=basefile),
            Loads(basefile=basefile),
            Options(basefile=basefile),
            Profile(basefile=basefile),
            ShearLug(basefile=basefile),
            Stiffeners(basefile=basefile),
            Welds(basefile=basefile)
        ]
        super().__init__(basefile, headerpath, submodules_list)