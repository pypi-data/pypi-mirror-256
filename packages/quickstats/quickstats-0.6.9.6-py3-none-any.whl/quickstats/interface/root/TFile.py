from typing import Optional, Union, List, Dict
import numpy as np

class TFile:
    
    def __init__(self, source:Union[str, "ROOT.TFile"]):
        self.initializes(source)
        
    def initialize(self, source:Union[str, "ROOT.TFile"]):
        self.rfile = TFile._open(source)
        
    @staticmethod
    def is_corrupt(f:"ROOT.TFile"):
        if f.IsZombie():
            return True
        if f.GetNkeys() == 0:
            return True
        import ROOT
        if f.TestBit(ROOT.TFile.kRecovered):
            return True
        return False
    
    @staticmethod
    def _open(source:Union[str, "ROOT.TFile"]):
        # source is path to a root file
        if isinstance(source, str):
            import ROOT
            source = ROOT.TFile(source)
            
        if TFile.is_corrupt(source):
            raise RuntimeError(f'root file "{source.GetName()}" is corrupt')
            
        return source        
        
    """
    def make_branches(self, branch_data):
        branches = {}
        return branches
    
    def fill_branches(self, treename:str, branch_data):
        if self.obj is None:
            raise RuntimeError("no active ROOT file instance defined")
        tree = self.obj.Get(treename)
        if not tree:
            raise RuntimeError(f"the ROOT file does not contain the tree named \"{treename}\"")
        n_entries = tree.GetEntriesFast()
        
        for i in range(n_entries):
            for branch in branches:
                
        tree.SetDirectory(self.obj)
        # save only the new version of the tree
        tree.GetCurrentFile().Write("", ROOT.TObject.kOverwrite)
    """
    
    def get_tree(self, name:str, strict:bool=True):
        tree = self.rfile.Get(name)
        if not tree:
            if strict:
                raise RuntimeError(f'In TFile.Get: Tree "{name}" does not exist')
            return None
        return tree

    def close(self):
        self.rfile.Close()
        self.rfile = None