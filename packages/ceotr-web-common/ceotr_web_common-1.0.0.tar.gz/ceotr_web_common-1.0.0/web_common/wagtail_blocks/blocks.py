"""
Custom StreamField blocks to be used in Wagtail CMS setups
"""

from rest_framework.fields import Field

from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class BaseStyleStructValue(blocks.StructValue):
    """
    Add a base CSS class for the custom blocks defined here

    NOTE: This doesn't seem to work with the API, so not being used in the template at the moment.
    Hoping to revisit sometime.
    """
    @property
    def base_class(self):
        block_type = self.get('type')
        if block_type == 'rich_text' or block_type == 'richtext':
            return 'richtext'
        elif block_type == 'image':
            return 'image-block'
        elif block_type == 'image_set':
            return 'image-box'
        elif block_type == 'figure':
            return 'figure-block'
        elif block_type == 'multifigure':
            return 'multifigure'
        elif block_type == 'buttons':
            return 'button-set'
        elif block_type == 'video':
            return 'video-embed'
        elif block_type == 'block_quote':
            return 'block-quote'
        elif block_type == 'code':
            return 'code-block'
        else:
            return None


class StyledRichTextBlock(blocks.StructBlock):
    text = blocks.RichTextBlock(required=True)
    class_names = blocks.CharBlock(required=False, max_length=255, help_text="One or more CSS class names to apply to bounding element, separated by spaces")

    class Meta:
        icon = 'doc-full'
        label = 'Rich Text'
        value_class = BaseStyleStructValue


class ImageSerializedField(Field):
    """A custom serializer to be used in Wagtail's v2 API."""

    def to_representation(self, value):
        """Return the image URL, title and dimensions."""
        return {
            "url": value.file.url,
            "title": value.title,
            "width": value.width,
            "height": value.height,
        }


class APIImageChooserBlock(ImageChooserBlock):
    """Use custom serializer to get image info from API"""
    def get_api_representation(self, value, context=None):
        return ImageSerializedField().to_representation(value)


class ImageBlock(blocks.StructBlock):
    """A single image"""

    image = APIImageChooserBlock(required=True)
    alt_text = blocks.TextBlock(required=False)
    class_names = blocks.CharBlock(required=False, max_length=255, help_text="One or more CSS class names to apply to bounding element, separated by spaces")

    class Meta:
        icon = "image"
        label = "Image"
        value_class = BaseStyleStructValue


class ImageSetBlock(blocks.StructBlock):
    """A set of images to be displayed together"""

    images = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", APIImageChooserBlock(required=True)),
                ("alt_text", blocks.TextBlock(required=False)),
            ]
        )
    )
    class_names = blocks.CharBlock(required=False, max_length=255, help_text="One or more CSS class names to apply to bounding element, separated by spaces")

    class Meta:
        icon = "image"
        label = "Image Set"
        value_class = BaseStyleStructValue


class MultiFigureBlock(blocks.StructBlock):
    """One or more images to be displayed together with a single optional caption"""
    images = blocks.ListBlock(
        blocks.StructBlock([
            ("image", APIImageChooserBlock(required=True)),
            ("alt_text", blocks.TextBlock(required=False)),
        ])
    )
    caption = blocks.RichTextBlock(required=False, features=['bold', 'italic', 'link', 'document-link'])
    class_names = blocks.CharBlock(required=False, max_length=255, help_text="One or more CSS class names to apply to bounding element, separated by spaces")

    class Meta:
        icon = "folder-open-1"
        label = "Multi-Image Figure"
        value_class = BaseStyleStructValue


class FigureCaptionBlock(blocks.StructBlock):
    """Show an image with a caption"""
    figure = APIImageChooserBlock(required=True)
    alt_text = blocks.TextBlock(required=False)
    caption = blocks.RichTextBlock(required=False, features=['bold', 'italic', 'link', 'document-link'])
    class_names = blocks.CharBlock(required=False, max_length=255, help_text="One or more CSS class names to apply to bounding element, separated by spaces")

    class Meta:
        icon = "image"
        label = "Figure"
        value_class = BaseStyleStructValue


class ButtonBlock(blocks.StructBlock):
    """One or more buttons which link to another page or an external URL"""
    buttons = blocks.ListBlock(
        blocks.StructBlock([
            ("button_text", blocks.CharBlock(required=True)),
            ("button_page", blocks.PageChooserBlock(required=False)),
            ("button_url", blocks.URLBlock(required=False)),
        ])
    )
    class_names = blocks.CharBlock(required=False, max_length=255, help_text="One or more CSS class names to apply to bounding element, separated by spaces")

    class Meta:
        icon = "link"
        label = "Buttons"
        value_class = BaseStyleStructValue


CODE_CHOICES = [
    ('python', 'Python'),
    ('matlab', 'MATLAB'),
    ('cpp', 'C++'),
    ('c', 'C'),
    ('javascript', 'JavaScript'),
    ('fortran', 'Fortran'),
    ('css', 'CSS'),
    ('markup', 'Markup'),
]


class CodeBlock(blocks.StructBlock):
    """Block for displaying code with appropriate syntax highlighting (when used with PrismJS, for example)"""
    language = blocks.ChoiceBlock(choices=CODE_CHOICES, default='python')
    text = blocks.TextBlock(required=True)
    class_names = blocks.CharBlock(required=False, max_length=255, help_text="One or more CSS class names to apply to bounding element, separated by spaces")

    class Meta:
        icon = "code"
        label = "Code"
        value_class = BaseStyleStructValue


class VideoEmbedBlock(blocks.StructBlock):
    """Block for embedding a video from a URL (e.g. YouTube)"""
    video = EmbedBlock(required=True, help_text="If embedding a YouTube video, be sure to use the 'embed' version of the link (generally defaults to 'watch').")
    class_names = blocks.CharBlock(required=False, max_length=255, help_text="One or more CSS class names to apply to bounding element, separated by spaces")

    class Meta:
        icon = "media"
        label = "Video Embed"
        value_class = BaseStyleStructValue


class BlockQuoteBlock(blocks.StructBlock):
    """Block to enter text to be inserted in an HTML <blockquote> tag"""
    text = blocks.RichTextBlock(required=True)
    class_names = blocks.CharBlock(required=False, max_length=255, help_text="One or more CSS class names to apply to bounding element, separated by spaces")

    class Meta:
        icon = "openquote"
        label = "Block Quote"
        value_class = BaseStyleStructValue


class StandardStream(blocks.StreamBlock):
    """To be used in StreamField definition instead of having to list all available blocks (for convenience)"""
    rich_text = StyledRichTextBlock()
    image = ImageBlock()
    image_set = ImageSetBlock()
    figure = FigureCaptionBlock()
    multifigure = MultiFigureBlock()
    buttons = ButtonBlock()
    video = VideoEmbedBlock()
    block_quote = BlockQuoteBlock()
    code = CodeBlock()
    
    class Meta:
        icon = 'cogs'


