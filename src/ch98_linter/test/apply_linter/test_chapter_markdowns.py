from re import findall as re_findall
from pathlib import Path


def get_image_paths_from_markdown(md_text: str) -> list[str]:
    """Extract image paths from markdown and html img tags."""
    markdown_imgs = re_findall(r"!\[[^\]]*]\(([^)]+)\)", md_text)
    html_imgs = re_findall(r'<img[^>]*src=["\']([^"\']+)["\']', md_text)
    return markdown_imgs + html_imgs


def get_missing_markdown_image_file_links(src_dir: Path) -> list[str]:
    missing_files: list[str] = []
    for md_file in src_dir.rglob("*.md"):
        # print(f"{md_file=}")
        md_text = md_file.read_text(encoding="utf-8")

        for image_path_str in get_image_paths_from_markdown(md_text):
            image_path_str = image_path_str.strip()
            if image_path_str.startswith(("http://", "https://")):
                continue

            if image_path_str.startswith("/"):
                image_path = src_dir / image_path_str.lstrip("/")
            else:
                image_path = md_file.parent / image_path_str

            if not image_path.exists():
                missing_files.append(f"{md_file}: image not found -> {image_path_str}")
    return missing_files


def get_all_images_with_metadata(src_dir: Path) -> list[str]:
    failures = []
    for image_path in src_dir.rglob("*"):
        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        data = image_path.read_bytes()

        if found_markers := [
            marker.decode(errors="ignore")
            for marker in FORBIDDEN_MARKERS
            if marker in data
        ]:
            failures.append(f"{image_path}: found metadata markers {found_markers}")
    return failures


def test_MarkdownImageLinksFilesExist() -> None:
    # GIVEN
    # repo_root = Path("src").resolve().parents[1]
    src_dir = Path(__file__).resolve().parents[3]

    # WHEN
    missing_files = get_missing_markdown_image_file_links(src_dir)

    # THEN
    assert not missing_files, "\n".join(missing_files)


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
FORBIDDEN_MARKERS = {
    b"Exif",
    b"http://ns.adobe.com/xap",  # XMP
    b"Photoshop",
    b"ICC_PROFILE",
    b"XML:com.adobe.xmp",
    b"tEXt",
    b"iTXt",
    b"zTXt",
}


# # TODO activate this test
# def test_images_HaveNoMetadata_AllImagesInSrc():
#     # GIVEN
#     src_dir = Path(__file__).resolve().parents[3]
#     # WHEN
#     failures = get_all_images_with_metadata(src_dir)
#     # THEN
#     assertion_failure_str = "Images containing metadata were found:\n"
#     assert not failures, assertion_failure_str + "\n".join(failures)


def get_markdown_footnote_failures(src_dir: Path) -> list[str]:
    failures: list[str] = []

    footnote_pattern = r"\[\^([^\]]+)\]"

    for md_file in src_dir.rglob("*.md"):
        md_text = md_file.read_text(encoding="utf-8")

        footnotes = re_findall(footnote_pattern, md_text)

        counts: dict[str, int] = {}
        for footnote in footnotes:
            counts[footnote] = counts.get(footnote, 0) + 1

        failures.extend(
            f"{md_file}: footnote [^{footnote}] appears {count} times (expected 2)"
            for footnote, count in sorted(counts.items())
            if count != 2
        )
    return failures


def test_MarkdownFootnotesAreMirrored() -> None:
    # GIVEN
    src_dir = Path(__file__).resolve().parents[3]

    # WHEN
    failures = get_markdown_footnote_failures(src_dir)

    # THEN
    assert not failures, "\n".join(failures)


def get_markdown_footnote_order_failures(src_dir: Path) -> list[str]:
    failures: list[str] = []

    for md_file in src_dir.rglob("*.md"):
        md_text = md_file.read_text(encoding="utf-8")

        references = [int(x) for x in re_findall(r"\[\^(\d+)\](?!:)", md_text)]

        expected = list(range(1, len(references) + 1))

        if references != expected:
            failures.append(
                f"{md_file}: footnotes are out of order "
                f"(found {references}, expected {expected})"
            )

    return failures


def test_MarkdownFootnotesAreInOrder() -> None:
    # GIVEN
    src_dir = Path(__file__).resolve().parents[3]

    # WHEN
    failures = get_markdown_footnote_order_failures(src_dir)

    # THEN
    assert not failures, "\n".join(failures)


def get_file_paths_from_markdown(md_text: str) -> list[str]:
    """Extract markdown file links (excluding images)."""
    return re_findall(r"(?<!!)\[[^\]]*]\(([^)]+)\)", md_text)


def get_missing_markdown_file_links(src_dir: Path) -> list[str]:
    missing_files: list[str] = []

    for md_file in src_dir.rglob("*.md"):
        md_text = md_file.read_text(encoding="utf-8")

        for file_path_str in get_file_paths_from_markdown(md_text):
            file_path_str = file_path_str.strip()

            # Skip anchors
            if file_path_str.startswith("#"):
                continue

            # Skip external links
            if file_path_str.startswith(("http://", "https://")):
                continue

            # Remove anchor portion from local links
            file_path_str = file_path_str.split("#")[0]

            if not file_path_str:
                continue

            if file_path_str.startswith("/"):
                file_path = src_dir / file_path_str.lstrip("/")
            else:
                file_path = md_file.parent / file_path_str

            if not file_path.exists():
                missing_files.append(f"{md_file}: file not found -> {file_path_str}")

    return missing_files


def test_MarkdownFileLinksFilesExist() -> None:
    # GIVEN
    src_dir = Path(__file__).resolve().parents[3]

    # WHEN
    missing_files = get_missing_markdown_file_links(src_dir)

    # THEN
    assert not missing_files, "\n".join(missing_files)
