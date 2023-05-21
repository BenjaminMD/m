from pathlib import Path
import numpy as np
import fire


def main(*files, out="diff"):
    if not Path(f"./{out}").exists():
        Path(f"./{out}").mkdir()

    for file in files:
        name = Path(file).stem
        r, gcalc, gr, *_ = np.loadtxt(file).T
        np.savetxt(f"./{out}/{name}", np.c_[r, gcalc-gr])


if __name__ == '__main__':
    fire.Fire(main)
