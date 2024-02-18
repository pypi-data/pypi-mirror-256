"""PDFbox Package."""
__all__ = (
    "PDFBOX_DATA",
    "PDFBOX_DATA_TESTS",
    "PDF_REDUCE_THRESHOLD",
    "SCAN_PREFIX",
    "exif_rm_tags",
    "exif_transform_date",
    "linearized",
    "metadata",
    "pdf_diff",
    "pdf_from_picture",
    "pdf_linearize",
    "pdf_reduce",
    "pdf_scan",
    "pdf_to_picture",
    "picture_paste",
    "putalpha_random",
    "white_alpha",
)

import contextlib
import datetime
import difflib
import random
import re
import shutil
import subprocess
import tempfile
from typing import Literal

import fitz
import nodeps
import numpy as np
import pikepdf
from dateutil.tz import tzoffset, tzutc
from nodeps import AnyPath, Path
from PIL import Image
from PIL.Image import Resampling

PDFBOX_DATA = Path(__file__).parent / "data"
PDFBOX_DATA_TESTS = PDFBOX_DATA / "tests"
PDF_REDUCE_THRESHOLD = 2000000
"""Reduce pdf for files bigger than 2MB"""
SCAN_PREFIX = "scanned_"


pdf_date_pattern = re.compile("(D:)?(?P<year>\\d\\d\\d\\d)(?P<month>\\d\\d)(?P<day>\\d\\d)(?P<hour>\\d\\d)(?P<minute>"
                              "\\d\\d)(?P<second>\\d\\d)(?P<tz_offset>[+-zZ])?(?P<tz_hour>"
                              "\\d\\d)?'?(?P<tz_minute>\\d\\d)?'?")


def exif_rm_tags(file: Path | str):
    """Removes tags with exiftool in pdf."""
    nodeps.which("exiftool", raises=True)
    nodeps.which("mat2", raises=True)
    subprocess.run(["mat2", "--inplace", file])

    subprocess.check_call(["exiftool", "-q", "-q", "-all=", "-overwrite_original", file])


def exif_transform_date(data: str | pikepdf.Object) -> datetime.datetime | str | pikepdf.Object:
    """Convert a pdf date such as "D:20120321183444+07'00'" into a usable datetime.

    https://www.verypdf.com/pdfinfoeditor/pdf-date-format.htm
    (D:YYYYMMDDHHmmSSOHH'mm')

    Examples:
        >>> from kitpdf import exif_transform_date
        >>>
        >>> exif_transform_date("D:20201002181301Z")
        datetime.datetime(2020, 10, 2, 18, 13, 1, tzinfo=tzutc())

    Args:
        data: text to find match and convert.

    Returns:
        datetime.datetime or None if no match.
    """
    if isinstance(data, str) and (match := re.match(pdf_date_pattern, data)):
        date_info = match.groupdict()

        for k, v in date_info.items():  # transform values
            if v is None:
                pass
            elif k == 'tz_offset':
                date_info[k] = v.lower()  # so we can treat Z as z
            else:
                date_info[k] = int(v)

        if date_info['tz_offset'] in ('z', None):  # UTC
            date_info['tzinfo'] = tzutc()
        else:
            multiplier = 1 if date_info['tz_offset'] == '+' else -1
            date_info['tzinfo'] = tzoffset(None, multiplier*(3600 * date_info['tz_hour'] + 60 * date_info['tz_minute']))

        for k in ('tz_offset', 'tz_hour', 'tz_minute'):  # no longer needed
            del date_info[k]

        return datetime.datetime(**date_info)  # noqa: DTZ001
    return data


def linearized(file: Path | str) -> bool:
    """Check if metadata Linearize if Yes.

    Examples:
        >>> import datetime
        >>> from kitpdf import linearized, PDFBOX_DATA_TESTS
        >>>
        >>> assert linearized(PDFBOX_DATA_TESTS / "BBVA.pdf") is False

    Args:
        file: file to check linearize metadata
    """
    return metadata(file).get("Linearized", "No") == "Yes"


