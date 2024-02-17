from abc import ABC, abstractmethod
from typing import Tuple, Union


class MapsDownloader(ABC):
	MAX_LATITUDE = 85.0511287798
	MAX_LONGITUDE = 180.0

	"""An abstract class for downloading map sections from various map providers."""
	@abstractmethod
	def __call__(
			self,
			north_latitude: float,
			west_longitude: float,
			south_latitude: float,
			east_longitude: float,
			zoom: int,
			style: str,
			image_format: str = "RGB",
			resize: Union[None, Tuple[int, int], int] = None,
			return_type: str = Union["PIL", "numpy", "bytes"],
	):
		"""
		Download a map section given geographical coordinates, zoom level, and style.

		:param north_latitude: Northern latitude of the map section.
		:param west_longitude: Western longitude of the map section.
		:param south_latitude: Southern latitude of the map section.
		:param east_longitude: Eastern longitude of the map section.
		:param zoom: Zoom level.
		:param style: Map style.
		:param image_format: Image format. Supported formats are "RGB" and "RGBA".
		:param resize: New size of the map section as a tuple (width, height) or
		an integer for the desired width (in this case, the original aspect ratio is maintained). If None, the
		original size is used.
		:param return_type: The type of the returned object. Supported types are "PIL", "numpy", and "bytes".
		:return: The combined map section. It can be a PIL Image object, a NumPy array, or a byte object, depending
		on the return_type parameter.
		"""
		self.validate_latitude(north_latitude)
		self.validate_latitude(south_latitude)
		self.validate_longitude(west_longitude)
		self.validate_longitude(east_longitude)

	def validate_latitude(self, latitude: float):
		assert abs(latitude) <= self.MAX_LATITUDE, \
			f"Latitude must be between -{self.MAX_LATITUDE} and {self.MAX_LATITUDE} degrees."

	def validate_longitude(self, longitude: float):
		assert abs(longitude) <= self.MAX_LONGITUDE, \
			f"Longitude must be between -{self.MAX_LONGITUDE} and {self.MAX_LONGITUDE} degrees."
