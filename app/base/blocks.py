from wagtail import blocks
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


class CaptionedImageBlock(StructBlock):
    image = ImageBlock(required=True)
    attribution = CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "base/blocks/captioned_image_block.html"


class HeadingBlock(StructBlock):
    heading_text = CharBlock( required=True)
    size = ChoiceBlock(
        choices=[
            ("", "Seleccione un tamaño de encabezado"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
        ],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "base/blocks/heading_block.html"


class CommonContentBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(
        form_classname="title",
        label="Encabezado",
        required=False,
    )
    paragraph = blocks.RichTextBlock(label="Párrafo", required=False, icon="pilcrow")
    image = ImageBlock(label="Imagen", required=False, search_index=False)
    embed_block = EmbedBlock(
        help_text="Inserte una URL a incrustar.",
        icon="media",
    )

    class Meta:
        block_counts = {"image": {"max_num": 10}}