def metadata(file: Path | str, slash: bool = False) -> dict[str, str | datetime.datetime]:
    """Returns file metadata.

    Examples:
        >>> import datetime
        >>> from kitpdf import metadata, PDFBOX_DATA_TESTS
        >>>
        >>> meta = metadata(PDFBOX_DATA_TESTS / "BBVA.pdf")
        >>> assert isinstance(meta["CreationDate"], datetime.datetime)
        >>> assert meta["Author"] == "BBVA"

    Args:
        file: file to get metadata
        slash: False default to remove start / and convert pikepdf.String to str.

    Returns:
        datetime.datetime or None if no match.

    """
    def _parse(data):
        data = str(data) if isinstance(data, pikepdf.String) else data
        return data.removeprefix("/") if slash is False and isinstance(data := exif_transform_date(data), str) else data

    pdf = pikepdf.Pdf.open(file)
    return {_parse(key): _parse(value) for key, value in pdf.docinfo.items()}


def pdf_diff(file1: Path | str, file2: Path | str) -> list[bytes]:
    """Show diffs of two pdfs.

    Args:
        file1: file 1
        file2: file 2

    Returns:
        True if equals
    """
    return list(
        difflib.diff_bytes(
            difflib.unified_diff, Path(file1).read_bytes().splitlines(), Path(file2).read_bytes().splitlines(), n=1
        )
    )


def pdf_from_picture(file: Path | str, picture: Path | str, rm: bool = True) -> Path:
    """Creates pdf from image.

    Args:
        file: pdf file
        picture: image file
        rm: remove image file (default: True)
    """
    doc = fitz.Document()
    doc.new_page()
    page = doc[0]
    page.insert_image(page.rect, filename=picture)
    doc.save(Path(file))
    if rm:
        Path(picture).unlink()
    return file


def pdf_linearize(file: Path | str) -> None:
    """Linearize pdf (overwrites original)."""
    nodeps.which("qpdf")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir) / "tmp.pdf"
        subprocess.run(["qpdf", "--linearize", file, tmp])
        Path(tmp).replace(file)


def pdf_reduce(
        path: Path | str,
        level: Literal["/default", "/prepress", "ebook", "/screen"] = "/ebook",
        threshold: int | None = PDF_REDUCE_THRESHOLD,
) -> None:
    """Compress pdf.

    https://www.adobe.com/acrobat/hub/how-to-compress-pdf-in-linux.html

    Examples:
        >>> import shutil
        >>> from nodeps import Path
        >>> from kitpdf import PDFBOX_DATA_TESTS
        >>> from kitpdf import pdf_reduce
        >>>
        >>> original = PDFBOX_DATA_TESTS / "5.2M.pdf"
        >>> backup = PDFBOX_DATA_TESTS / "5.2M-bk.pdf"
        >>>
        >>> shutil.copyfile(original, backup)  # doctest: +ELLIPSIS
        Path('.../kitpdf/data/tests/5.2M-bk.pdf')
        >>> original_size = original.stat().st_size
        >>> pdf_reduce(original, level="/screen")
        >>> reduced_size = original.stat().st_size
        >>> assert original_size != reduced_size  # doctest: +SKIP
        >>> shutil.move(backup, original)  # doctest: +ELLIPSIS
        Path('.../kitpdf/data/tests/5.2M.pdf')

    Args:
        path: path to file
        threshold: limit in MB to reduce file size, None to reuce any pdf
        level: /default is selected by the system, /prepress 300 dpi, ebook 150 dpi, screen 72 dpi

    Returns:
        None
    """
    if threshold is None or Path(path).stat().st_size > threshold:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir) / "tmp.pdf"
            subprocess.check_call(
                [
                    "gs",
                    "-sDEVICE=pdfwrite",
                    "-dCompatibilityLevel=1.4",
                    f"-dPDFSETTINGS={level}",
                    "-dNOPAUSE",
                    "-dQUIET",
                    "-dBATCH",
                    f"-sOutputFile={tmp}",
                    path,
                ]
            )
            Path(tmp).replace(path)


