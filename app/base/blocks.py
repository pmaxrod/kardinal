from wagtail import blocks
from wagtail.images.blocks import ImageBlock


class CommonContentBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(
        form_classname="title",
        label="Encabezado",
        required=False,
    )
    paragraph = blocks.RichTextBlock(label="Párrafo", required=False)
    image = ImageBlock(label="Imagen", required=False, search_index=False)

    class Meta:
        block_counts = {"image": {"max_num": 10}}