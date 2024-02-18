import pytest

from imxInsights.domain.models.imxSituations import ImxSituationsEnum
from imxInsights.graph.imxGraphBuilder import ImxGraphBuilder

# from imxInsights.graph.queries.sectionGeometryQuery import SectionGeometryGraphQuery


@pytest.mark.slow
def test_imx_graph_project_v124(imx_v124_project_instance):
    new_situation = imx_v124_project_instance.get_situation_repository(ImxSituationsEnum.NewSituation)
    imx_graph = ImxGraphBuilder(new_situation).build_graph()
    assert len(imx_graph.g.edges) == 370
    assert len(imx_graph.g.nodes) == 150

    imx_graph._get_plot()

    from_obj = new_situation.get_by_puic("0aada88e-f8d9-4022-bab1-883666f34b2c")
    to_obj = new_situation.get_by_puic("8cb18979-6b8e-4581-94c4-f4d00c855e6a")
    paths = imx_graph.get_paths_between_imx_objects(from_obj, to_obj)
    assert len(paths) == 2
    # SectionGeometryGraphQuery(imx_graph).create_geojson_files()


@pytest.mark.slow
def test_imx_graph_project_v500(imx_v500_project_instance):
    new_situation = imx_v500_project_instance.get_situation_repository(ImxSituationsEnum.NewSituation)
    imx_graph = ImxGraphBuilder(new_situation).build_graph()
    assert len(imx_graph.g.edges) == 384
    assert len(imx_graph.g.nodes) == 145

    imx_graph._get_plot()

    from_obj = new_situation.get_by_puic("09e58556-846b-4f67-9fa5-c7d5727f41ca")
    to_obj = new_situation.get_by_puic("3969e28b-ad7a-401f-8091-ffc3998745c7")
    paths = imx_graph.get_paths_between_imx_objects(from_obj, to_obj)
    assert len(paths) == 1
    # SectionGeometryGraphQuery(imx_graph).create_geojson_files()
