from src.f2_bud.bud_tool import (
    budunit_str,
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_ideaunit_str,
    bud_idea_awardlink_str,
    bud_idea_reasonunit_str,
    bud_idea_reason_premiseunit_str,
    bud_idea_teamlink_str,
    bud_idea_healerlink_str,
    bud_idea_factunit_str,
)
from src.f4_gift.atom_config import (
    atom_insert,
    atom_delete,
    atom_update,
    get_normal_table_name,
)
from src.f4_gift.atom import atomunit_shop, AtomUnit
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
    display_str: str = None
    color: str = None

    def set_attrs(self):
        self.base_width = 0.1
        self.base_h = 0.2
        self.level = 0
        self.level_width0 = 0.1
        self.level_width1 = 0.9
        self.display_str = f"{get_normal_table_name(self.x_atomunit.category)} {self.x_atomunit.crud_str} Order: {self.x_atomunit.atom_order}"

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


def add_rect_str(fig, x, y, text):
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
    if atomplotyshape.color is not None:
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
    add_rect_str(fig, x=text_x, y=text_y, text=atomplotyshape.display_str)


def add_groupboxs_circle(fig: plotly_Figure):
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
    add_rect_str(fig, x=text_x, y=text_y, text="GroupBoxs")


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
    add_rect_str(fig, x=text_x, y=text_y, text="Different Ideas")


def get_atomunit_base_fig() -> plotly_Figure:
    fig = plotly_Figure()
    fig.update_xaxes(range=[0, 4])
    fig.update_yaxes(range=[0, 15])
    return fig


