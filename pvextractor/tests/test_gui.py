import numpy as np
from ..gui import PVSlicer

from .test_slicer import make_test_hdu


def test_gui():

    hdu = make_test_hdu()

    pv = PVSlicer(hdu, clim=(-0.02, 2))
    pv.show(block=False)

    xy_data = np.array([[0.0, 0.1, 0.5, 1.0, 0.5],
                        [0.0, 0.3, 0.4, 0.9, 1.4]]).T

    x, y = pv.ax1.transData.transform(xy_data).T

    for i in range(len(x)):
        pv.fig.canvas.motion_notify_event(x[i], y[i])
        pv.fig.canvas.button_press_event(x[i], y[i], 1)

    pv.fig.canvas.key_press_event('enter')
    pv.fig.canvas.motion_notify_event(x[-1] - 20, y[-1])
    pv.fig.canvas.button_press_event(x[-1] - 20, y[-1], 1)

    pv.fig.canvas.draw()

    assert pv.pv_slice.data.shape == (5, 2)
