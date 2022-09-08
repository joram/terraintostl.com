import enum

from pydantic import BaseModel


class BoundsEnum(enum.Enum):
    polygon = "polygon"
    bounding_box = "boundingbox"


class BuildSTLRequest(BaseModel):
    name: str = "Vancouver Island"
    region: str  # md5 hash of the region in the format [(lat, lng), (lat, lng), ...]
    resolution: int = 1
    z_scale: int = 1
    bounds: BoundsEnum = BoundsEnum.polygon
    drop_ocean_by: int = 0
