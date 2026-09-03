from backend.documents.processing import content_to_ir
from backend.documents.renderers import BuiltinPdfRenderer, validate_pdf
from backend.documents.service import DocumentService
from backend.documents.themes import THEMES


def test_content_is_converted_to_structured_ir():
    result = content_to_ir("Lesson", "# Forces\n\nNewton's *first* law.\n\n$$ F = ma $$")
    assert result.title == "Lesson"
    assert result.blocks[0] == {"type": "heading", "level": 1, "text": "Forces"}
    assert result.blocks[1]["type"] == "paragraph"
    assert result.blocks[2] == {"type": "equation", "text": "F = ma"}


def test_pdf_validation_rejects_incomplete_output():
    try:
        validate_pdf(b"%PDF-1.7\nnot complete")
    except ValueError:
        pass
    else:
        raise AssertionError("incomplete PDF should be rejected")


def test_content_hash_is_deterministic():
    first = DocumentService.content_hash("A", "body", "default")
    assert first == DocumentService.content_hash("A", "body", "default")
    assert first != DocumentService.content_hash("A", "other", "default")


def test_builtin_themes_are_available_to_renderer():
    assert {"default", "academic", "dark"} <= set(THEMES)
    assert THEMES["academic"]["body_font"] != THEMES["default"]["body_font"]


def test_builtin_renderer_produces_valid_pdf_with_special_blocks():
    document = content_to_ir(
        "Lesson (safe)",
        "# Forces\n\nUse (m = 2) and $$ F = ma $$.\n\n```mermaid\nflowchart LR\nA-->B\n```",
    )
    pdf = BuiltinPdfRenderer().render(document)
    assert validate_pdf(pdf)
    assert b"%PDF-" in pdf
    assert b"%%EOF" in pdf
