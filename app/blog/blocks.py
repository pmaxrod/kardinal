from base.blocks import BaseStreamBlock


class BlogPostBlock(BaseStreamBlock):
    class Meta:
        label="Contenido"
        help_text="Contenido de la entrada del blog"
        icon="doc-full"