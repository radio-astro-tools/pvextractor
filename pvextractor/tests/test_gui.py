import numpy as np
from numpy.testing import assert_allclose

from astropy.io import fits

from ..pvextractor import extract_pv_slice
from ..geometry.path import Path
from ..gui import PVSlicer

from .test_slicer import make_test_hdu


def test_gui():
    hdu = make_test_hdu()

    pv = PVSlicer(hdu, clim=(-0.02, 2))
    pv.show(block=False)

    x = [100,200,220,330,340]
    y = [100,200,300,420,430]

    for i in range(len(x)):
        pv.fig.canvas.motion_notify_event(x[i],y[i])
        pv.fig.canvas.button_press_event(x[i],y[i],1)

    pv.fig.canvas.key_press_event('enter')
    pv.fig.canvas.motion_notify_event(310,420)
    pv.fig.canvas.button_press_event(410,420,1)

    pv.fig.canvas.draw()

    assert pv.pv_slice.data.shape == (5,2)
