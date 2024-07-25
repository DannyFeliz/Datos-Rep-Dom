import pandas as pd
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.types import Integer, String
from dataclasses import dataclass


# Dataclass to hold database credentials
@dataclass
class DatabaseCreds:
    user: str = "root"
    password: str = "admin"
    host: str = "127.0.0.1"
    port: int = 3306
    database: str = "division-territorial-rd"


# Mapping for column names in the Excel file to database column names
COLUMN_NAMES = {
    "Región": "region",
    "Provincia": "provincia",
    "Municipio": "municipio",
    "Distrito municipal": "distrito",
    "Sección": "seccion",
    "Barrio/paraje": "barrio",
    "Sub-barrio": "barrio2",
    "Toponimia o nombre": "nombre",
}

# Define types for the columns
TYPES = {
    "region": "int",
    "provincia": "int",
    "municipio": "int",
    "distrito": "int",
    "seccion": "int",
    "barrio": "int",
    "barrio2": "int",
}

# Mapping to define relationships between tables for foreign keys
RELATIONS_MAPPER = {
    "municipios": {
        "t": "municipios",
        "fk": "provinciaId",
        "t_relation": "provincias",
        "t_relation_ref": "id",
    },
    "distritos": {
        "t": "distritos",
        "fk": "municipioId",
        "t_relation": "municipios",
        "t_relation_ref": "id",
    },
    "secciones_distritos": {
        "t": "secciones",
        "fk": "distritoId",
        "t_relation": "distritos",
        "t_relation_ref": "id",
    },
    "secciones_municipios": {
        "t": "secciones",
        "fk": "municipioId",
        "t_relation": "municipios",
        "t_relation_ref": "id",
    },
    "barrios": {
        "t": "barrios",
        "fk": "seccionId",
        "t_relation": "secciones",
        "t_relation_ref": "id",
    },
    "sub_barrios": {
        "t": "sub_barrios",
        "fk": "barrioId",
        "t_relation": "barrios",
        "t_relation_ref": "id",
    },
}

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def extract_excel_data(sheet_name: str, xls_obj: pd.ExcelFile) -> pd.DataFrame:
    """
    Extract and clean data from an Excel sheet.
    Args:
        sheet_name (str): Name of the Excel sheet.
        xls_obj (pd.ExcelFile): Excel file object.
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = xls_obj.parse(sheet_name=sheet_name).dropna()
    df = (
        df.rename(columns=df.iloc[0])
        .drop(df.index[0])
        .rename(columns=COLUMN_NAMES)
        .astype(TYPES)
    )
    return df


def filter_data(
    filter_name: str, columns: list[str], xls_obj: pd.ExcelFile
) -> pd.DataFrame:
    """
    Filter and extract data based on specified criteria.
    Args:
        filter_name (str): The name of the filter to apply.
        columns (list[str]): List of columns to retain.
        xls_obj (pd.ExcelFile): Excel file object.
    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    combined_df = []

    for sheet in xls_obj.sheet_names:
        df = extract_excel_data(sheet, xls_obj)

        # Define filter conditions
        filters = {
            "provincias": df["municipio"] == 0,
            "municipios": (df["municipio"] > 0) & (df["distrito"] == 0),
            "distritos": (df["municipio"] > 0)
            & (df["distrito"] > 1)
            & (df["seccion"] == 0),
            "secciones": (df["municipio"] > 0)
            & (df["distrito"] > 0)
            & (df["seccion"] > 0)
            & (df["barrio"] == 0),
            "barrios": (df["municipio"] > 0)
            & (df["distrito"] > 0)
            & (df["seccion"] > 0)
            & (df["barrio"] > 0)
            & (df["barrio2"] == 0),
            "sub_barrios": (df["municipio"] > 0)
            & (df["distrito"] > 0)
            & (df["seccion"] > 0)
            & (df["barrio"] > 0)
            & (df["barrio2"] > 0),
        }

        filtered_df = df[filters[filter_name]].dropna().astype(TYPES)
        combined_df.append(filtered_df)

    combined_df = pd.concat(combined_df, ignore_index=True)
    columns_to_drop = [
        column for column in combined_df.columns if column not in columns
    ]
    combined_df.drop(columns=columns_to_drop, inplace=True)
    combined_df.index += 1
    return combined_df


def save_to_sql(df: pd.DataFrame, table_name: str, engine, dtype_mapping: dict):
    """
    Save DataFrame to SQL table.
    Args:
        df (pd.DataFrame): DataFrame to save.
        table_name (str): Name of the SQL table.
        engine: SQLAlchemy engine object.
        dtype_mapping (dict): Mapping of column types.
    """
    df.to_sql(name=table_name, con=engine, dtype=dtype_mapping, if_exists="replace")


def execute_sql_relations(engine, relations: list):
    """
    Execute SQL commands to set up foreign key relations.
    Args:
        engine: SQLAlchemy engine object.
        relations (list): List of SQL commands as strings.
    """
    with engine.connect() as connection:
        for relation in relations:
            connection.execute(text(relation))


