"""Foster thermal model and curve fitting"""

import csv

import numpy as np
import sympy as sp
from scipy.optimize import curve_fit


class Foster:
    """foster thermal impedance model RC network class"""

    def __init__(self) -> None:
        self.foster_func_dict = {
            3: self.foster_zth_3,
            4: self.foster_zth_4,
            5: self.foster_zth_5,
        }

    @staticmethod
    def get_rational_coeffs(expr):
        """Returns coefficients of rational expression"""
        num, den = expr.as_numer_denom()
        return sp.Poly(num).all_coeffs(), sp.Poly(den).all_coeffs()

    @staticmethod
    def foster_zth_3(t, r1, r2, r3, c1, c2, c3):
        """Foster ladder time domain equation for curve fit"""
        return (
            r1 * (1 - np.exp(-t / (r1 * c1)))
            + r2 * (1 - np.exp(-t / (r2 * c2)))
            + r3 * (1 - np.exp(-t / (r3 * c3)))
        )

    @staticmethod
    def foster_zth_4(t, r1, r2, r3, r4, c1, c2, c3, c4):
        """Foster ladder time domain equation for curve fit"""
        return (
            r1 * (1 - np.exp(-t / (r1 * c1)))
            + r2 * (1 - np.exp(-t / (r2 * c2)))
            + r3 * (1 - np.exp(-t / (r3 * c3)))
            + r4 * (1 - np.exp(-t / (r4 * c4)))
        )

    @staticmethod
    def foster_zth_5(t, r1, r2, r3, r4, r5, c1, c2, c3, c4, c5):
        """Foster ladder time domain equation for curve fit"""
        return (
            r1 * (1 - np.exp(-t / (r1 * c1)))
            + r2 * (1 - np.exp(-t / (r2 * c2)))
            + r3 * (1 - np.exp(-t / (r3 * c3)))
            + r4 * (1 - np.exp(-t / (r4 * c4)))
            + r5 * (1 - np.exp(-t / (r5 * c5)))
        )

    def foster_fit(self, csv_path, bounds, norder=4, header=False):
        """Return foster RC values from curve fit. CSV column order must be time, zth.
        rc_vals = R1, R2, ..., R{n-1}, Rn, C1, C2, ..., C{n-1}, Cn
        """
        self._check_order(norder)
        time = []
        zth = []
        with open(csv_path, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            if header:
                next(reader, None)  # discard first row
            for row in reader:
                time.append(float(row[0]))
                zth.append(float(row[1]))
        rc_vals, _ = curve_fit(self.foster_func_dict[norder], time, zth, bounds=bounds)
        return rc_vals

    def foster_zth_n(self, norder, t_list, rc_list):
        """gets foster_zth_n callable and passes args to it"""
        self._check_order(norder)
        return [self.foster_func_dict[norder](time, *rc_list) for time in t_list]

    def _check_order(self, norder):
        """check if order is within bounds and raise exception"""
        nmin = 3
        nmax = 5
        if norder < nmin or norder > nmax:
            raise ValueError(f"norder: {norder} is invalid.  Min: {nmin}, Max: {nmax}")

    def foster_zth_fs(self, rc_vals, norder):
        """build Zth(s) symbolic function
        Zth(s) = R1/(1+s*R1*C1) + R2/(1+s*R2*C2) + ... + Rn/(1+s*Rn*Cn)
        """
        self._check_order(norder)
        s = sp.symbols("s")
        zth_s = 0
        for idx in range(norder):
            rn = rc_vals[idx]
            cn = rc_vals[idx + norder]  # based on the order of foster_fit return tuple
            zth_s = sp.Add(zth_s, rn / (1 + s * rn * cn))
        return zth_s
