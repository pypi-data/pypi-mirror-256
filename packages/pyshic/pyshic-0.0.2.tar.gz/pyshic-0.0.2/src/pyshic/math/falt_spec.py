import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline, PPoly
from scipy.signal import convolve

def falt_eqi(ex_wl, ex_I, wl, P):
    """
    Convolve the spectrum (ex_wl, ex_I) with the slit function described by spline P
    onto the wavelengths wl.
    
    P must be calculated with scipy's PPoly (equivalent to MATLAB's csapi).
    
    ex_wl and wl must be equidistant and the step size of wl must be a multiple of
    the step size of ex_wl.
    """
    # Extracting spline properties
    breaks = P.x
    spmin = np.min(breaks)
    spmax = np.max(breaks)
    
    # Check for equidistant wavelength vectors
    d1 = np.diff(ex_wl)
    d2 = np.diff(wl)
    if not np.allclose(d1, d1[0], atol=1e-6) or not np.allclose(d2, d2[0], atol=1e-6):
        raise ValueError('Wavelength vectors are not equidistant.')
    
    # Check step size requirement
    md1 = d1[0]  # Assuming equidistant, so taking the first element
    per = d2[0] / md1
    if not np.isclose(per, round(per), atol=1e-6):
        raise ValueError('Step size of wl must be a multiple of the step size of ex_wl.')
    per = int(round(per))
    
    h = (wl[0] - ex_wl[0]) / md1
    delta = (h - np.floor(h)) * md1
    anf_index = 1 + np.floor(h)
    anf_spalt = np.floor((spmin + delta) / md1) - 1
    end_spalt = np.ceil((spmax + delta) / md1) + 1
    spalt_wl = np.arange(end_spalt, anf_spalt - 1, -1) * md1 - delta
    
    # Evaluate spline
    spalt = P(spalt_wl) * (spalt_wl >= spmin) & (spalt_wl <= spmax)
    spalt = spalt / np.sum(spalt)
    
    # Perform convolution and select indices based on per and anf_index
    h = convolve(ex_I, spalt, mode='full')
    ind = np.arange(0, len(wl)) * per + anf_index
    I = h[ind.astype(int)]
    
    return I


def falt_spec(specwl, spec, wlout, P):
    """
    Convolves spec with P on wlout.
    specwl: wavelengths corresponding to spec
    spec: spectrum to be convolved
    wlout: output wavelengths
    P: convolution kernel
    """
    d1 = np.diff(specwl)
    d2 = np.diff(wlout)
    md1 = np.min(d1)
    md2 = np.min(d2)
    per = md2 / md1

    # Check if wavelength grids are equidistant and period is an integer
    eqi = np.allclose(np.max(d1) - np.min(d1), 0, atol=1e-6) and \
          np.allclose(np.max(d2) - np.min(d2), 0, atol=1e-6) and \
          np.allclose(per, np.round(per), atol=1e-6)

    # Filter out NaN values from spec
    ind = ~np.isnan(spec)
    
    # Assuming falt_eqi is a placeholder for actual convolution, 
    # replaced with generic convolution logic
    if eqi:
        # Equidistant grid - direct convolution (simplified example)
        convolved = np.convolve(spec[ind], P, mode='same')
        I = np.interp(wlout, specwl[ind], convolved)
    else:
        # Non-equidistant grid - convolve then interpolate
        # First, convolve on the valid part of the spectrum
        etc_temp = np.convolve(spec[ind], P, mode='same')
        
        # Then, use spline interpolation for non-equidistant output grid
        spline = InterpolatedUnivariateSpline(specwl[ind], etc_temp)
        I = spline(wlout)

    return I
