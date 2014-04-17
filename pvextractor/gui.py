import math
import warnings

import numpy as np

from matplotlib.collections import LineCollection


def distance(x1, y1, x2, y2, x3, y3):
    """
    Find the shortest distance between a point (x3, y3) and the line passing
    through the points (x1, y1) and (x2, y2).
    """

    px = x2-x1
    py = y2-y1

    something = px * px + py * py

    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(something)

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    dist = math.sqrt(dx*dx + dy*dy)

    return dist


class MovableSliceBox(object):

    def __init__(self, box, callback):
        self.box = box
        self.press = None
        self.background = None
        self.point_counter = 0
        self.callback = callback

    def connect(self):
        self.cidpress = self.box.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidmotion = self.box.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):

        if event.inaxes != self.box.axes:
            return

        self.press = event.xdata, event.ydata

        self.point_counter += 1

        axes = self.box.axes
        canvas = self.box.figure.canvas

        if self.point_counter == 1:  # first point

            self.box.x0 = event.xdata
            self.box.y0 = event.ydata
            self.box.x1 = event.xdata
            self.box.y1 = event.ydata

            self.box.width = 0.

            self.box.set_animated(True)
            canvas.draw()
            self.background = canvas.copy_from_bbox(self.box.axes.bbox)

        self.box._update_segments()

        # now redraw just the lineangle
        axes.draw_artist(self.box)

        if self.point_counter == 3:
            self.point_counter = 0
            self.callback(self.box)
        else:
            canvas.blit(axes.bbox)

    def on_motion(self, event):

        if self.point_counter == 0:
            return

        if event.inaxes != self.box.axes:
            return

        if self.point_counter == 1:
            self.box.x1 = event.xdata
            self.box.y1 = event.ydata
        elif self.point_counter == 2:
            self.box.width = distance(self.box.x0, self.box.y0, self.box.x1, self.box.y1, event.xdata, event.ydata) * 2
        elif self.point_counter == 3:
            return

        canvas = self.box.figure.canvas
        axes = self.box.axes
        canvas.restore_region(self.background)

        self.box._update_segments()

        # redraw just the current lineangle
        axes.draw_artist(self.box)

        # blit just the redrawn area
        canvas.blit(axes.bbox)

    def disconnect(self):
        self.box.figure.canvas.mpl_disconnect(self.cidpress)
        self.box.figure.canvas.mpl_disconnect(self.cidmotion)


class SliceBox(LineCollection):

    def __init__(self, x0=None, y0=None, x1=None, y1=None, width=None, **kwargs):

        super(SliceBox, self).__init__([], **kwargs)

        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.width = width

        self._update_segments()

    def _update_segments(self):

        if self.x0 is None:
            return

        # Find angle of normal to line
        theta = np.arctan2(self.y1 - self.y0, self.x1 - self.x0) + np.pi / 2.

        # Find displacement vectors
        dx = np.cos(theta) * self.width / 2.
        dy = np.sin(theta) * self.width / 2.

        # Find central line
        line = [(self.x0, self.y0), (self.x1, self.y1)]

        # Find bounding rectangle
        rect = [(self.x0 + dx, self.y0 + dy), (self.x0 - dx, self.y0 - dy),
                (self.x1 - dx, self.y1 - dy), (self.x1 + dx, self.y1 + dy),
                (self.x0 + dx, self.y0 + dy)]

        self.set_segments((line, rect))
        self.set_linestyles(('solid', 'dashed'))
        self.set_linewidths((2, 1))