def atomunit_periodic_table0() -> plotly_Figure:
    fig = get_atomunit_base_fig()

    premise_str = bud_idea_reason_premiseunit_str()
    bud_acctunit_insert = get_insert_rect(bud_acctunit_str())
    bud_acct_membership_insert = get_insert_rect(bud_acct_membership_str())
    bud_ideaunit_insert = get_insert_rect(bud_ideaunit_str())
    bud_idea_awardlink_insert = get_insert_rect(bud_idea_awardlink_str())
    bud_idea_teamlink_insert = get_insert_rect(bud_idea_teamlink_str())
    bud_idea_healerlink_insert = get_insert_rect(bud_idea_healerlink_str())
    bud_idea_factunit_insert = get_insert_rect(bud_idea_factunit_str())
    bud_idea_reasonunit_insert = get_insert_rect(bud_idea_reasonunit_str())
    bud_idea_reason_premiseunit_insert = get_insert_rect(premise_str)
    bud_acctunit_update = get_update_rect(bud_acctunit_str())
    bud_acct_membership_update = get_update_rect(bud_acct_membership_str())
    bud_ideaunit_update = get_update_rect(bud_ideaunit_str())
    bud_idea_awardlink_update = get_update_rect(bud_idea_awardlink_str())
    bud_idea_factunit_update = get_update_rect(bud_idea_factunit_str())
    bud_idea_reason_premiseunit_update = get_update_rect(premise_str)
    bud_idea_reasonunit_update = get_update_rect(bud_idea_reasonunit_str())
    bud_idea_reason_premiseunit_delete = get_delete_rect(premise_str)
    bud_idea_reasonunit_delete = get_delete_rect(bud_idea_reasonunit_str())
    bud_idea_factunit_delete = get_delete_rect(bud_idea_factunit_str())
    bud_idea_teamlink_delete = get_delete_rect(bud_idea_teamlink_str())
    bud_idea_healerlink_delete = get_delete_rect(bud_idea_healerlink_str())
    bud_idea_awardlink_delete = get_delete_rect(bud_idea_awardlink_str())
    bud_ideaunit_delete = get_delete_rect(bud_ideaunit_str())
    bud_acct_membership_delete = get_delete_rect(bud_acct_membership_str())
    bud_acctunit_delete = get_delete_rect(bud_acctunit_str())
    budunit_update = get_update_rect(budunit_str())

    green_str = "Green"
    bud_acctunit_insert.set_level(0, 0, 0.25, green_str)
    bud_acctunit_update.set_level(0, 0.25, 0.75, green_str)
    bud_acctunit_delete.set_level(0, 0.75, 1, green_str)
    bud_acct_membership_insert.set_level(1, 0, 0.3, green_str)
    bud_acct_membership_update.set_level(1, 0.3, 0.7, green_str)
    bud_acct_membership_delete.set_level(1, 0.7, 1, green_str)
    bud_idea_healerlink_insert.set_level(3, 0.2, 0.4)
    bud_idea_healerlink_delete.set_level(3, 0.6, 0.8)
    bud_idea_teamlink_insert.set_level(4, 0.2, 0.4)
    bud_idea_teamlink_delete.set_level(4, 0.6, 0.8)
    bud_idea_awardlink_insert.set_level(5, 0.2, 0.4, green_str)
    bud_idea_awardlink_update.set_level(5, 0.4, 0.6, green_str)
    bud_idea_awardlink_delete.set_level(5, 0.6, 0.8, green_str)
    bud_ideaunit_insert.set_level(6, 0, 0.3, green_str)
    bud_ideaunit_update.set_level(6, 0.3, 0.7, green_str)
    bud_ideaunit_delete.set_level(6, 0.7, 1, green_str)
    bud_idea_reasonunit_insert.set_level(7, 0.2, 0.4)
    bud_idea_reasonunit_update.set_level(7, 0.4, 0.6)
    bud_idea_reasonunit_delete.set_level(7, 0.6, 0.8)
    bud_idea_reason_premiseunit_insert.set_level(8, 0.2, 0.4)
    bud_idea_reason_premiseunit_update.set_level(8, 0.4, 0.6)
    bud_idea_reason_premiseunit_delete.set_level(8, 0.6, 0.8)
    bud_idea_factunit_insert.set_level(9, 0.2, 0.4)
    bud_idea_factunit_update.set_level(9, 0.4, 0.6)
    bud_idea_factunit_delete.set_level(9, 0.6, 0.8)
    budunit_update.set_level(-2, 0, 1, green_str)

    # bud_ideaunit_insert = get_insert_rect(bud_ideaunit_str())
    # bud_idea_awardlink_insert = get_insert_rect(bud_idea_awardlink_str())
    # bud_idea_teamlink_insert = get_insert_rect(bud_idea_teamlink_str())
    # bud_idea_healerlink_insert = get_insert_rect(bud_idea_healerlink_str())
    # bud_idea_factunit_insert = get_insert_rect(bud_idea_factunit_str())
    # bud_idea_reasonunit_insert = get_insert_rect(bud_idea_reasonunit_str())
    # bud_idea_reason_premiseunit_insert = get_insert_rect(premise_str)
    # bud_ideaunit_update = get_update_rect(bud_ideaunit_str())
    # bud_idea_awardlink_update = get_update_rect(bud_idea_awardlink_str())
    # bud_idea_factunit_update = get_update_rect(bud_idea_factunit_str())
    # bud_idea_reason_premiseunit_update = get_update_rect(premise_str)
    # bud_idea_reasonunit_update = get_update_rect(bud_idea_reasonunit_str())
    # bud_idea_reason_premiseunit_delete = get_delete_rect(premise_str)
    # bud_idea_reasonunit_delete = get_delete_rect(bud_idea_reasonunit_str())
    # bud_idea_factunit_delete = get_delete_rect(bud_idea_factunit_str())
    # bud_idea_teamlink_delete = get_delete_rect(bud_idea_teamlink_str())
    # bud_idea_healerlink_delete = get_delete_rect(bud_idea_healerlink_str())
    # bud_idea_awardlink_delete = get_delete_rect(bud_idea_awardlink_str())
    # bud_ideaunit_delete = get_delete_rect(bud_ideaunit_str())
    # budunit_update = get_update_rect(budunit_str())

    # WHEN / THEN

    # Add shapes
    add_atom_rect(fig, bud_acctunit_insert)
    add_atom_rect(fig, bud_acct_membership_insert)
    add_atom_rect(fig, bud_idea_teamlink_insert)
    add_atom_rect(fig, bud_idea_healerlink_insert)
    add_atom_rect(fig, bud_idea_factunit_insert)
    add_atom_rect(fig, bud_idea_reasonunit_insert)
    add_atom_rect(fig, bud_idea_reason_premiseunit_insert)
    add_atom_rect(fig, bud_acctunit_update)
    add_atom_rect(fig, bud_acct_membership_update)
    add_atom_rect(fig, bud_idea_factunit_update)
    add_atom_rect(fig, bud_idea_reason_premiseunit_update)
    add_atom_rect(fig, bud_idea_reasonunit_update)
    add_atom_rect(fig, bud_idea_reason_premiseunit_delete)
    add_atom_rect(fig, bud_idea_reasonunit_delete)
    add_atom_rect(fig, bud_idea_factunit_delete)
    add_atom_rect(fig, bud_idea_teamlink_delete)
    add_atom_rect(fig, bud_idea_healerlink_delete)
    add_atom_rect(fig, bud_idea_awardlink_insert)
    add_atom_rect(fig, bud_idea_awardlink_update)
    add_atom_rect(fig, bud_idea_awardlink_delete)
    add_atom_rect(fig, bud_ideaunit_insert)
    add_atom_rect(fig, bud_ideaunit_update)
    add_atom_rect(fig, bud_ideaunit_delete)
    add_atom_rect(fig, bud_acct_membership_delete)
    add_atom_rect(fig, bud_acctunit_delete)
    add_atom_rect(fig, budunit_update)
    add_groupboxs_circle(fig)
    add_different_ideas_circle(fig)

    fig.add_trace(
        plotly_Scatter(
            x=[2.0],
            y=[13],
            text=["Periodic Table of AtomUnits"],
            mode="text",
        )
    )

    return fig
