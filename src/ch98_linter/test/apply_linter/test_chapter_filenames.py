from ch00_py.file_toolbox import get_dir_file_strs
from ch98_linter.style import get_chapter_descs, get_filenames_with_wrong_style
from re import findall as re_findall
from pathlib import Path


def get_filenamebase_mapping(filenamebases: list[str]) -> dict:
    base_map = {}
    for focus_filenamebase in filenamebases:
        for check_filenamebase in filenamebases:
            if check_filenamebase.find(focus_filenamebase) > -1:
                if base_map.get(focus_filenamebase) is None:
                    base_map[focus_filenamebase] = []
                base_map[focus_filenamebase].append(check_filenamebase)
    return base_map


def get_file_collisions_set(filenames: list[str]) -> list[str]:
    base_map = get_filenamebase_mapping(filenames)
    collisions = []
    for name_group in base_map.values():
        if len(name_group) > 1:
            collisions.extend(name_group)
    return collisions


def test_check_Chapters_filenames_FollowFileNameConventions_NoNamingCollision():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH
    all_level1_file_bases = set()
    all_level1_filenames = set()
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        level1_file_bases = get_dir_file_strs(chapter_dir, True, False, True)
        level1_file_bases = set(level1_file_bases.keys())
        all_level1_file_bases.update(level1_file_bases)

        level1_filenames = get_dir_file_strs(chapter_dir, None, False, True)
        level1_filenames = set(level1_filenames.keys())
        all_level1_filenames.update(level1_filenames)
        # print(f"{level1_files=}")
        collisions = get_file_collisions_set(level1_file_bases)
        if collisions:
            print(f"{chapter_desc} {collisions=}")
        assert not collisions

    # CHECK for collisions acress chapters
    # WHEN / THEN
    all_collisions = get_file_collisions_set(all_level1_file_bases)
    if all_collisions:
        print(f"{all_collisions=}")
    assert not all_collisions
    assert get_filenames_with_wrong_style(all_level1_filenames) == set()


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


# # TODO activate this test
# def test_images_HaveNoMetadata_AllImagesInSrc():
#     # GIVEN
#     src_dir = Path(__file__).resolve().parents[3]
#     # WHEN
#     failures = get_all_images_with_metadata(src_dir)
#     # THEN
#     assertion_failure_str = "Images containing metadata were found:\n"
#     assert not failures, assertion_failure_str + "\n".join(failures)
