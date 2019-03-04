import pytest
from distutils.version import LooseVersion
import matplotlib as mpl


from ..gui import PVSlicer

from .test_slicer import make_test_hdu

try:
    import PyQt5
    PYQT5OK = True
except ImportError:
    PYQT5OK = False


if LooseVersion(mpl.__version__) < LooseVersion('2'):
    MPLOK = True
else:
    MPLOK = False


@pytest.mark.skipif('not PYQT5OK or not MPLOK')
def test_gui():
    hdu = make_test_hdu()

    pv = PVSlicer(hdu, clim=(-0.02, 2))
    pv.show(block=False)

    x = [100, 200, 220, 330, 340]
    y = [100, 200, 300, 420, 430]

    for i in range(len(x)):
        pv.fig.canvas.motion_notify_event(x[i], y[i])
        pv.fig.canvas.button_press_event(x[i], y[i], 1)

    pv.fig.canvas.key_press_event('enter')
    pv.fig.canvas.motion_notify_event(310, 420)
    pv.fig.canvas.button_press_event(410, 420, 1)

    pv.fig.canvas.draw()

    assert pv.pv_slice.data.shape == (5, 2)
