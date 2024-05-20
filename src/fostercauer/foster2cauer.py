"""Foster to Cauer network converter"""

import numpy as np


def foster2cauer(
    foster_zin_coeffs: tuple[list[float], list[float]]
) -> dict[str, float]:
    """foster model to cauer model RC value conversion"""
    # Example coeffs data
    # z_den = np.array([0.005506, 1.8785, 7.247, 6.3744, 1])
    # z_num = np.array([0.1236, 3.202, 7.2855, 1.7])

    z_den = np.array(foster_zin_coeffs[1])
    z_num = np.array(foster_zin_coeffs[0])

    # Invert Zin(s): 1/Zin(s) = s*Ci + Yi(s)
    # dividend
    A = z_den
    # divisor
    B = z_num

    cauer_rc_dict: dict[str, float] = {}
    # Polynomial long division
    for idx in range(len(B)):

        # Calculate quotient, which is Cth
        cth_n_raw = A[0] / B[0]
        cth_n = np.abs(cth_n_raw)
        # print(f"Cth_{index + 1} = {cth:.5f} J/K")

        # Calculate numerator of remainder, which is numerator of admittance
        # Denominator is divisor of Zin
        y_num = A[:-1] - B * cth_n
        # Pull down next term of dividend
        y_num = np.append(y_num, A[-1])
        y_den = B

        A = y_den
        B = y_num

        # Calculate quotient of inverse admittance, which is Rth
        # 1/Yi(s) = Ri + Znext
        rth_n_raw = A[0] / B[1]
        rth_n = np.abs(rth_n_raw)
        # print(f"Rth_{index + 1} = {rth:.5f} K/W")

        # New remainder: Znext
        # If numerator of remainder is 0, we are done
        z_num = A - B[1:] * rth_n
        z_den = B

        A = z_den[1:]
        B = z_num[1:]

        cauer_rc_dict[f"C{idx+1}"] = cth_n
        cauer_rc_dict[f"R{idx+1}"] = rth_n
        # print(f".param C{idx+1}={cth:.5f} R{idx+1}={rth:.5f}")

    return cauer_rc_dict
