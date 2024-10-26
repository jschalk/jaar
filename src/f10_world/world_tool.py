from src.f00_instrument.pandas_tool import get_all_excel_sheetnames
from src.f08_brick.brick_config import get_brick_numbers


def get_all_excel_bricksheets(dir: str) -> set[str, str, str]:
    return get_all_excel_sheetnames(dir, get_brick_numbers())
