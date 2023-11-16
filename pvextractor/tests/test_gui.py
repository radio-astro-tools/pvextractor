from packaging.version import Version

import pytest
import numpy as np
import matplotlib
from matplotlib.backend_bases import KeyEvent, MouseEvent

from ..gui import PVSlicer

from .test_slicer import make_test_hdu, make_test_fits_file

MATPLOTLIB_GE_36 = Version(matplotlib.__version__) >= Version('3.6')

def key_press_event(canvas, *event):
    if MATPLOTLIB_GE_36:
        canvas.callbacks.process('key_press_event',
                                  KeyEvent('key_press_event', canvas, *event))
    else:
        canvas.key_press_event(*event)


def button_press_event(canvas, *event):
    if MATPLOTLIB_GE_36:
        canvas.callbacks.process('button_press_event',
                                  MouseEvent('button_press_event', canvas, *event))
    else:
        canvas.button_press_event(*event)


def motion_notify_event(canvas, *event):
    if MATPLOTLIB_GE_36:
        canvas.callbacks.process('motion_notify_event',
                                  MouseEvent('motion_notify_event', canvas, *event))
    else:
        canvas.motion_notify_event(*event)


def test_gui():

    pytest.importorskip('PyQt6')

    hdu = make_test_hdu()

    pv = PVSlicer(hdu, clim=(-0.02, 2), backend='QtAgg')
    pv.show(block=False)

    xy_data = np.array([[0.0, 0.1, 0.5, 1.0, 0.5],
                        [0.0, 0.3, 0.4, 0.9, 1.4]]).T

    x, y = pv.ax1.transData.transform(xy_data).T

    for i in range(len(x)):
        motion_notify_event(pv.fig.canvas, x[i], y[i])
        button_press_event(pv.fig.canvas, x[i], y[i], 1)

    key_press_event(pv.fig.canvas, 'enter')
    motion_notify_event(pv.fig.canvas, x[-1] - 20, y[-1])
    button_press_event(pv.fig.canvas, x[-1] - 20, y[-1], 1)

    pv.fig.canvas.draw()

    assert pv.pv_slice.data.shape == (5, 2)

    pv.close()


def test_gui_from_fits_filename(tmp_path):

    pytest.importorskip('PyQt6')

    fits_filename = make_test_fits_file(tmp_path)

    pv = PVSlicer(fits_filename, clim=(-0.02, 2), backend='QtAgg')
    pv.show(block=False)

    pv.close()
