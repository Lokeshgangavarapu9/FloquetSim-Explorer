"""
FloquetSim Explorer - Exploratory Spectral Analysis & Error Mitigation
Specification: Master Engineering Specification v1.2, Subphase 8.7
Non-blocking optional modules: Discrete Fourier Power Spectrum and Richardson Zero-Noise Extrapolation (ZNE).
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np


def compute_fourier_spectrum(
    time_series: List[float],
    dt: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute standard discrete Fourier power spectral density:
    S(f) = (1 / N) * |FFT(x)|^2
    Returns: (positive_frequencies, power_spectrum)
    """
    n = len(time_series)
    if n == 0:
        return np.array([]), np.array([])

    # Discrete Fourier Transform
    fft_vals = np.fft.fft(time_series)
    freqs = np.fft.fftfreq(n, d=dt)

    # Power spectral density
    power = (np.abs(fft_vals) ** 2) / n

    # Filter to positive half-spectrum
    pos_mask = freqs >= 0
    return freqs[pos_mask], power[pos_mask]


def richardson_extrapolate(
    scale_factors: List[float],
    expectation_values: List[float],
) -> float:
    """
    Polynomial / Richardson extrapolation to zero noise limit (scale factor -> 0).
    Fits a polynomial of degree len(scale_factors) - 1 and evaluates at scale = 0.
    """
    if len(scale_factors) != len(expectation_values):
        raise ValueError("scale_factors and expectation_values must have identical length.")
    if len(scale_factors) < 2:
        return expectation_values[0] if expectation_values else 0.0

    # Polynomial fit: y = poly(x)
    degree = min(2, len(scale_factors) - 1)
    coeffs = np.polyfit(scale_factors, expectation_values, deg=degree)
    # Evaluate at x = 0 (constant term in poly1d)
    poly = np.poly1d(coeffs)
    return float(poly(0.0))
