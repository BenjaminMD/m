from ezplot import plot_defaults, scatter_w_outline, create_basic_plot
from ezpdf import ParseResDir
from glob import glob
from pathlib import Path
from datetime import datetime, timedelta
from typing import Type, TypeAlias, Dict, Union
import numpy.typing as npt
import pandas as pd
import numpy as np
import h5py


StrArray: TypeAlias = npt.NDArray[np.str_]
FloatArray: TypeAlias = npt.NDArray[np.float64]
DateArray: TypeAlias = npt.NDArray[np.datetime64]

Kwargs = Dict[str, Union[str, int, Type[str]]]


def parse_date(date_raw: str, time_raw: str) -> datetime:
    base_date: datetime = datetime(1900, 1, 1)
    date: datetime = base_date + timedelta(days=float(date_raw))
    time: timedelta = timedelta(float(f"0.{time_raw}"))
    return date + time


def read_temperture_file(file_path: Path) -> pd.DataFrame:
    t_raw: StrArray
    T_raw: StrArray
    params: Kwargs = {"skiprows": 1, "delimiter": ";", "dtype": str}
    t_raw, T_raw = np.loadtxt(file_path, **params).T[[0, 1]]

    date_raw: StrArray
    time_raw: StrArray
    date_raw, time_raw = np.char.partition(t_raw, sep=",")[:, [0, 2]].T

    dt = np.vectorize(parse_date)(date_raw, time_raw)

    T: FloatArray = np.char.replace(T_raw, ",", ".").astype(np.float64)

    df = pd.DataFrame({"dt": dt, "T": T})

    return df


def compute_time_passed(df: pd.DataFrame) -> pd.DataFrame:
    df["t / s"] = (df["dt"] - df["dt"].min()).dt.total_seconds()
    return df


def merge_df(df: pd.DataFrame, dfT: pd.DataFrame) -> pd.DataFrame:
    # match up times in df and dfT and add T to each file_name
    ...


def get_time_h5(file_name: Path) -> datetime:
    with h5py.File(file_name, "r") as f:
        time_b = f['/info/end_time'][()]
    time_s: str = time_b.decode("utf-8")

    time_s = time_s.replace("Z", "")
    time_s = time_s.replace("T", " ")

    time: datetime = datetime.strptime(time_s, "%Y-%m-%d %H:%M:%S")


    return time


def get_combined_df(
        time_files: StrArray,
        res_glob: str,
        par_file: Path,
        T_file: Path) -> pd.DataFrame:
    res = ParseResDir(res_glob, par_file)
    df = res.df
    df["mtime"] = np.nan

    for fn, file in zip(df["file_name"], time_files):
        time = get_time_h5(file)
        df.loc[df["file_name"] == fn, "mdt"] = time

    df["mt / s"] = (df["mdt"] - df["mdt"].min()).dt.total_seconds()

    print(df.head())
    dfT = read_temperture_file(T_file)
    dfT = compute_time_passed(dfT)

    df = merge_df(df, dfT)

    return df


def main():
    dat_base = Path(__file__).parent / "../0d/"
    res_glob = f"{Path(__file__).parent}/../0d/res/*res"
    par_file = Path(__file__).parent / "parameters.wAl2O3.txt"
    T_file = Path(__file__).parent / ".." / "0d" / "220121_UC1_Al2O3.csv"
    t_files = glob(f"{dat_base}/h5/*.h5")


    get_time_h5(t_files[0])
    df = get_combined_df(t_files, res_glob, par_file, T_file)




if __name__ == "__main__":
    main()
