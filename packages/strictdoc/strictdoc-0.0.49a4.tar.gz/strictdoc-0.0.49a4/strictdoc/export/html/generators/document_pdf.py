from datetime import datetime
from typing import Optional

from jinja2 import Template

from strictdoc import __version__
from strictdoc.backend.sdoc.models.document import Document
from strictdoc.backend.sdoc.models.document_view import ViewElement
from strictdoc.core.document_tree_iterator import DocumentTreeIterator
from strictdoc.core.project_config import ProjectConfig
from strictdoc.export.html.document_type import DocumentType
from strictdoc.export.html.html_templates import HTMLTemplates
from strictdoc.export.html.renderers.link_renderer import LinkRenderer


class DocumentHTML2PDFGenerator:
    @staticmethod
    def export(
        project_config: ProjectConfig,
        document: Document,
        traceability_index,
        markup_renderer,
        link_renderer: LinkRenderer,
        standalone: bool,
        html_templates: HTMLTemplates,
    ):
        current_view: ViewElement = document.view.get_current_view(
            project_config.view
        )

        output = ""

        date_today = datetime.today().strftime("%Y-%m-%d")
        document_tree_iterator = DocumentTreeIterator(
            traceability_index.document_tree
        )

        custom_html2pdf_template: Optional[Template] = None
        if project_config.html2pdf_template is not None:
            with open(project_config.html2pdf_template) as f:
                custom_html2pdf_template = Template(f.read())

        template = html_templates.jinja_environment().get_template(
            "screens/document/pdf/index.jinja"
        )

        document_iterator = traceability_index.get_document_iterator(document)

        output += template.render(
            project_config=project_config,
            document=document,
            traceability_index=traceability_index,
            link_renderer=link_renderer,
            renderer=markup_renderer,
            standalone=standalone,
            document_type=DocumentType.pdf(),
            document_iterator=document_iterator,
            strictdoc_version=__version__,
            document_tree=traceability_index.document_tree,
            document_tree_iterator=document_tree_iterator,
            custom_html2pdf_template=custom_html2pdf_template,
            date_today=date_today,
            current_view=current_view,
        )

        return output
