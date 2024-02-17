from __future__ import annotations

from ormspace import model as md



class SpaceModel(md.Model):
    
    async def setup_instance(self):
        pass


    
class SpaceSearchModel(SpaceModel, md.SearchModel):
    pass