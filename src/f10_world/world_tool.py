from src.f00_instrument.file import create_path
from src.f09_brick.brick_config import get_brick_numbers, get_quick_bricks_column_ref
from src.f09_brick.pandas_tool import get_all_excel_sheet_names
from pandas import read_excel as pandas_read_excel
from dataclasses import dataclass


def get_all_excel_bricksheets(dir: str) -> set[tuple[str, str, str]]:
    return get_all_excel_sheet_names(dir, get_brick_numbers())


@dataclass
class BrickFileRef:
    file_dir: str = None
    file_name: str = None
    sheet_name: str = None
    brick_number: str = None


def get_all_brick_dataframes(dir: str) -> list[BrickFileRef]:
    bricksheets = get_all_excel_bricksheets(dir)
    candidate_bricks = set()
    for dir, filename, sheet_name in bricksheets:
        for brick_number in get_brick_numbers():
            if sheet_name.find(brick_number) >= 0:
                candidate_bricks.add((dir, filename, sheet_name, brick_number))

    valid_bricks = []
    for dir, filename, sheet_name, brick_number in candidate_bricks:
        brick_columns = get_quick_bricks_column_ref().get(brick_number)
        file_path = create_path(dir, filename)
        df = pandas_read_excel(file_path, sheet_name=sheet_name)
        if brick_columns.issubset(set(df.columns)):
            valid_bricks.append(BrickFileRef(dir, filename, sheet_name, brick_number))

    return valid_bricks


# from sqlalchemy import create_engine, Column, Integer, String, Date, Float
# from sqlalchemy.orm import sessionmaker
# from datetime import datetime


# # 2. Create an engine and session
# engine = create_engine("sqlite:///employees.db")
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

# # 3. Read Excel data into a Pandas DataFrame
# df = pd.read_excel("employees.xlsx")

# # 4. Insert data from DataFrame to the database
# for index, row in df.iterrows():
#     employee = Employee(
#         id=row["id"],
#         name=row["name"],
#         position=row["position"],
#         hire_date=pd.to_datetime(row["hire_date"]).date(),
#         salary=row["salary"],
#     )
#     session.add(employee)

# # 5. Commit the session and verify data
# session.commit()

# # Optional: Print out the records
# for employee in session.query(Employee).all():
#     print(f"{employee.id}: {employee.name} - {employee.position} - {employee.salary}")

# # 6. Close the session
# session.close()
