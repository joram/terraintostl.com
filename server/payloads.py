import enum
from typing import Optional

from pydantic import BaseModel


class BoundsEnum(enum.Enum):
    polygon = "polygon"
    bounding_box = "boundingbox"


class RequestType(enum.Enum):
    peak = "peak"
    polygon = "polygon"


class BuildSTLRequest(BaseModel):
    session_key: str
    request_type: RequestType
    name: str = "Vancouver Island"
    resolution: float = 1.0

    # md5 hash of the region in the format [(lat, lng), (lat, lng), ...]
    region: Optional[str]
    z_scale: Optional[int] = 1
    bounds: Optional[BoundsEnum] = BoundsEnum.polygon
    drop_ocean_by: Optional[int] = 0
    percentage_processed: Optional[float] = 0.0
