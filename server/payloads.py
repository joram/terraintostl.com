from pydantic import BaseModel


class BuildSTLRequest(BaseModel):
    name: str = "Vancouver Island.stl"
    region: str  # md5 hash of the region in the format [(lat, lng), (lat, lng), ...]
    resolution: int = 1
    z_scale: int = 1