class PVSlicer(object):

    def __init__(self, filename, backend="Qt4Agg"):

        try:
            from spectral_cube import read
            cube = read(filename, format='fits')
            self.array = cube.get_filled_data()
        except:
            warnings.warn("spectral_cube package is not available - using astropy.io.fits directly")
            from astropy.io import fits
            self.array = fits.getdata(filename)
            if self.array.ndim != 3:
                raise ValueError("dataset does not have 3 dimensions (install the spectral_cube package to avoid this error)")

        import matplotlib as mpl
        mpl.use(backend)
        import matplotlib.pyplot as plt

        self.fig = plt.figure(figsize=(14, 8))

        self.ax1 = self.fig.add_axes([0.1, 0.1, 0.4, 0.7])

        self._clim = (np.min(self.array[~np.isnan(self.array) & ~np.isinf(self.array)]),
                      np.max(self.array[~np.isnan(self.array) & ~np.isinf(self.array)]))

        self.slice = int(round(self.array.shape[0] / 2.))

        from matplotlib.widgets import Slider

        self.slice_slider_ax = self.fig.add_axes([0.1, 0.95, 0.4, 0.03])
        self.slice_slider_ax.set_xticklabels("")
        self.slice_slider_ax.set_yticklabels("")
        self.slice_slider = Slider(self.slice_slider_ax, "3-d slice", 0, self.array.shape[0], valinit=self.slice, valfmt="%i")
        self.slice_slider.on_changed(self.update_slice)
        self.slice_slider.drawon = False

        self.image = self.ax1.imshow(self.array[self.slice, :,:], origin='lower', interpolation='nearest', vmin=self._clim[0], vmax=self._clim[1], cmap=plt.cm.gray)

        self.vmin_slider_ax = self.fig.add_axes([0.1, 0.90, 0.4, 0.03])
        self.vmin_slider_ax.set_xticklabels("")
        self.vmin_slider_ax.set_yticklabels("")
        self.vmin_slider = Slider(self.vmin_slider_ax, "vmin", self._clim[0], self._clim[1], valinit=self._clim[0])
        self.vmin_slider.on_changed(self.update_vmin)
        self.vmin_slider.drawon = False

        self.vmax_slider_ax = self.fig.add_axes([0.1, 0.85, 0.4, 0.03])
        self.vmax_slider_ax.set_xticklabels("")
        self.vmax_slider_ax.set_yticklabels("")
        self.vmax_slider = Slider(self.vmax_slider_ax, "vmax", self._clim[0], self._clim[1], valinit=self._clim[1])
        self.vmax_slider.on_changed(self.update_vmax)
        self.vmax_slider.drawon = False

        self.grid1 = None
        self.grid2 = None
        self.grid3 = None

        self.ax2 = self.fig.add_axes([0.55, 0.1, 0.4, 0.7])

        # Add slicing box
        self.box = SliceBox(colors=(0.8, 0.0, 0.0))
        self.ax1.add_collection(self.box)
        self.movable = MovableSliceBox(self.box, callback=self.update_pv_slice)
        self.movable.connect()

        # Add save button
        from matplotlib.widgets import Button
        self.save_button_ax = self.fig.add_axes([0.65, 0.90, 0.20, 0.05])
        self.save_button = Button(self.save_button_ax, 'Save slice to FITS')
        self.save_button.on_clicked(self.save_fits)

        self.pv_slice = None

    def save_fits(self, *args, **kwargs):
        if self.pv_slice is None:
            return
        from astropy.io import fits
        # TODO: customize slice name
        fits.writeto('slice.fits', self.pv_slice, clobber=True)

    def update_pv_slice(self, box):

        from .geometry.path import Path
        from . import extract_pv_slice

        path = Path([(box.x0, box.y0), (box.x1, box.y1)])
        self.pv_slice = extract_pv_slice(self.array, path)

        self.ax2.imshow(self.pv_slice, origin='lower', aspect='auto')

        self.fig.canvas.draw()
        self.ax1.draw_artist(self.box)

    def show(self):
        import matplotlib.pyplot as plt
        plt.show()

    def update_slice(self, pos=None):

        if self.array.ndim == 2:
            self.image.set_array(self.array)
        else:
            self.slice = int(round(pos))
            self.image.set_array(self.array[self.slice, :, :])

        self.fig.canvas.draw()

    def update_vmin(self, vmin):
        if vmin > self._clim[1]:
            self._clim = (self._clim[1], self._clim[1])
        else:
            self._clim = (vmin, self._clim[1])
        self.image.set_clim(*self._clim)
        self.fig.canvas.draw()

    def update_vmax(self, vmax):
        if vmax < self._clim[0]:
            self._clim = (self._clim[0], self._clim[0])
        else:
            self._clim = (self._clim[0], vmax)
        self.image.set_clim(*self._clim)
        self.fig.canvas.draw()
