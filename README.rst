Position-Velocity Diagram Extractor
===================================

Tool to slice through data cubes and extract position-velocity (or other)
slices.

There are a few `utilities <pvextractor/utils>`_ related to header trimming &
parsing.  Otherwise, there's one main function,
`pvdiagram <pvextractor/pvextractor.py>`_, that takes a data cube and a series of
points and returns a PV array.  It is based on scipy's map_coordinates.

For an example use case, see `this notebook
<http://nbviewer.ipython.org/urls/raw.github.com/keflavich/pvextractor/master/examples/IRAS05358Slicing.ipynb>`_
(also `here <examples/IRAS05358Slicing.html>`_)




.. image:: https://d2weczhvl823v0.cloudfront.net/keflavich/pvextractor/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

