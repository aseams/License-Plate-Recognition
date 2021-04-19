.. L.O.S.E.R.S documentation master file, created by
   Andrew Seamon on Sun Apr 18 16:12:48 2021.

L.O.S.E.R.S documentation!
++++++++++++++++++++++++++

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

classifications.txt
-------------------
Contains classifications for character recognition training

constants.py
------------
.. dropdown:: Colors

	.. autodata:: constants.SCALAR_BLACK
	.. autodata:: constants.SCALAR_WHITE
	.. autodata:: constants.SCALAR_YELLOW
	.. autodata:: constants.SCALAR_GREEN
	.. autodata:: constants.SCALAR_RED

.. dropdown:: Preprocessing

	.. autodata:: constants.GAUSSIAN_SMOOTH_FILTER_SIZE
	.. autodata:: constants.ADAPTIVE_THRESH_BLOCK_SIZE
	.. autodata:: constants.ADAPTIVE_THRESH_WEIGHT

.. dropdown:: License Plates

	.. autodata:: constants.PLATE_WIDTH_PADDING_FACTOR
	.. autodata:: constants.PLATE_HEIGHT_PADDING_FACTOR

.. dropdown:: Possible Characters

	.. autodata:: constants.MIN_PIXEL_WIDTH
	.. autodata:: constants.MIN_PIXEL_HEIGHT
	.. autodata:: constants.MIN_ASPECT_RATIO
	.. autodata:: constants.MAX_ASPECT_RATIO
	.. autodata:: constants.MIN_PIXEL_AREA

.. dropdown:: Comparing Characters

	.. autodata:: constants.MIN_DIAG_SIZE_MULTIPLE_AWAY
	.. autodata:: constants.MAX_DIAG_SIZE_MULTIPLE_AWAY
	.. autodata:: constants.MAX_CHANGE_IN_AREA
	.. autodata:: constants.MAX_CHANGE_IN_WIDTH
	.. autodata:: constants.MAX_CHANGE_IN_HEIGHT
	.. autodata:: constants.MAX_ANGLE_BETWEEN_CHARS

.. dropdown:: Other

	.. autodata:: constants.MIN_NUMBER_OF_MATCHING_CHARS
	.. autodata:: constants.RESIZED_CHAR_IMAGE_WIDTH
	.. autodata:: constants.RESIZED_CHAR_IMAGE_HEIGHT
	.. autodata:: constants.MIN_CONTOUR_AREA
	.. autodata:: constants.typeface
	.. autodata:: constants.state_names
	.. autodata:: constants.API_KEY


database.py
-----------
.. automodule:: database
   :members:

dbConn.py
---------
.. automodule:: dbConn
   :members:

doubleCheck.py
--------------
.. automodule:: doubleCheck
   :members:

FindChars.py
------------
.. automodule:: FindChars
   :members:

FindPlates.py
-------------
.. automodule:: FindPlates
   :members:

flattened_images.txt
--------------------
Training data for personal OCR

LPR_Final.py
------------
.. automodule:: LPR_Final
   :members:

PossibleChar.py
---------------
.. autoclass:: PossibleChar.PossibleChar
   :members:

PossiblePlate.py
----------------
.. autoclass:: PossiblePlate.PossiblePlate
   :members:

preprocess.py
-------------
.. automodule:: preprocess
   :members: