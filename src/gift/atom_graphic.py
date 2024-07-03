from src.gift.atom_config import (
    atom_insert,
    atom_delete,
    atom_update,
    get_normal_table_name,
)
from src.gift.atom import atomunit_shop, AtomUnit
from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter
from dataclasses import dataclass


@dataclass
class AtomPlotlyShape:
    x_atomunit: AtomUnit
    base_width: float = None
    base_h: float = None
    level: float = None
    level_width0: float = None
    level_width1: float = None
    display_text: str = None
    color: str = None

    def set_attrs(self):
        self.base_width = 0.1
        self.base_h = 0.2
        self.level = 0
        self.level_width0 = 0.1
        self.level_width1 = 0.9
        self.display_text = f"{get_normal_table_name(self.x_atomunit.category)} {self.x_atomunit.crud_text} Order: {self.x_atomunit.atom_order}"

    def set_level(self, x_level, x_width0, x_width1, color=None):
        self.level = x_level
        self.level_width0 = x_width0
        self.level_width1 = x_width1
        self.color = color


def get_insert_rect(category: str) -> AtomPlotlyShape:
    x_atomunit = atomunit_shop(category, atom_insert())
    x_atomunit.set_atom_order()
    atom_rect = AtomPlotlyShape(x_atomunit=x_atomunit)
    atom_rect.set_attrs()
    return atom_rect


def get_update_rect(category: str) -> AtomPlotlyShape:
    x_atomunit = atomunit_shop(category, atom_update())
    x_atomunit.set_atom_order()
    atom_rect = AtomPlotlyShape(x_atomunit=x_atomunit)
    atom_rect.set_attrs()
    return atom_rect


def get_delete_rect(category: str) -> AtomPlotlyShape:
    x_atomunit = atomunit_shop(category, atom_delete())
    x_atomunit.set_atom_order()
    atom_rect = AtomPlotlyShape(x_atomunit=x_atomunit)
    atom_rect.set_attrs()
    return atom_rect


def add_rect_text(fig, x, y, text):
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=x,
        y=y,
        text=text,
        showarrow=False,
    )


def add_atom_rect(fig: plotly_Figure, atomplotyshape: AtomPlotlyShape):
    level_bump = atomplotyshape.level * 0.05
    home_form_x0 = atomplotyshape.base_width
    home_form_x1 = 1 - atomplotyshape.base_width
    home_width = home_form_x1 - home_form_x0
    shape_x0 = home_form_x0 + (home_width * atomplotyshape.level_width0)
    shape_x1 = home_form_x0 + (home_width * atomplotyshape.level_width1)
    shape_y0 = level_bump + atomplotyshape.base_h
    shape_y1 = level_bump + atomplotyshape.base_h + 0.05
    x_color = "RoyalBlue"
    if atomplotyshape.color != None:
        x_color = atomplotyshape.color
    fig.add_shape(
        type="rect",
        xref="paper",
        yref="paper",
        x0=shape_x0,
        y0=shape_y0,
        x1=shape_x1,
        y1=shape_y1,
        line=dict(
            color=x_color,
            width=8,
        ),
        fillcolor=None,  # "LightSkyBlue",
    )
    text_y = (shape_y0 + shape_y1) / 2
    text_x = (shape_x0 + shape_x1) / 2
    add_rect_text(fig, x=text_x, y=text_y, text=atomplotyshape.display_text)


def add_beliefunits_circle(fig: plotly_Figure):
    home_form_x0 = 0.2
    home_form_x1 = 1 - 0.2
    home_width = home_form_x1 - home_form_x0
    shape_x0 = home_form_x0 + (home_width * 0.425)
    shape_x1 = home_form_x0 + (home_width * 0.575)
    shape_y0 = 0.325
    shape_y1 = 0.425
    x_color = "Green"
    fig.add_shape(
        type="circle",
        xref="paper",
        yref="paper",
        x0=shape_x0,
        y0=shape_y0,
        x1=shape_x1,
        y1=shape_y1,
        line=dict(
            color=x_color,
            width=8,
        ),
        fillcolor=None,  # "LightSkyBlue",
    )
    text_y = (shape_y0 + shape_y1) / 2
    text_x = (shape_x0 + shape_x1) / 2
    add_rect_text(fig, x=text_x, y=text_y, text="BeliefUnits")


def add_different_ideas_circle(fig: plotly_Figure):
    home_form_x0 = 0.2
    home_form_x1 = 1 - 0.2
    home_width = home_form_x1 - home_form_x0
    shape_x0 = home_form_x0
    shape_x1 = home_form_x0 + home_width
    shape_y0 = 0.54
    shape_y1 = 0.75
    x_color = "Grey"
    fig.add_shape(
        type="circle",
        xref="paper",
        yref="paper",
        x0=shape_x0,
        y0=shape_y0,
        x1=shape_x1,
        y1=shape_y1,
        line=dict(
            color=x_color,
            width=3,
        ),
        fillcolor=None,  # "LightSkyBlue",
    )
    text_y = shape_y1 - 0.01
    text_x = (shape_x0 + shape_x1) / 2
    add_rect_text(fig, x=text_x, y=text_y, text="Different Ideas")


def get_atomunit_base_fig() -> plotly_Figure:
    fig = plotly_Figure()
    fig.update_xaxes(range=[0, 4])
    fig.update_yaxes(range=[0, 15])
    return fig


def atomunit_periodic_table0() -> plotly_Figure:
    fig = get_atomunit_base_fig()

    premise_text = "world_idea_reason_premiseunit"
    world_charunit_insert = get_insert_rect("world_charunit")
    world_char_beliefhold_insert = get_insert_rect("world_char_beliefhold")
    world_ideaunit_insert = get_insert_rect("world_ideaunit")
    world_idea_fiscallink_insert = get_insert_rect("world_idea_fiscallink")
    world_idea_heldbelief_insert = get_insert_rect("world_idea_heldbelief")
    world_idea_healerhold_insert = get_insert_rect("world_idea_healerhold")
    world_idea_factunit_insert = get_insert_rect("world_idea_factunit")
    world_idea_reasonunit_insert = get_insert_rect("world_idea_reasonunit")
    world_idea_reason_premiseunit_insert = get_insert_rect(premise_text)
    world_charunit_update = get_update_rect("world_charunit")
    world_char_beliefhold_update = get_update_rect("world_char_beliefhold")
    world_ideaunit_update = get_update_rect("world_ideaunit")
    world_idea_fiscallink_update = get_update_rect("world_idea_fiscallink")
    world_idea_factunit_update = get_update_rect("world_idea_factunit")
    world_idea_reason_premiseunit_update = get_update_rect(premise_text)
    world_idea_reasonunit_update = get_update_rect("world_idea_reasonunit")
    world_idea_reason_premiseunit_delete = get_delete_rect(premise_text)
    world_idea_reasonunit_delete = get_delete_rect("world_idea_reasonunit")
    world_idea_factunit_delete = get_delete_rect("world_idea_factunit")
    world_idea_heldbelief_delete = get_delete_rect("world_idea_heldbelief")
    world_idea_healerhold_delete = get_delete_rect("world_idea_healerhold")
    world_idea_fiscallink_delete = get_delete_rect("world_idea_fiscallink")
    world_ideaunit_delete = get_delete_rect("world_ideaunit")
    world_char_beliefhold_delete = get_delete_rect("world_char_beliefhold")
    world_charunit_delete = get_delete_rect("world_charunit")
    worldunit_update = get_update_rect("worldunit")

    green_text = "Green"
    world_charunit_insert.set_level(0, 0, 0.25, green_text)
    world_charunit_update.set_level(0, 0.25, 0.75, green_text)
    world_charunit_delete.set_level(0, 0.75, 1, green_text)
    world_char_beliefhold_insert.set_level(1, 0, 0.3, green_text)
    world_char_beliefhold_update.set_level(1, 0.3, 0.7, green_text)
    world_char_beliefhold_delete.set_level(1, 0.7, 1, green_text)
    world_idea_healerhold_insert.set_level(3, 0.2, 0.4)
    world_idea_healerhold_delete.set_level(3, 0.6, 0.8)
    world_idea_heldbelief_insert.set_level(4, 0.2, 0.4)
    world_idea_heldbelief_delete.set_level(4, 0.6, 0.8)
    world_idea_fiscallink_insert.set_level(5, 0.2, 0.4, green_text)
    world_idea_fiscallink_update.set_level(5, 0.4, 0.6, green_text)
    world_idea_fiscallink_delete.set_level(5, 0.6, 0.8, green_text)
    world_ideaunit_insert.set_level(6, 0, 0.3, green_text)
    world_ideaunit_update.set_level(6, 0.3, 0.7, green_text)
    world_ideaunit_delete.set_level(6, 0.7, 1, green_text)
    world_idea_reasonunit_insert.set_level(7, 0.2, 0.4)
    world_idea_reasonunit_update.set_level(7, 0.4, 0.6)
    world_idea_reasonunit_delete.set_level(7, 0.6, 0.8)
    world_idea_reason_premiseunit_insert.set_level(8, 0.2, 0.4)
    world_idea_reason_premiseunit_update.set_level(8, 0.4, 0.6)
    world_idea_reason_premiseunit_delete.set_level(8, 0.6, 0.8)
    world_idea_factunit_insert.set_level(9, 0.2, 0.4)
    world_idea_factunit_update.set_level(9, 0.4, 0.6)
    world_idea_factunit_delete.set_level(9, 0.6, 0.8)
    worldunit_update.set_level(-2, 0, 1, green_text)

    # world_ideaunit_insert = get_insert_rect("world_ideaunit")
    # world_idea_fiscallink_insert = get_insert_rect("world_idea_fiscallink")
    # world_idea_heldbelief_insert = get_insert_rect("world_idea_heldbelief")
    # world_idea_healerhold_insert = get_insert_rect("world_idea_healerhold")
    # world_idea_factunit_insert = get_insert_rect("world_idea_factunit")
    # world_idea_reasonunit_insert = get_insert_rect("world_idea_reasonunit")
    # world_idea_reason_premiseunit_insert = get_insert_rect(premise_text)
    # world_ideaunit_update = get_update_rect("world_ideaunit")
    # world_idea_fiscallink_update = get_update_rect("world_idea_fiscallink")
    # world_idea_factunit_update = get_update_rect("world_idea_factunit")
    # world_idea_reason_premiseunit_update = get_update_rect(premise_text)
    # world_idea_reasonunit_update = get_update_rect("world_idea_reasonunit")
    # world_idea_reason_premiseunit_delete = get_delete_rect(premise_text)
    # world_idea_reasonunit_delete = get_delete_rect("world_idea_reasonunit")
    # world_idea_factunit_delete = get_delete_rect("world_idea_factunit")
    # world_idea_heldbelief_delete = get_delete_rect("world_idea_heldbelief")
    # world_idea_healerhold_delete = get_delete_rect("world_idea_healerhold")
    # world_idea_fiscallink_delete = get_delete_rect("world_idea_fiscallink")
    # world_ideaunit_delete = get_delete_rect("world_ideaunit")
    # worldunit_update = get_update_rect("worldunit")

    # WHEN / THEN

    # Add shapes
    add_atom_rect(fig, world_charunit_insert)
    add_atom_rect(fig, world_char_beliefhold_insert)
    add_atom_rect(fig, world_idea_heldbelief_insert)
    add_atom_rect(fig, world_idea_healerhold_insert)
    add_atom_rect(fig, world_idea_factunit_insert)
    add_atom_rect(fig, world_idea_reasonunit_insert)
    add_atom_rect(fig, world_idea_reason_premiseunit_insert)
    add_atom_rect(fig, world_charunit_update)
    add_atom_rect(fig, world_char_beliefhold_update)
    add_atom_rect(fig, world_idea_factunit_update)
    add_atom_rect(fig, world_idea_reason_premiseunit_update)
    add_atom_rect(fig, world_idea_reasonunit_update)
    add_atom_rect(fig, world_idea_reason_premiseunit_delete)
    add_atom_rect(fig, world_idea_reasonunit_delete)
    add_atom_rect(fig, world_idea_factunit_delete)
    add_atom_rect(fig, world_idea_heldbelief_delete)
    add_atom_rect(fig, world_idea_healerhold_delete)
    add_atom_rect(fig, world_idea_fiscallink_insert)
    add_atom_rect(fig, world_idea_fiscallink_update)
    add_atom_rect(fig, world_idea_fiscallink_delete)
    add_atom_rect(fig, world_ideaunit_insert)
    add_atom_rect(fig, world_ideaunit_update)
    add_atom_rect(fig, world_ideaunit_delete)
    add_atom_rect(fig, world_char_beliefhold_delete)
    add_atom_rect(fig, world_charunit_delete)
    add_atom_rect(fig, worldunit_update)
    add_beliefunits_circle(fig)
    add_different_ideas_circle(fig)

    fig.add_trace(
        plotly_Scatter(
            x=[2.0],
            y=[13],
            text=[
                "Periodic Table of AtomUnits",
            ],
            mode="text",
        )
    )

    return fig