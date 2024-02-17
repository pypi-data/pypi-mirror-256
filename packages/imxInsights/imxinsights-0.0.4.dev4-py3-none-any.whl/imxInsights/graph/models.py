from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, TypeVar

from lxml.etree import Element
from shapely import LineString

from imxInsights.repo.imxRepo import ImxObject

T = TypeVar("T")


@dataclass
class ImxRailConnection:
    imx_object: ImxObject
    puic: str = field(init=False)
    passage_refs: List[str] = field(init=False)

    def __post_init__(self):
        self.puic = self.imx_object.puic
        try:
            self.passage_refs = [_ for _ in self.imx_object.reffed_objects.objects if _.type in ["passageRefs", "PassageRefs"]]
        except Exception as e:
            print(e)


@dataclass
class ImxMicroNodeJumper:
    _element: Element
    from_idx: str = field(init=False)
    to_idx: str = field(init=False)
    is_traversible: bool = field(init=False)
    is_two_way: bool = field(init=False)
    passage_refs: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.from_idx = self._element.attrib.get("fromIndex")
        self.to_idx = self._element.attrib.get("toIndex")
        self.is_traversible = bool(self._element.attrib.get("isTraversible"))
        self.is_two_way = bool(self._element.attrib.get("isTwoWay"))
        try:
            self.passage_refs = self._element.attrib.get("passageRefs").split(" ")
        except Exception as e:
            print(e)
            self.passage_refs = self._element.find(".//{*}PassageRefs").text.split(" ")


@dataclass
class ImxMicroNode:
    _imx_obj: ImxObject
    puic: str = field(init=False)
    junctionRef: str = field(init=False)
    jumpers: List[ImxMicroNodeJumper] = field(default_factory=list)

    def __post_init__(self):
        self.puic = self._imx_obj.puic
        self.junctionRef = self._imx_obj.puic.split("_")[0]
        self.jumpers = [ImxMicroNodeJumper(_) for _ in self._imx_obj.element.findall(".//{http://www.prorail.nl/IMSpoor}Jumper")]


@dataclass
class ImxMicroLinkFromOrToNode:
    _element: Element
    ref: str = field(init=False)
    idx: int = field(init=False)
    micro_node: ImxMicroNode | None = None
    tag: str = field(init=False)

    def __post_init__(self):
        self.ref = self._element.attrib.get("nodeRef")
        self.idx = self._element.attrib.get("portIndex")
        self.tag = self._element.tag.split("}")[1]


@dataclass
class ImxMicroLink:
    _imx_obj: ImxObject
    from_node: ImxMicroLinkFromOrToNode = field(init=False)
    to_node: ImxMicroLinkFromOrToNode = field(init=False)
    _rail_connection: ImxObject = field(init=False)
    puic: str = field(init=False)
    track_ref: str = field(init=False)
    passage_refs: List[str] = field(init=False)

    def __post_init__(self):
        self.puic = self._imx_obj.puic.split("_")[0]
        self.from_node = ImxMicroLinkFromOrToNode(self._imx_obj.element.find(".//{http://www.prorail.nl/IMSpoor}FromMicroNode"))
        self.to_node = ImxMicroLinkFromOrToNode(self._imx_obj.element.find(".//{http://www.prorail.nl/IMSpoor}ToMicroNode"))
        self._rail_connection = self._imx_obj.reffed_objects.objects[0].reffed_object
        self.track_ref = self._rail_connection.properties["@trackRef"] if "@trackRef" in self._rail_connection.properties.keys() else ""
        self.passage_refs = (
            self._rail_connection.properties["@passageRefs"].split(" ") if "@passageRefs" in self._rail_connection.properties.keys() else []
        )

    def link_micro_nodes(self, micro_nodes: dict[str, ImxMicroNode]):
        self.from_node.micro_node = micro_nodes[self.from_node.ref]
        self.to_node.micro_node = micro_nodes[self.to_node.ref]

    def get_centroid_as_xy(self) -> tuple[float, float]:
        x = self._rail_connection.shapely.centroid.x
        y = self._rail_connection.shapely.centroid.y
        return x, y

    def get_shapely(self):
        return self._rail_connection.shapely


