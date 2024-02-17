import pytest

from imxInsights.domain.models.imxSituations import ImxSituationsEnum
from imxInsights.graph.builder import ImxGraphBuilder


@pytest.mark.slow
def test_imx_graph_project_v500(imx_v500_project_instance):
    new_situation = imx_v500_project_instance.get_situation_repository(ImxSituationsEnum.NewSituation)
    graph = ImxGraphBuilder(new_situation).build_graph()
    graph._get_plot()
