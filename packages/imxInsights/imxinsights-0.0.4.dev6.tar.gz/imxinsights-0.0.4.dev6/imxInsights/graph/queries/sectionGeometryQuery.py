import asyncio
from dataclasses import dataclass
from typing import List, cast

from loguru import logger
from shapely import LineString
from shapely.ops import linemerge

from imxInsights import GeoJsonFeature, GeoJsonFeatureCollection, ImxObject, dump
from imxInsights.graph.imxGraph import ImxGraph
from imxInsights.utils.shapely_helpers import ShapelyTransform


@dataclass
class ImxGraphSectionQueryResult:
    section: ImxObject
    geometry: LineString


class SectionGeometryGraphQuery:
    def __init__(self, imx_graph: ImxGraph):
        self.g = imx_graph

    async def _get_section_geometry(self, refs: List[str]) -> LineString:
        # todo: make get path loop async task
        refs_mapping = {uuid: [other_uuid for other_uuid in refs if other_uuid != uuid] for uuid in refs}
        line_strings = []

        for key, values in refs_mapping.items():
            from_obj = self.g.imx_situation.get_by_puic(key)
            if from_obj is None:
                logger.warning(f"Object {key} not found in situation")
                continue

            for item in values:
                to_obj = self.g.imx_situation.get_by_puic(item)
                if to_obj is None:
                    logger.warning(f"Object {item} not found in situation")
                    continue

                paths = self.g.get_paths_between_imx_objects(from_obj, to_obj)
                for path in paths:
                    line_strings.append(path.geometry)

        return linemerge(line_strings).buffer(0.01)

    async def _get_section_async(self, section: ImxObject, ref_type: List[str]) -> ImxGraphSectionQueryResult:
        refs = [_.key for _ in section.reffed_objects.objects if _.type in ref_type]
        line_string = await self._get_section_geometry(refs)
        return ImxGraphSectionQueryResult(section, line_string)

    async def _get_all_sections_async(self, section_type: str, ref_type: List[str]) -> List[ImxGraphSectionQueryResult]:
        sections = self.g.imx_situation.get_by_types([section_type])
        tasks = [self._get_section_async(section, ref_type) for section in sections]
        result = await asyncio.gather(*tasks)
        return cast(List[ImxGraphSectionQueryResult], result)

    def get_section(self, section: ImxObject, ref_type: List[str]) -> ImxGraphSectionQueryResult:
        return asyncio.run(self._get_section_async(section, ref_type))

    def get_all_section(self, section_type: str, ref_type: List[str]) -> List[ImxGraphSectionQueryResult]:
        return asyncio.run(self._get_all_sections_async(section_type, ref_type))

    @staticmethod
    def _create_geojson_features(query_results: List[ImxGraphSectionQueryResult]):
        features = []
        for result in query_results:
            features.append(GeoJsonFeature([ShapelyTransform.rd_to_wgs(result.geometry)], result.section.properties | {"type": result.section.tag}))
        return features

    @staticmethod
    def _save_as_geojson(fc, file_name="test_path.geojson"):
        with open(file_name, "w") as file:
            dump(fc, file)

    def create_geojson_files(self):
        try:
            features = self.get_all_section("AxleCounterSection", ["AxleCounterDetectionPointRefs"])
            tester = self._create_geojson_features(features)
            self._save_as_geojson(GeoJsonFeatureCollection(tester))

            features = self.get_all_section("TrackCircuit", ["InsulatedJointRefs"])
            tester = self._create_geojson_features(features)
            self._save_as_geojson(GeoJsonFeatureCollection(tester))

            print()
        except RuntimeError as e:
            print(f"Error running async function: {e}")
