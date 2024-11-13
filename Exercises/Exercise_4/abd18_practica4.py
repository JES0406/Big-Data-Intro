import ray
from ray.data import *
import pandas as pd
from time import time

def query_1(df):
    # Obtén en qué estados nacieron más bebés en 2003
    bebes_2003 = df.filter(lambda row: row['year'] == 2003)
    estados_2003 = bebes_2003.groupby("state").count()
    return estados_2003.take_batch()

def query_2(df):
    # Obtén la media de peso de los bebés por año y estado.
    return df.groupby(["year", "state"]).mean("weight_pounds").sort("year", "state").take_batch()

def query_3(df):
    # Evolución por año y por mes del número de niños y niñas nacidas 
    # (Resultado por separado con una sola consulta, cada registro debe tener 4 columnas: año, mes, numero de niños nacidos, numero de niñas nacidas).

    # Group by 'year', 'month', and 'is_male' to get the birth count
    grouped_df = df.groupby(["year", "month", "is_male"]).count().rename_columns({"count()": "num_nacimientos"})

    # Separate male and female birth counts
    males_df = grouped_df.filter(lambda row: row["is_male"] == 1).map(lambda row: {
        "year": row["year"],
        "month": row["month"],
        "num_ninos_nacidos": row["num_nacimientos"],
        "num_ninas_nacidas": 0
    })

    females_df = grouped_df.filter(lambda row: row["is_male"] == 0).map(lambda row: {
        "year": row["year"],
        "month": row["month"],
        "num_ninas_nacidas": row["num_nacimientos"],
        "num_ninos_nacidos": 0
    })

    # Combine the male and female datasets
    combined_df = males_df.union(females_df)

    # Group again to sum up births by month and year for each gender
    final_df = combined_df.groupby(["year", "month"]).sum(["num_ninas_nacidas", "num_ninos_nacidos"])

    return final_df.take_batch()

def query_4(df):
    # Obtén los tres meses de 2005 en que nacieron más bebés.
    bebes_2005 = df.filter(lambda row: row['year'] == 2005)
    meses_2005 = (
        bebes_2005.groupby("month")
        .count()  # This creates a column named "count()"
        .sort("count()", descending=True)  # Sort by the actual count column
        .limit(3)
    )
    return meses_2005.take_batch()

def query_5(df):
    # Obtén los estados donde las semanas de gestación son superiores a la media de EE. UU.
    gest_time_mean = df.mean("gestation_weeks")

    df_states = df.groupby("state").mean("gestation_weeks")

    # We remove the Na value
    df_states = df_states.filter(lambda x: type(x["mean(gestation_weeks)"]) != type(None))

    df_states.filter(lambda x: x["mean(gestation_weeks)"] > gest_time_mean).show()
    return df_states.take_batch()

def query_6(df):
    # Obtén los cinco estados donde la media de edad de las madres ha sido mayor.

    df.groupby("state").mean("mother_age").sort("mean(mother_age)", True).limit(5)
    return df.take_batch()

def query_7(df):
    # Influencia en el peso del bebé y semanas de gestación en partos múltiples.
    return df.groupby("plurality").mean(["weight_pounds", "gestation_weeks"]).take_batch()

if __name__ == "__main__":

    path = ""
    path = "/home/icai/practicas/practica4/"

    times = []
    results = []

    ray.init()

    t_0_0 = time()

    # Carga el fichero de datos en un DataFrame.

    df = read_csv(f"{path}natality.csv")

    # Field gestation_weeks has incompatible types: double vs int64
    df = df.map_batches(lambda batch: pd.DataFrame(batch).astype({'gestation_weeks': 'float64'}))

    df = df.drop_columns(["source_year","day","wday","child_race","apgar_1min","apgar_5min",
                          "mother_residence_state","mother_race","lmp","mother_married","mother_birth_state","cigarette_use",
                          "cigarettes_per_day","alcohol_use","drinks_per_week","weight_gain_pounds","born_alive_alive","born_alive_dead",
                          "born_dead","ever_born","father_race","father_age","record_weight"])

    queries = [query_1, query_2, query_3, query_4, query_5, query_6, query_7]

    for query in queries:
        t0 = time()
        results.append(query(df))
        times.append(time() - t0)   

    for i, _ in enumerate(queries):
        print(f"Query {i+1}:")
        print(results[i])
        print(f"Time elapsed: {times[i]}")

    print(f"Total time elapsed: {time() - t_0_0}")

    ray.shutdown()
