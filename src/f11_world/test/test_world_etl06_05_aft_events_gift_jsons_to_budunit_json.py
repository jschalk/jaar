from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_name_str, fiscal_title_str
from src.f07_fiscal.fiscal_config import cumlative_minute_str, hour_title_str
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.idea_db_tool import upsert_sheet, sheet_exists
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import env_dir_setup_cleanup
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


# ESTABLISH
# fiscal/owners/events each with a gift.json
# for each owner
#   grab all events numbers
#   create sorted list of all events numbers
#   get min event: create BudUnit from giftunit. Save json
#   for event_id in smallest to  largerst event_ints
#       get previous budunit,
#       apply gift to budunit
#       save budunit json
#
# that's it.
