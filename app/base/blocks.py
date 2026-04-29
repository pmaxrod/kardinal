from django.utils.translation import gettext as _
from wagtail.images.blocks import ImageBlock

from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock


class CustomImageBlock(StructBlock):
    """Bloque de imagen personalizado.

    Attributes:
        image: Imagen
    """

    image = ImageBlock(required=True, label=_("Imagen"), help_text=_("Imagen del bloque"))

    class Meta:
        template = "base/blocks/custom_image_block.html"
        label = _("Imagen")
        help_text = _("Imagen a insertar")
        icon = "image"


class HeadingBlock(StructBlock):
    """Encabezados de distintos tamaños.

    Attributes:
        heading_text: Texto de encabezado
        size: Tamaño del encabezado
    """

    heading_text = CharBlock(
        required=True, label=_("Texto"), help_text=_("Texto del encabezado")
    )
    size = ChoiceBlock(
        choices=[
            ("", "Seleccione un tamaño de encabezado"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
        label=_("Tamaño"),
        help_text=_("Tamaño del encabezado"),
    )

    class Meta:
        template = "base/blocks/heading_block.html"
        label = _("Encabezado")
        help_text = _("Bloque de encabezado")
        icon = "title"


class BaseStreamBlock(StreamBlock):
    """Contenido base para StreamFields.

    Attributes:
        heading_block: Bloque de encabezado
        paragraph: Bloque de párrafos que implementa RichText
        image: Bloque de imagen
        embed_block: Bloque de incustrado de contenido de una URL
    """

    heading = HeadingBlock(
        required=False,
    )
    paragraph = RichTextBlock(
        required=False,
        label=_("Párrafo"),
        help_text=_("Añada texto formateado a la página"),
        icon="pilcrow",
        features=[
            "bold",
            "italic",
            "ol",
            "ul",
            "hr",
            "superscript",
            "subscript",
            "strikethrough",
            "blockquote",
        ],
    )
    image = CustomImageBlock(required=False, search_index=False)
    embed_block = EmbedBlock(
        label=_("Bloque de incrustado multimedia"),
        help_text=_("Introduzca una URL a incrustar"),
        icon="media",
    )

    class Meta:
        block_counts = {"image": {"max_num": 10}, "embed_block": {"max_num": 10}}