def pdf_scan(file: Path, directory: Path | None = None) -> Path:
    """Looks like scanned, linearize and sets tag color.

    Examples:
        >>> from pathlib import Path
        >>> from kitpdf import PDFBOX_DATA
        >>> from kitpdf import PDFBOX_DATA_TESTS
        >>> from kitpdf import SCAN_PREFIX
        >>> from kitpdf import pdf_scan
        >>>
        >>> for f in Path(PDFBOX_DATA_TESTS).iterdir():
        ...     if f.is_file() and f.suffix == ".pdf":
        ...         assert f"generated/{SCAN_PREFIX}" in str(pdf_scan(f, PDFBOX_DATA_TESTS / "generated"))

    Args:
        file: path of file to be scanned
        directory: destination directory (Default: file directory)

    Returns:
        Destination file
    """
    rotate = round(random.uniform(*random.choice([(-0.9, -0.5), (0.5, 0.9)])), 2)  # noqa: S311

    file = Path(file)
    filename = f"{SCAN_PREFIX}{file.stem}{file.suffix}"
    if directory:
        directory = Path(directory)
        if not directory.is_dir():
            directory.mkdir()
        dest = directory / filename
    else:
        dest = file.with_name(filename)

    nodeps.which("convert", raises=True)

    subprocess.check_call(
        [
            "convert",
            "-density",
            "120",
            file,
            "-attenuate",
            "0.4",
            "+noise",
            "Gaussian",
            "-rotate",
            str(rotate),
            "-attenuate",
            "0.03",
            "+noise",
            "Uniform",
            "-sharpen",
            "0x1.0",
            dest,
        ]
    )
    return dest


@contextlib.contextmanager
def pdf_to_picture(source: AnyPath, dest: AnyPath | Literal["dir", "tmp"] = "dir", dpi: int = 300,
                   fmt: Literal["jpeg", "png"] = "png") -> Path:
    """Creates a file with jpeg in the same directory from first page of pdf.

    Examples:
        >>> from kitpdf import PDFBOX_DATA_TESTS
        >>> from kitpdf import pdf_to_picture
        >>>
        >>> src = PDFBOX_DATA_TESTS / "BBVA.pdf"
        >>>
        >>> with pdf_to_picture(src, PDFBOX_DATA_TESTS / f"generated/BBVA-{putalpha_random.__name__}.png") as output:
        ...     assert output.exists()
        ...     assert output.suffix == ".png"
        >>>
        >>> with pdf_to_picture(src, "tmp") as temp:
        ...     assert temp.exists()
        ...     assert temp.suffix == ".png"
        >>>
        >>> with pdf_to_picture(src) as png:
        ...     assert png.exists()
        ...     assert png.suffix == ".png"

    Arguments:
        source: Source pdf to converto to picture
        dest: Destination path, dir to use the same same path with different suffix or tmp for temp file
        dpi: dpi
        fmt: output jpeg or png

    Returns:
        Temp path with new image or destination
    """
    nodeps.which("pdftoppm")

    source = Path(source)

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir) / "tmp"
            subprocess.check_call(["pdftoppm", f"-{fmt}", "-r", str(dpi), "-singlefile", source, tmp])
            suffix = f".{fmt}" if fmt == "png" else ".jpg"
            if not (tmp := tmp.with_suffix(suffix)).exists():
                msg = f"File not found {tmp}"
                raise FileNotFoundError(msg)
            if dest == "dir":
                yield shutil.copy(tmp, source.with_suffix(suffix))
            elif dest == "tmp":
                yield tmp
            else:
                yield shutil.copy(tmp, dest)
    finally:
        pass


