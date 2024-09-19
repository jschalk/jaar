from src.s0_instrument.plotly_tool import conditional_fig_show
from src.s1_road.jaar_refer import (
    LightSeaGreen_str,
    green_str,
    purple_str,
    blue_str,
    red_str,
    darkred_str,
    black_str,
    bob_str,
    buz_str,
    car_str,
    joc_str,
    luc_str,
    ell_str,
    ric_str,
    sue_str,
    xio_str,
    yao_str,
    zia_str,
)
from src.s1_road.finance import default_money_magnitude
from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter


def add_river_rect(fig: plotly_Figure, x0, xw, y0, yh, display_str, x_color=None):
    if x_color is None:
        x_color = LightSeaGreen_str()
    x1 = x0 + xw
    y1 = y0 + yh
    line_dict = dict(color=x_color, width=4)
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_str(fig, x0, y1, display_str)


def add_column_rect(
    fig: plotly_Figure, x0, y0, x1, y1, display_str, x_color=None, money_supply=None
):
    if x_color is None:
        x_color = purple_str()
    line_dict = dict(color=x_color, width=4)
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    if money_supply is None:
        add_rect_str(fig, x0, y0, display_str)
    if money_supply is not None:
        money_percent = f"{display_str} {int(((y0 - y1) * 12.5))}%"
        add_rect_str(fig, x0, y0, str(money_percent))
        money_amt = round((((y0 - y1) * 12.5) / 100) * money_supply)
        add_rect_str(fig, x0, y0 - 0.2, str(money_amt))


def add_river_row(fig, grants_dict: dict, money_amt, row_x0, row_x1, y0, color=None):
    row_len = row_x1 - row_x0
    grants_sum = sum(grants_dict.values())
    ratio_dict = {grantee: grax / grants_sum for grantee, grax in grants_dict.items()}
    for grantee in grants_dict:
        new_x1 = row_x0 + row_len * ratio_dict.get(grantee)
        add_river_rect(fig, row_x0, y0, new_x1, y0 + 1, grantee, color, money_amt)
        row_x0 = new_x1


def add_river_col(fig, num_dict: dict, money_amt, x0, y0, c_len):
    row_y0 = y0
    row_y1 = row_y0 - c_len
    row_len = row_y1 - row_y0
    num_sum = sum(num_dict.values())
    ratio_dict = {acct_id: acctx / num_sum for acct_id, acctx in num_dict.items()}
    for grantee in num_dict:
        new_y1 = row_y0 + row_len * ratio_dict.get(grantee)
        add_column_rect(fig, x0, row_y0, x0 + 1, new_y1, grantee, None, money_amt)
        row_y0 = new_y1


def add_grants_top(fig, grants_dict: dict, t_y0: int, healer_id, money_amt):
    grants_str = f"{healer_id} Grants"
    dy0 = t_y0 - 1.2
    dy1 = t_y0 - 1.6
    dy2 = t_y0 - 2.2
    dy3 = t_y0 - 3
    ey0 = t_y0 - 0.8
    ey1 = t_y0 - 1.2
    add_river_rect(fig, 1.0, t_y0 - 1, 2.0, t_y0, grants_str, green_str())
    add_river_row(fig, grants_dict, money_amt, 1, 9, t_y0 - 4)
    add_2_curve(fig, path=f"M 1.75,{dy0} C 2,{dy1} 7.4,{dy2} 9,{dy3}", color=blue_str())
    add_2_curve(fig, path=f"M 1.75,{dy0} C 2,{dy1} 1.2,{dy2} 1,{dy3}", color=blue_str())
    add_rect_arrow(fig, 1.75, ey1, 1.5, ey0, blue_str())


