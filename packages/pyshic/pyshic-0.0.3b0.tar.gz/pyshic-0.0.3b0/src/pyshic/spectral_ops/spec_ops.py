import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline, PPoly,CubicSpline
from scipy.signal import convolve
from typing import Tuple, Union

def conv_eqi_spec_with_slit(input_wavelengths: np.ndarray, 
                            input_intensities: np.ndarray, 
                            output_wavelengths: np.ndarray, 
                            slit_function_spline: PPoly) -> np.ndarray:
    """
    Convolve the input spectrum with the slit function described by a PPoly spline
    onto the specified output wavelengths.
    
    Args:
        input_wavelengths (np.ndarray): Wavelengths of the input spectrum.
        input_intensities (np.ndarray): Intensity values of the input spectrum.
        output_wavelengths (np.ndarray): Output wavelengths for the convolved spectrum.
        slit_function_spline (PPoly): Spline representation of the slit function. 
                                    Use `scipy.interpolate`
    
    Returns:
        Intensity values of the convolved spectrum at output wavelengths in as numpy `ndarray`.
    """
    # Extracting spline properties
    breaks = slit_function_spline.x
    spmin = np.min(breaks)
    spmax = np.max(breaks)
    
    # Check for equidistant wavelength vectors
    d1 = np.diff(input_wavelengths)
    d2 = np.diff(output_wavelengths)
    if not np.allclose(d1, d1[0], atol=1e-6) or not np.allclose(d2, d2[0], atol=1e-6):
        raise ValueError('Wavelength vectors are not equidistant.')
    
    # Check step size requirement
    min_d1 = np.min(d1)
    min_d2 = np.min(d2)
    period = min_d2 / min_d1
    if not np.isclose(period, round(period), atol=1e-6):
        raise ValueError('Step size of output_wavelengths must be a multiple of the step size of input_wavelengths.')
    period = int(round(period))
    
    offset = (output_wavelengths[0] - input_wavelengths[0]) / min_d1
    delta = (offset - np.floor(offset)) * min_d1
    starting_index = 1 + np.floor(offset)
    
    slit_start = np.floor((spmin + delta) / min_d1) - 1
    slit_end = np.ceil((spmax + delta) / min_d1) + 1
    slit_wavelengths = np.arange(slit_end, slit_start - 1, -1) * min_d1 - delta
    
    # Evaluate spline
    slit_values = slit_function_spline(slit_wavelengths) * (slit_wavelengths >= spmin) * (slit_wavelengths <= spmax)
    slit_values = slit_values / np.sum(slit_values)
    
    starting_index += slit_end
    convolved = convolve(input_intensities, slit_values, mode='full')
    indices = np.arange(0, len(output_wavelengths)) * period + starting_index
    convolved_intensities = convolved[indices.astype(int)-1]
    
    return convolved_intensities

def conv_spec_with_slit(spec_wavelengths: np.ndarray, 
                        spec_intensities: np.ndarray, 
                        output_wavelengths: np.ndarray, 
                        slit_spline: PPoly) -> np.ndarray:
    """
    Convolve spectrum with a slit function on specified output wavelengths.
    
    Args:
        spec_wavelengths (np.ndarray): Wavelengths of the input spectrum.
        spec_intensities (np.ndarray): Intensity values of the input spectrum.
        output_wavelengths (np.ndarray): Output wavelengths for the convolved spectrum.
        slit_spline (PPoly): Spline representation of the slit function.
                             Use `scipy.interpolate`
    
    Returns:
    Intensity values of the convolved spectrum at output wavelengths.
    """
    # Check if wavelength vectors are equidistant and meet step size requirements
    diff_spec_wl = np.diff(spec_wavelengths)
    diff_output_wl = np.diff(output_wavelengths)
    min_diff_spec_wl = np.min(diff_spec_wl)
    min_diff_output_wl = np.min(diff_output_wl)
    period = min_diff_output_wl / min_diff_spec_wl

    if (np.max(diff_spec_wl) - np.min(diff_spec_wl) > 1e-6 or
        np.max(diff_output_wl) - np.min(diff_output_wl) > 1e-6 or
        abs(period - round(period)) > 1e-6):
        eqi = False
    else:
        eqi = True

    valid_indices = ~np.isnan(spec_intensities)

    if eqi:
        convolved_intensities = conv_eqi_spec_with_slit(spec_wavelengths, spec_intensities, output_wavelengths, slit_spline)
    else:
        # For non-equidistant grid: convolve then interpolate
        temp_convolution = conv_eqi_spec_with_slit(spec_wavelengths[valid_indices], spec_intensities[valid_indices], spec_wavelengths, slit_spline)
        cs = CubicSpline(spec_wavelengths[valid_indices], temp_convolution)
        convolved_intensities = cs(output_wavelengths)

    return convolved_intensities