def extract_and_save(filename: str, db_creds: DatabaseCreds = DatabaseCreds()):
    """
    Extract data from Excel, filter it, and save to the database.
    Args:
        filename (str): Path to the Excel file.
        db_creds (DatabaseCreds): Database credentials.
    """
    xl = pd.ExcelFile(filename)

    # Define data filters and corresponding columns
    data_filters = {
        "provincias": ["nombre"],
        "municipios": ["provincia", "municipio", "nombre"],
        "distritos": ["provincia", "municipio", "distrito", "nombre"],
        "secciones": ["provincia", "municipio", "distrito", "seccion", "nombre"],
        "barrios": [
            "provincia",
            "municipio",
            "distrito",
            "seccion",
            "barrio",
            "nombre",
        ],
        "sub_barrios": [
            "provincia",
            "municipio",
            "distrito",
            "seccion",
            "barrio",
            "barrio2",
            "nombre",
        ],
    }

    # Filter data based on criteria
    dfs = {
        name: filter_data(name, columns, xl) for name, columns in data_filters.items()
    }

    # Transform data to match database schema and define relationships
    municipios_sql = (
        dfs["municipios"]
        .rename(columns={"provincia": RELATIONS_MAPPER["municipios"]["fk"]})
        .drop(columns=["municipio"])
    )
    distritos_sql = pd.merge(
        dfs["distritos"],
        dfs["municipios"]
        .drop(columns=["nombre"])
        .rename_axis(RELATIONS_MAPPER["distritos"]["fk"])
        .reset_index(),
        on=["provincia", "municipio"],
    )
    distritos_sql.index += 1
    distritos_sql.drop(columns=["provincia", "municipio", "distrito"], inplace=True)
    secciones_sql = pd.merge(
        dfs["secciones"],
        dfs["municipios"]
        .drop(columns=["nombre"])
        .rename_axis(RELATIONS_MAPPER["secciones_municipios"]["fk"])
        .reset_index(),
        how="left",
        on=["provincia", "municipio"],
    )
    secciones_sql = pd.merge(
        secciones_sql,
        dfs["distritos"]
        .drop(columns=["nombre"])
        .rename_axis(RELATIONS_MAPPER["secciones_distritos"]["fk"])
        .reset_index(),
        how="left",
        on=["provincia", "municipio", "distrito"],
    )
    secciones_sql.index += 1
    secciones_sql.drop(
        columns=["provincia", "municipio", "distrito", "seccion"], inplace=True
    )
    barrios_sql = pd.merge(
        dfs["barrios"],
        dfs["secciones"]
        .drop(columns=["nombre"])
        .rename_axis(RELATIONS_MAPPER["barrios"]["fk"])
        .reset_index(),
        on=["provincia", "municipio", "distrito", "seccion"],
    )
    barrios_sql.index += 1
    barrios_sql.drop(
        columns=["provincia", "municipio", "distrito", "seccion", "barrio"],
        inplace=True,
    )
    sub_barrios_sql = pd.merge(
        dfs["sub_barrios"],
        dfs["barrios"]
        .drop(columns=["nombre"])
        .rename_axis(RELATIONS_MAPPER["sub_barrios"]["fk"])
        .reset_index(),
        on=["provincia", "municipio", "distrito", "seccion", "barrio"],
    )
    sub_barrios_sql.index += 1
    sub_barrios_sql.drop(
        columns=["provincia", "municipio", "distrito", "seccion", "barrio", "barrio2"],
        inplace=True,
    )

    # Create database engine
    engine = create_engine(
        f"mysql+pymysql://{db_creds.user}:{db_creds.password}@{
            db_creds.host}:{db_creds.port}/{db_creds.database}"
    )

    # Define column types for each table
    dtype_mapping = {
        "provincias": {"id": Integer(), "nombre": String(50)},
        "municipios": {
            "id": Integer(),
            "provinciaId": Integer(),
            "nombre": String(150),
        },
        "distritos": {"id": Integer(), "municipioId": Integer(), "nombre": String(150)},
        "secciones": {
            "id": Integer(),
            "distritoId": Integer(),
            "municipioId": Integer(),
            "nombre": String(150),
        },
        "barrios": {"id": Integer(), "seccionId": Integer(), "nombre": String(150)},
        "sub_barrios": {"id": Integer(), "barrioId": Integer(), "nombre": String(150)},
    }

    # Save dataframes to SQL tables
    save_to_sql(
        dfs["provincias"].rename_axis("id"),
        "provincias",
        engine,
        dtype_mapping["provincias"],
    )
    save_to_sql(
        municipios_sql.rename_axis("id"),
        "municipios",
        engine,
        dtype_mapping["municipios"],
    )
    save_to_sql(
        distritos_sql.rename_axis("id"), "distritos", engine, dtype_mapping["distritos"]
    )
    save_to_sql(
        secciones_sql.rename_axis("id"), "secciones", engine, dtype_mapping["secciones"]
    )
    save_to_sql(
        barrios_sql.rename_axis("id"), "barrios", engine, dtype_mapping["barrios"]
    )
    save_to_sql(
        sub_barrios_sql.rename_axis("id"),
        "sub_barrios",
        engine,
        dtype_mapping["sub_barrios"],
    )

    # Define and execute SQL commands to set up foreign key relationships
    relation_sql = [
        f"""ALTER TABLE {RELATIONS_MAPPER[relation]["t"]}
        ADD CONSTRAINT fk_{RELATIONS_MAPPER[relation]["t"]}_{RELATIONS_MAPPER[relation]["t_relation"]}
        FOREIGN KEY ({RELATIONS_MAPPER[relation]["fk"]})
        REFERENCES {RELATIONS_MAPPER[relation]["t_relation"]}({RELATIONS_MAPPER[relation]["t_relation_ref"]})"""
        for relation in RELATIONS_MAPPER.keys()
    ]

    execute_sql_relations(engine, relation_sql)


if __name__ == "__main__":
    filename: str = "division_territorial_2021.xlsx"
    logging.info(f"Start parsing {filename}")
    try:
        extract_and_save(filename)
    except Exception as e:
        logging.error(f"Failed parsing: {e}", exc_info=True)
        sys.exit(42)
    logging.info("Parsing Done!")
    sys.exit(0)