@contextlib.contextmanager
def picture_paste(
        background: AnyPath,
        foreground: AnyPath,
        dest: AnyPath = None,
        putalpha: bool = True,
        position: tuple[int, int] | tuple[int, int, int, int] | None = (0, 0),
        stamp: bool = False,
) -> Path:
    """Paste the foreground image on top of the background image.

    Examples:
        >>> from kitpdf import PDFBOX_DATA_TESTS
        >>> from kitpdf import picture_paste
        >>>
        >>> src = PDFBOX_DATA_TESTS / "BBVA.png"
        >>> fo = PDFBOX_DATA_TESTS / "folded.png"
        >>>
        >>> with picture_paste(fo, src, PDFBOX_DATA_TESTS / f"generated/folded-BBVA-{picture_paste.__name__}.png") as o:
        ...     assert o.exists()
        ...     assert o.suffix == ".png"
        >>>
        >>> with picture_paste(fo, src) as temp:
        ...     assert temp.exists()
        ...     assert temp.suffix == ".png"
        >>>
        >>> src = PDFBOX_DATA_TESTS / "BioSalud Stamp Transparent.png"
        >>> d = PDFBOX_DATA_TESTS / f"generated/BioSalud Stamp Transparent-{picture_paste.__name__}.png"
        >>> with picture_paste(fo, src, d, position=(300, 420)) as o:
        ...     assert o.exists()
        ...     assert o.suffix == ".png"
        >>>
        >>> src = PDFBOX_DATA_TESTS / "generated/BBVA-white_alpha.png"
        >>> d = PDFBOX_DATA_TESTS / f"generated/BBVA-white_alpha-{picture_paste.__name__}.png"
        >>> with picture_paste(fo, src, d, position=(0, 210)) as o:
        ...     assert o.exists()
        ...     assert o.suffix == ".png"
        >>>

    Arguments:
        background: Background image
        foreground: Foreground image
        dest: None for temp path or dest
        putalpha: Put alpha channel (transparency) to random value `putalpha_random()` before pasting
        position: position of foreground image, if position is (0,0) background is resized to same size as forground
        stamp: True to stamp the foreground image
    """
    try:
        if foreground is None:
            yield background
        else:
            bg = Image.open(background).convert("RGBA")
            fg = Image.open(foreground).convert("RGBA")

            if stamp:
                putalpha = False
                x = random.randint(int(0.1 * bg.size[0]), int(0.7 * bg.size[0]))  # noqa: S311
                y = random.randint(int(0.6 * bg.size[1]), int(0.85 * bg.size[1]))  # noqa: S311
                puntos = Image.open(PDFBOX_DATA / "Puntos.png").convert("RGBA")
                puntos = puntos.resize(fg.size, resample=Resampling.NEAREST)
                puntos = puntos.rotate(random.randint(0, 180))  # noqa: S311
                fg.paste(puntos, (0, 0), puntos)
                fg = fg.resize(fg.size, resample=Resampling.NEAREST)
                fg = fg.rotate(random.randint(8, 48), expand=True)  # noqa: S311
                position = (x, y)

            if position == (0, 0):
                bg = bg.resize(fg.size)

            if putalpha:
                with putalpha_random(foreground) as fg:
                    f = Image.open(fg).convert("RGBA")
                    if not stamp:
                        bg = bg.rotate(random.randint(0, 3), expand=False)  # noqa: S311
                    bg.paste(f, position, f)
                    with tempfile.TemporaryDirectory() as tmpdir:
                        tmp = Path(tmpdir) / "paste.png"
                        bg.save(tmp, "PNG")
                        if dest is None:
                            yield tmp
                        else:
                            yield shutil.copy(tmp, dest)
            else:
                bg.paste(fg, position, fg)
                with tempfile.TemporaryDirectory() as tmpdir:
                    tmp = Path(tmpdir) / "paste.png"
                    bg.save(tmp, "PNG")
                    if dest is None:
                        yield tmp
                    else:
                        yield shutil.copy(tmp, dest)
    finally:
        pass


@contextlib.contextmanager
def putalpha_random(source: AnyPath, dest: AnyPath = None, value: tuple[int, int] = (0.62, 0.72)) -> Path:
    """Put alpha channel (transparency) to random value.

    Examples:
        >>> from kitpdf import putalpha_random
        >>> from kitpdf import PDFBOX_DATA_TESTS
        >>>
        >>> src = PDFBOX_DATA_TESTS / "BBVA.pdf"
        >>> pic = PDFBOX_DATA_TESTS / f"generated/BBVA-{putalpha_random.__name__}.png"
        >>> with (pdf_to_picture(src, dest=pic) as picture, putalpha_random(picture) as out):
        ...     assert out.exists()
        ...     assert out.suffix == ".png"
        >>> with (putalpha_random(src) as temp):
        ...     assert temp.exists()
        ...     assert temp.suffix == ".png"

    Arguments:
        source: Source image, or pdf to converto to png
        dest: Destination path or None for temp file
        value: Tuple of min and max value

    Returns:
        Temp path with new image or destination
    """
    @contextlib.contextmanager
    def _putalpha_random(src) -> Path:
        img = Image.open(src)
        img.putalpha(int(random.uniform(*value) * 255))  # noqa: S311
        try:
            if dest:
                img.save(dest)
                yield Path(dest)
            else:
                with tempfile.TemporaryDirectory() as tmpdir:
                    tmp = Path(tmpdir) / "tmp.png"
                    img.save(tmp)
                    if not tmp.exists():
                        msg = f"File not found {tmp}"
                        raise FileNotFoundError(msg)
                    yield tmp
        finally:
            pass

    source = Path(source)

    if source.suffix == ".pdf":
        with (pdf_to_picture(source) as png, _putalpha_random(png) as alpha):
            yield alpha
    else:
        with _putalpha_random(source) as alpha:
            yield alpha


@contextlib.contextmanager
def white_alpha(source: AnyPath, dest: AnyPath = None) -> Path:
    """Make the white pixels transparent.

    Examples:
        >>> from kitpdf import white_alpha
        >>> from kitpdf import PDFBOX_DATA_TESTS
        >>>
        >>> src = PDFBOX_DATA_TESTS / "Biosalud Stamp.png"
        >>> with white_alpha(src, PDFBOX_DATA_TESTS / f"generated/Biosalud Stamp-{white_alpha.__name__}.png", ) as out:
        ...     assert out.exists()
        ...     assert out.suffix == ".png"
        >>> with white_alpha(src) as temp:
        ...     assert temp.exists()
        ...     assert temp.suffix == ".png"
        >>>
        >>> src = PDFBOX_DATA_TESTS / "BBVA.png"
        >>> with white_alpha(src, PDFBOX_DATA_TESTS / f"generated/BBVA-{white_alpha.__name__}.png", ) as out:
        ...     assert out.exists()
        ...     assert out.suffix == ".png"


    Arguments:
        source: Source image, or pdf to converto to png
        dest: Destination path or None for temp file

    Returns:
        path temp or dest
    """
    image = np.asarray(Image.open(source).convert("RGBA"))
    r, g, b, a = np.rollaxis(image, axis=-1)  # split into 4 n x m arrays
    r_m = r != 255  # binary mask for red channel, True for all non white values  # noqa: PLR2004
    g_m = g != 255  # binary mask for green channel, True for all non white values  # noqa: PLR2004
    b_m = b != 255  # binary mask for blue channel, True for all non white values  # noqa: PLR2004

    # combine the three masks using the binary "or" operation
    # multiply the combined binary mask with the alpha channel
    a = a * ((r_m == 1) | (g_m == 1) | (b_m == 1))

    # stack the img back together
    image = Image.fromarray(np.dstack([r, g, b, a]), 'RGBA')
    try:
        if dest:
            image.save(dest)
            yield Path(dest)
        else:
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp = Path(tmpdir) / "tmp.png"
                image.save(tmp)
                if not tmp.exists():
                    msg = f"File not found {tmp}"
                    raise FileNotFoundError(msg)
                yield tmp
    finally:
        pass