class DirectionEnum(Enum):
    UPSTREAM = "upstream"
    DOWNSTREAM = "downstream"
    UNKNOWN = "unknown"


@dataclass
class GraphMicroLink:
    imx_micro_link: ImxMicroLink
    from_direction: DirectionEnum
    to_direction: DirectionEnum
    true_node: ImxMicroNode


class Repo:
    @staticmethod
    def _check_and_return(list_of_things: List[T]) -> T:
        if len(list_of_things) == 1:
            return list_of_things[0]
        if len(list_of_things) > 1:
            raise ValueError("Multiple instances found in repo")
        raise ValueError("Not Found")


@dataclass
class ImxRailConnectionRepo(Repo):
    rail_connections: List[ImxRailConnection] = field(default_factory=list)

    def get_by_puic(self, puic: str) -> ImxRailConnection:
        _ = [item for item in self.rail_connections if item.puic == puic]
        return self._check_and_return(_)


@dataclass
class MicroNodeRepo(Repo):
    micro_nodes: List[ImxMicroNode] = field(default_factory=list)

    def get_by_puic(self, puic: str) -> ImxMicroNode:
        _ = [item for item in self.micro_nodes if item.junctionRef == puic]
        return self._check_and_return(_)


@dataclass
class MicroLinkRepo(Repo):
    micro_links: List[ImxMicroLink] = field(default_factory=list)

    def get_by_puic(self, puic: str) -> ImxMicroLink:
        _ = [item for item in self.micro_links if item.puic == puic]
        return self._check_and_return(_)


class MicroLinkConnectionTypeEnum(Enum):
    POINT = "point"
    LINE_START = "line_start"
    LINE_END = "line_end"


@dataclass
class MicroLinkConnection:
    measure: float
    ref: str
    direction: str
    connection_type: MicroLinkConnectionTypeEnum
    item: any  # Assuming 'item' can be of any type for now

    @staticmethod
    def create_from_rail_info(rail_con_info, imx_object):
        """Creates MicroLinkConnection instances from rail connection information.

        Args:
            rail_con_info: The rail connection information object.
            imx_object: The IMX object associated with the rail connection.

        Returns:
            List[MicroLinkConnection]: A list containing one or more MicroLinkConnection instances.
        """
        connections = []
        if hasattr(rail_con_info, "at_measure"):
            # Handle point-type rail connections.
            connections.append(
                MicroLinkConnection(
                    rail_con_info.at_measure, rail_con_info.ref, rail_con_info.direction, MicroLinkConnectionTypeEnum.POINT, imx_object
                )
            )
        else:
            # Handle line-type rail connections, assuming they have 'from_measure' and 'to_measure'.
            # todo: check if present, else give error warning.
            if not hasattr(rail_con_info, "from_measure") or not hasattr(rail_con_info, "to_measure"):
                pass
            else:
                connections.extend(
                    [
                        MicroLinkConnection(
                            rail_con_info.from_measure,
                            rail_con_info.ref,
                            rail_con_info.direction,
                            MicroLinkConnectionTypeEnum.LINE_START,
                            imx_object,
                        ),
                        MicroLinkConnection(
                            rail_con_info.to_measure,
                            rail_con_info.ref,
                            rail_con_info.direction,
                            MicroLinkConnectionTypeEnum.LINE_END,
                            imx_object,
                        ),
                    ]
                )
        return connections


@dataclass
class MicroLinkConnectionRepo:
    micro_links: Dict[str, list[MicroLinkConnection]] = field(default_factory=list)

    def get_by_puic(self, puic: str) -> List[MicroLinkConnection]:
        return self.micro_links[puic]


@dataclass
class PathEdgeData:
    source_direction: DirectionEnum
    target_direction: DirectionEnum
    true_node: str


@dataclass
class PathEdge:
    source: str
    target: str
    data: Optional[PathEdgeData] = None


@dataclass
class GraphRoute:
    path: List[PathEdge] = field(default_factory=list)
    geometry: LineString = None
    objects_on_route: List[Any] = field(default_factory=list)