def add_taxs_bottom(fig, taxs_dict, b_y0: int, healer_id: str, money_amt: int):
    taxs_str = f"{healer_id} Taxs"
    cy0 = b_y0 + 1.2
    cy1 = b_y0 + 1.6
    cy2 = b_y0 + 2.2
    cy3 = b_y0 + 3
    ay0 = b_y0 + 0.8
    ay1 = b_y0 + 1.2
    add_river_rect(fig, 1.0, b_y0, 2.0, b_y0 + 1, taxs_str, darkred_str())
    add_river_row(fig, taxs_dict, money_amt, 1, 9, y0=b_y0 + 3, color=purple_str())
    add_2_curve(fig, path=f"M 1.75,{cy0} C 2,{cy1} 7.4,{cy2} 9,{cy3}", color=red_str())
    add_2_curve(fig, path=f"M 1.75,{cy0} C 2,{cy1} 1.2,{cy2} 1,{cy3}", color=red_str())
    add_rect_arrow(fig, 1.5, ay0, 1.75, ay1, red_str())


def add_taxs_column(
    fig,
    taxs_dict,
    b_x0: int,
    b_y0: int,
    healer_id: str,
    money_amt: int,
    col_y0: float,
    col_len: float,
):
    taxs_str = f"{healer_id} Taxs"
    cx0 = b_x0 - 0.2
    cx1 = b_x0 - 0.8
    cx2 = b_x0 - 0.4
    cy1 = col_y0 - col_len
    cy2 = cy1 + 2
    cy4 = b_y0 - 1
    cy5 = cy4 - 1
    cy6 = col_y0 + 1
    add_river_rect(fig, b_x0, b_y0 - 1, b_x0 + 1, b_y0, taxs_str, darkred_str())
    add_river_col(fig, taxs_dict, money_amt, b_x0, col_y0, c_len=col_len)
    z1_path = f"M {cx0},{cy4} C {cx2},{cy5} {cx2},{cy6} {b_x0},{col_y0}"
    z2_path = f"M {cx0},{cy4} C {cx1},{cy5} {cx1},{cy2} {b_x0},{cy1}"
    add_2_curve(fig, path=z1_path, color=red_str())
    add_2_curve(fig, path=z2_path, color=red_str())
    ax0 = b_x0 + 0.05
    ax1 = b_x0 - 0.2
    ay0 = b_y0 - 0.7
    add_rect_arrow(fig, ax0, ay0, ax1, cy4, red_str())


