
from pathlib import Path

from hilti_profis import xmlparser
from hilti_profis.Model import DesignModel

class PE:
    def __init__(self, basefile: Path|None = None) -> None:
        self.basefile: Path = basefile or Path(__file__).parent / 'basefile.pe'
        self.data: dict = {}
        self.Model = DesignModel(basefile=xmlparser.read_xml(self.basefile))
        
    def __repr__(self) -> str:
        return f'PE(basefile={self.basefile})'
    
    def __str__(self) -> str:
        return "Hilti Profis file generation module"
        
    def __apply_baseconfig(self) -> dict:
        """Applies cofigs from basefile"""
        return __update_dict(
            base_dict=xmlparser.read_xml(filepath=self.basefile),
            override_dict=self.data)

    def save(self, filepath: Path):
        """Saves the modified config to file"""
        return xmlparser.save_xml(filepath=filepath, data=self.__apply_baseconfig())

def __update_dict(base_dict: dict, override_dict: dict) -> dict:
    """Applies dict values from `override_dict` to `base_dict`"""
    override_dict = override_dict.copy()
    for kb, vb in base_dict.items():
        ko = kb
        vo = override_dict.get(ko)
        if vo is None:
            vo = vb
        if isinstance(vb, dict):
            kb = __update_dict(vb, vo)
        else:
            override_dict[ko] = vo
    return override_dict