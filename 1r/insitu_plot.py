from ezplot import plot_defaults, scatter_w_outline, create_basic_plot
from ezpdf import ParseResDir
from glob import glob
from pathlib import Path
from datetime import datetime, timedelta
import datetime as dt
from typing import Type, TypeAlias, Dict, Union
import numpy.typing as npt
import pandas as pd
import numpy as np
import h5py

import matplotlib.pyplot as plt

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


def get_T(df_dt, df_temp, start_time, end_time):
    df_dt['dt'] = pd.to_datetime(df_dt['dt'])
    df_temp['dt'] = pd.to_datetime(df_temp['dt'])
    period = df_temp[(df_temp.dt >= start_time) & (df_temp.dt <= end_time)]
    if len(period) == 0:
        # find first data point earlier than start_time
        start_time = df_temp[df_temp.dt < start_time].dt.max()
        period = df_temp[(df_temp.dt >= start_time) & (df_temp.dt <= end_time)]
    T_avg = period["T"].mean()
    T_avg = round(T_avg, 2)
    return T_avg


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
        df.loc[df["file_name"] == fn, "dt"] = time + pd.Timedelta(days=2)

    df["t / s"] = (df["dt"] - df["dt"].min()).dt.total_seconds() 

    dfT = read_temperture_file(T_file)
    dfT = compute_time_passed(dfT)
    dfT.dt = dfT.dt - pd.Timedelta(hours=1)
    t_s = df['dt']
    t_e = df['dt'] +  pd.Timedelta(seconds=31)

    df['T_avg / °C'] = [get_T(df, dfT, s, e) for s, e in zip(t_s, t_e)]
    return df

def add_ms(df: pd.DataFrame, df_ms: pd.DataFrame) -> pd.DataFrame:
    start_time = df.dt
    end_time = df.dt +  pd.Timedelta(seconds=31)
    ms = []
    for s, e in zip(start_time, end_time):
        period = df_ms[(df_ms['time'] >= s) & (df_ms['time'] <= e)]
        if len(period) == 0:
            # find first data point earlier than start_time
            s = df_ms[df_ms['time'] < s]["time"].max()
            period = df_ms[(df_ms['time'] >= s) & (df_ms['time'] <= e)]
        ms.append(period.mean())
    print(ms, df_ms.columns)
    df[df_ms.columns] = ms
    return df


def main():
    
    _()

def ms():
    path_to_ms = Path(__file__).parent / ".." / "0d" / "MS_UC1.csv"
    t, tt, H, He, N2, CH4, H2O, CO, O2, CO2, *_ = np.loadtxt(
                                path_to_ms,
                                skiprows=29,
                                delimiter=',',
                                dtype=str).T
    tt = tt.astype(int)
    time = datetime.strptime("21/01/2022 01:02:33", "%d/%m/%Y %H:%M:%S")
    time = np.array([time + timedelta(days=2, milliseconds=int(t)) - timedelta(hours=1) for t in tt])
    
    data = {
            'time': time,
            'H': H, 'He': He, 'N2': N2, 'CH4': CH4,
            'H2O': H2O, 'CO': CO, 'O2': O2, 'CO2': CO2
        }

    for k, v in data.items():
        if k != 'time':
            print(k)
            data[k] = v.astype(float)
    df = pd.DataFrame(data)
    return df


def _():
    df_ms = ms()
    dat_base = Path(__file__).parent / "../0d/"
    res_glob = f"{Path(__file__).parent}/../0d/res_delta4/*res"
    par_file = Path(__file__).parent / "parameters.wAl2O3d4.txt"
    T_file = Path(__file__).parent / ".." / "0d" / "TC_UC1.csv"
    t_files = glob(f"{dat_base}/h5/*.h5")


    get_time_h5(t_files[0])
    df = get_combined_df(t_files, res_glob, par_file, T_file)

    add_ms(df, df_ms)







    fig, ax = create_basic_plot("t / h", "T_avg / °C")

    ax.plot(df.dt, df["T_avg / °C"], label="T_avg / °C")
    axr = ax.twinx()
    color_cycle = axr._get_lines.prop_cycler
    axr.set_ylabel("$p^{\prime}$H / ")
    
    C = next(color_cycle)
    c = next(color_cycle)

    axr.plot(df.dt, df.H, label="H", color=c['color'])
    ax.legend()
    print(df)
    df.to_csv("FelixStinkt.csv")
    plt.show()




if __name__ == "__main__":
    main()
