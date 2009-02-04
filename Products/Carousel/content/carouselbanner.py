"""Definition of the Carousel Banner content type
"""

from zope.interface import implements

try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    from Products.Archetypes import atapi
from Products.ATContentTypes.content import link
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.configuration import zconf
from Products.validation import V_REQUIRED

from Products.Carousel import CarouselMessageFactory as _
from Products.Carousel.interfaces import ICarouselBanner
from Products.Carousel.config import PROJECTNAME

CarouselBannerSchema = link.ATLinkSchema.copy() + atapi.Schema((

    atapi.ImageField('image',
        required = False,
        storage = atapi.AnnotationStorage(),
        languageIndependent = True,
        max_size = zconf.ATNewsItem.max_image_dimension,
        sizes= { },
        validators = (('isNonEmptyFile', V_REQUIRED),
                      ('checkNewsImageMaxSize', V_REQUIRED)),
        widget = atapi.ImageWidget(
            description = _(u'This image will be shown when this banner is active.'),
            label= _(u'Image'),
            show_content_type = False)
        ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

CarouselBannerSchema['title'].storage = atapi.AnnotationStorage()
CarouselBannerSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(CarouselBannerSchema, moveDiscussion=False)

class CarouselBanner(link.ATLink):
    """A carousel banner which may include an image, text, and/or link."""
    implements(ICarouselBanner)

    meta_type = portal_type = "Carousel Banner"
    schema = CarouselBannerSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image
    
        return super(CarouselBanner, self).__bobo_traverse__(REQUEST, name)
    

atapi.registerType(CarouselBanner, PROJECTNAME)