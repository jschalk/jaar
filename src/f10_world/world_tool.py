from src.f08_brick.brick_config import get_brick_numbers
from src.f08_brick.pandas_tool import get_all_excel_sheetnames


def get_all_excel_bricksheets(dir: str) -> set[str, str, str]:
    return get_all_excel_sheetnames(dir, get_brick_numbers())
