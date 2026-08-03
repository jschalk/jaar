from ch41_wheel.wheel_builder import (
    draw_trapezoid,
    draw_trapezoid_row,
    draw_trapezoid_stack,
    draw_contacts_row,
    draw_infinity_contact,
    draw_contact_rows,
    get_standard_drawing,
    save_to_images_dir,
    rebuild_markdown_wheel_theory_images,
    get_markdown_wheel_theory_drawings,
)
from drawsvg import Drawing
from copy import deepcopy as copy_deepcopy
from pathlib import Path
from os.path import exists as os_path_exists


def _get_elements_count(d: Drawing) -> int:
    return len(d.__dict__.get("elements"))


def save_example_image(d: Drawing, filebasename: str = "theory"):
    # Save the SVG
    output_file_path = save_to_images_dir(d, filebasename)
    print(f"Saved SVG to: {output_file_path}")


def test_draw_contacts_row_SetsAttr_Scenario0_4People():
    # ESTABLISH
    contacts = [
        {"contact_name": "Alice", "face_status": "Face"},
        {"contact_name": "Bob", "face_status": "needs"},
        {"contact_name": "Christopher", "face_status": "needs"},
        {"contact_name": "Dee", "face_status": "Face"},
    ]

    # WHEN
    drawing = draw_contacts_row(contacts)

    # THEN
    assert drawing
    # save_example_image(drawing)
    # assert 1 == 2


def test_draw_infinity_contact_SetsAttr_Scenario0_ContactWithFace(rebuild_images):
    # ESTABLISH
    # drawing = Drawing(2 * x_margin + 2 * radius, 2 * y_margin + radius, origin=(0, 0))
    drawing = get_standard_drawing()
    contact_name = "Doug Something of Someplace"
    face_status = "Face"
    font_size = 14
    face_font_size = 18
    x0 = 55
    y0 = 20
    d0_old = copy_deepcopy(drawing)
    assert drawing.__dict__ == d0_old.__dict__

    # WHEN
    draw_infinity_contact(
        d=drawing,
        x0=x0,
        y0=y0,
        font_size=font_size,
        face_font_size=face_font_size,
        contact_name=contact_name,
        face_status=face_status,
    )

    # THEN
    assert drawing.__dict__ != d0_old.__dict__
    # if rebuild_images:
    #     save_example_image(drawing)


def test_draw_trapezoid_SetsAttr_Scenario0_No_height():
    # ESTABLISH
    d0 = get_standard_drawing()
    d0_old = copy_deepcopy(d0)
    assert d0.__dict__ == d0_old.__dict__

    # WHEN
    draw_trapezoid(d0, 50, 50, 50, "test2")

    # THEN
    assert d0.__dict__ != d0_old.__dict__
    print(f"{d0_old.__dict__.get("elements")=}")
    print(f"    {d0.__dict__.get("elements")=}")
    assert _get_elements_count(d0) != _get_elements_count(d0_old)


def test_draw_trapezoid_SetsAttr_Scenario1_height_Passed():
    # ESTABLISH
    d0 = get_standard_drawing()
    d0_old = copy_deepcopy(d0)
    assert d0.__dict__ == d0_old.__dict__

    # WHEN
    draw_trapezoid(d0, 50, 50, 50, "test2", height=80)

    # THEN
    assert d0.__dict__ != d0_old.__dict__
    print(f"{d0_old.__dict__.get("elements")=}")
    print(f"    {d0.__dict__.get("elements")=}")
    assert _get_elements_count(d0) != _get_elements_count(d0_old)
    # save_example_image(d0)


def test_draw_trapezoid_row_SetsAttr_Scenario0_1Element():
    # ESTABLISH
    d0 = get_standard_drawing()
    d0_old = copy_deepcopy(d0)
    assert d0.__dict__ == d0_old.__dict__

    # WHEN
    draw_trapezoid_row(d0, 50, 50, 50, ["test2"])

    # THEN
    assert d0.__dict__ != d0_old.__dict__
    print(f"{d0_old.__dict__.get("elements")=}")
    print(f"    {d0.__dict__.get("elements")=}")
    assert _get_elements_count(d0) != _get_elements_count(d0_old)
    # save_example_image(d0)