def add_rivercycle(fig: plotly_Figure, x0, y0, x1, y1, display_str):
    line_dict = dict(color=LightSeaGreen_str(), width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_str(fig, x0, y1, display_str)


def add_fiscal__rect(
    fig: plotly_Figure,
    x0,
    y0,
    x1,
    y1,
    text1=None,
    text2=None,
    text3=None,
    text4=None,
    color=None,
):
    if color is None:
        color = LightSeaGreen_str()
    y0 -= 0.3
    y1 += 0.3
    x0 -= 0.3
    x1 += 0.3
    line_dict = dict(color=color, width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    mid_x0 = x0 + ((x1 - x0) / 2)
    add_keep_str(fig, mid_x0, y1 - 0.2, text1)
    add_keep_str(fig, mid_x0, y1 - 0.5, text2)
    add_keep_str(fig, mid_x0, y1 - 0.8, text3)
    add_keep_str(fig, mid_x0, y1 - 1.1, text4)


def add_keep_str(fig, x0, y0, text):
    fig.add_annotation(x=x0, y=y0, text=text, showarrow=False, align="left")


def add_rect_str(fig, x0, y0, text):
    x_margin = 0.3
    fig.add_annotation(
        x=x0 + x_margin, y=y0 - x_margin, text=text, showarrow=False, align="center"
    )


def add_2_curve(fig: plotly_Figure, path: str, color: str):
    fig.add_shape(dict(type="path", path=path, line_color=color))


def add_rect_arrow(fig: plotly_Figure, x0, y0, ax0, ay0, color=None, width=None):
    if color is None:
        color = black_str()
    if width is None:
        width = 3
    fig.add_annotation(
        x=x0,  # arrows' head
        y=y0,  # arrows' head
        ax=ax0,  # arrows' tail
        ay=ay0,  # arrows' tail
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        text="",  # arrow only
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=width,
        arrowcolor=color,
    )


def get_fiscal_graphic_base_fig() -> plotly_Figure:
    fig = plotly_Figure()
    fig.update_xaxes(range=[0, 10])
    fig.update_yaxes(range=[0, 10])
    return fig


def grants1_dict() -> dict:
    return {
        bob_str(): 2.2 - 1.0,
        buz_str(): 3.0 - 2.2,
        car_str(): 4.6 - 3.0,
        ric_str(): 5.2 - 4.6,
        sue_str(): 6.6 - 5.2,
        xio_str(): 7.2 - 6.6,
        yao_str(): 8.0 - 7.2,
        zia_str(): 9.0 - 8.0,
    }


def taxs1_dict() -> dict:
    return {
        joc_str(): 100,
        luc_str(): 100,
        ell_str(): 55,
        ric_str(): 60,
        sue_str(): 76,
        xio_str(): 130,
        yao_str(): 100,
        zia_str(): 100,
    }


def rivercycle1_dict() -> dict:
    return {
        bob_str(): 60,
        joc_str(): 200,
        luc_str(): 55,
        ell_str(): 66,
        sue_str(): 76,
        xio_str(): 130,
        yao_str(): 50,
        zia_str(): 70,
    }


def rivercycle2_dict() -> dict:
    return {
        bob_str(): 8,
        joc_str(): 13,
        ell_str(): 1,
        sue_str(): 1,
    }


def rivercycle3_dict() -> dict:
    return {
        bob_str(): 60,
        joc_str(): 200,
        luc_str(): 55,
        xio_str(): 130,
        yao_str(): 50,
        zia_str(): 70,
    }


def rivercycle4_dict() -> dict:
    return {bob_str(): 60, joc_str(): 200}


def add_cycle_to_tax_arrows(fig, cx_src, cx0, cx1, cy1, cy2, cy3, coor_dict):
    for coor_value in coor_dict.values():
        y0 = coor_value.get("y0")
        x2 = coor_value.get("x2")
        z_path = f"M {cx0},{y0} C {cx1},{cy1} {x2},{cy2} {x2+1},{cy3}"
        add_2_curve(fig, path=z_path, color=red_str())
        add_rect_arrow(fig, cx_src, y0, cx0, y0, red_str(), 2)


def get_fiscal_structures0_fig(graphics_bool: bool = False) -> plotly_Figure:
    fig = get_fiscal_graphic_base_fig()
    rx0 = 0
    rx1 = 10
    ry0 = 0
    ry1 = 10

    r_xmid = (rx1 - rx0) / 2
    r_ymid = (ry1 - ry0) / 2

    rect_height = 6
    rect_width = 6

    add_river_rect(fig, 3, 5, 2.0, 6, "People voice", green_str())
    # add_river_rect(fig, 1.0, ry1 - 2, 2.0, ry1 - 6, "People voice", green_str())

    # add_grants_top(fig, grants1_dict(), t_y0=ry0, healer_id=sue_str())
    # add_taxs_bottom(fig, taxs1_dict(), ry1, healer_id=sue_str(), money_amt=mm)
    sue1_p1 = ""
    sue1_p2 = ""
    sue1_p3 = ""
    sue1_p4 = ""
    add_fiscal__rect(fig, rx0, ry0, rx1, ry1, sue1_p1, sue1_p2, sue1_p3, sue1_p4)
    fig.update_xaxes(range=[rx0 - 1, rx1 + 1])
    fig.update_yaxes(range=[ry0 - 1, ry1 + 1])
    fig.add_trace(
        plotly_Scatter(
            x=[5.0, 5.0, 5.0],
            y=[ry0 + 1.5, ry0 + 1, ry0 + 0.5],
            text=[
                "Fiscality Structure",
                "Flow of voiceing to Doing",
                "We all have an interior life where we voice. And then there is what we do.",
            ],
            mode="text",
        )
    )
    conditional_fig_show(fig, graphics_bool)
