"""Utility functions

all assume radians"""

from __future__ import annotations

from .mathfun import atan2, cos, hypot, sin

__all__ = ["cart2pol", "pol2cart", "cart2sph", "sph2cart"]


def cart2pol(x, y) -> tuple:
    """Transform Cartesian to polar coordinates"""
    return atan2(y, x), hypot(x, y)


def pol2cart(theta, rho) -> tuple:
    """Transform polar to Cartesian coordinates"""
    return rho * cos(theta), rho * sin(theta)


def cart2sph(x, y, z) -> tuple:
    """Transform Cartesian to spherical coordinates"""
    hxy = hypot(x, y)
    r = hypot(hxy, z)
    el = atan2(z, hxy)
    az = atan2(y, x)
    return az, el, r


def sph2cart(az, el, r) -> tuple:
    """Transform spherical to Cartesian coordinates"""
    rcos_theta = r * cos(el)
    x = rcos_theta * cos(az)
    y = rcos_theta * sin(az)
    z = r * sin(el)
    return x, y, z
