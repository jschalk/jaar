from ch20_brick._ref.ch20_semantic_types import SheetName
from ch99_glossary.ch_keyword import Ch20Keywords as kw, ExampleStrs as exx
from inspect import getdoc as inspect_getdoc


def test_SheetName_Exists():
    # ESTABLISH
    br00104_str = "br00104"
    # WHEN
    br00104_sheetname = SheetName(br00104_str)
    # THEN
    assert br00104_sheetname == br00104_str
    doc_str = f"A string used as {kw.SheetName} for SpreadSheet files."
    assert inspect_getdoc(br00104_sheetname) == doc_str
