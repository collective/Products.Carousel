from zope.interface import Interface

from Products.Carousel import CarouselMessageFactory as _

class ICarouselFolder(Interface):
    """Marker for a folder that can hold Carousel banners."""
    
class ICarouselBanner(Interface):
    """A carousel banner which may include an image, text, and/or link."""

class ICarouselBrowserLayer(Interface):
    """Marker applied to the request during traversal of sites that
       have Carousel installed
    """