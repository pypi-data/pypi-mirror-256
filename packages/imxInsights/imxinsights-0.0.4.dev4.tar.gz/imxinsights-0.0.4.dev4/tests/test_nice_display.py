import pytest

from imxInsights.domain.models.imxSituations import ImxSituationsEnum
from imxInsights.report.imxObjectDisplay import ImxObjectDisplay
from imxInsights.report.refDisplay import ImxRefDisplay


@pytest.mark.slow
def test_nice_display_project_v124(imx_v500_project_instance):
    init_situation = imx_v500_project_instance.get_situation_repository(ImxSituationsEnum.InitialSituation)
    new_situation = imx_v500_project_instance.get_situation_repository(ImxSituationsEnum.NewSituation)
    imx_object_nice_display = ImxObjectDisplay(init_situation, new_situation)
    tester = imx_object_nice_display.get_nice_display("7113cebc-9f02-45c6-b028-66891b5aff29")
    assert tester.display() == "AxleCounterSection 1155AT (7113cebc-9f02-45c6-b028-66891b5aff29:ONLY_NEW)"
    tester = imx_object_nice_display.get_parent_display("cb3f54f3-a2c5-48bd-8c2a-f48cb34892a7")

    assert (
        tester
        == "<NoName (c8714313-3458-4ea3-843b-bf5741ec6a7a)/>.<100.3 (194b6d0d-269d-420a-a510-68f4b7ed329b)/>.<NoName (cb3f54f3-a2c5-48bd-8c2a-f48cb34892a7)/>"  # noqa: E501
    )

    imx_ref_display = ImxRefDisplay(init_situation, new_situation)
    tester = imx_ref_display.get_display("6e3b9697-4abf-4dbd-bfee-45ba21d103a3 06e3b616-30af-44c8-bdd1-adbea00d98d7")

    assert (
        tester
        == 'InsulatedJoint "" (6e3b9697-4abf-4dbd-bfee-45ba21d103a3:INIT_AND_NEW)\nInsulatedJoint "" (06e3b616-30af-44c8-bdd1-adbea00d98d7:INIT_AND_NEW)'  # noqa: E501
    )