def test_draw_trapezoid_row_SetsAttr_Scenario1_3Elements():
    # ESTABLISH
    d0 = get_standard_drawing()
    d0_old = copy_deepcopy(d0)
    assert d0.__dict__ == d0_old.__dict__

    # WHEN
    draw_trapezoid_row(d0, 50, 50, 50, ["test0", "test1", "test2"])

    # THEN
    assert d0.__dict__ != d0_old.__dict__
    print(f"{d0_old.__dict__.get("elements")=}")
    print(f"    {d0.__dict__.get("elements")=}")
    assert _get_elements_count(d0) != _get_elements_count(d0_old)
    # save_example_image(d0)


def test_draw_trapezoid_stack_SetsAttr_Scenario0_3Elements():
    # ESTABLISH
    d0 = get_standard_drawing()
    d0_old = copy_deepcopy(d0)
    assert d0.__dict__ == d0_old.__dict__

    # WHEN
    draw_trapezoid_stack(d0, 70, 50, 70, [["test0"], ["test1", "test2"]])

    # THEN
    assert d0.__dict__ != d0_old.__dict__
    print(f"{d0_old.__dict__.get("elements")=}")
    print(f"    {d0.__dict__.get("elements")=}")
    assert _get_elements_count(d0) != _get_elements_count(d0_old)
    # save_example_image(d0)


def test_draw_trapezoid_stack_SetsAttr_Scenario1_7Elements():
    # ESTABLISH
    d0 = get_standard_drawing()
    d0_old = copy_deepcopy(d0)
    label_rows = [["test0"], ["test1", "test2"], ["t3", "t4", "t5", "t6"]]
    assert d0.__dict__ == d0_old.__dict__

    # WHEN
    draw_trapezoid_stack(d0, 70, 50, 70, label_rows)

    # THEN
    assert d0.__dict__ != d0_old.__dict__
    assert _get_elements_count(d0) != _get_elements_count(d0_old)
    # save_example_image(d0)
    # assert 1 == 2


def test_draw_trapezoid_stack_SetsAttr_Scenario2_ManyElements():
    # ESTABLISH
    d0 = get_standard_drawing()
    d0_old = copy_deepcopy(d0)
    label_rows = [
        ["t0"],
        ["t1", "t2"],
        ["t3", "t4", "t5", "t6"],
        ["t7", "t8", "t9"],
        ["tx"],
        ["ty"],
    ]
    assert d0.__dict__ == d0_old.__dict__

    # WHEN
    draw_trapezoid_stack(d0, 30, 300, 70, label_rows)

    # THEN
    assert d0.__dict__ != d0_old.__dict__
    assert _get_elements_count(d0) != _get_elements_count(d0_old)
    # save_example_image(d0)
    # assert 1 == 2


def test_draw_contact_rows_SetsAttr_Scenario0_2Rows():
    # ESTABLISH
    rows = [
        [("Alice", 5, "need"), ("Bob", 20)],
        [("Sue", 12, "need"), ("Christopher", 2, "need")],
    ]
    d0_curr = get_standard_drawing()
    d0_old = copy_deepcopy(d0_curr)
    assert d0_curr.__dict__ == d0_old.__dict__

    # WHEN
    draw_contact_rows(d0_curr, rows)

    # THEN
    assert d0_curr.__dict__ != d0_old.__dict__
    assert _get_elements_count(d0_curr) != _get_elements_count(d0_old)
    # save_example_image(drawing)


def test_rebuild_markdown_wheel_theory_images_SpecialCreateImages(rebuild_images):
    # ESTABLISH / WHEN / THEN
    if rebuild_images:
        svg_image_paths = rebuild_markdown_wheel_theory_images()
        for svg_image_path in svg_image_paths:
            print(f"Saved {svg_image_path}")


def test_draw_contact_rows_SetsAttr_Scenario0_MatchesStaticFile():
    # ESTABLISH
    for filebasename, drawing in get_markdown_wheel_theory_drawings().items():
        project_dir = Path(__file__).resolve().parent.parent
        # Save the SVG
        output_file_path = project_dir / "images" / f"{filebasename}.svg"
        assert os_path_exists(output_file_path)

        # WHEN
        curr_svg_text = output_file_path.read_text()

        # THEN
        assert curr_svg_text == drawing.as_svg()
        print(f"{output_file_path=}")
