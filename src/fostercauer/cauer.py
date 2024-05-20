"""Cauer RC thermal model class"""

from .foster import Foster
from .foster2cauer import foster2cauer


class Cauer(Foster):
    """Cauer RC thermal model class"""

    def get_cauer_rcs(self, csv_file, norder, rmax, cmax):
        """generate cauer RC values"""
        fstr_rc_vals = self.foster_fit(
            csv_file, (0, [rmax] * norder + [cmax] * norder), norder
        )
        fstr_zin_s = self.foster_zth_fs(fstr_rc_vals, norder)
        fstr_coeffs = self.get_rational_coeffs(fstr_zin_s)
        return foster2cauer(fstr_coeffs)
