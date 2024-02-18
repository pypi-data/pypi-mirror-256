import math
from lxml import etree
from rtree import index

from tocky.ia import extract_page_index, get_ia_metadata, get_page_scan
from tocky.ocr import ocr_djvu_page
from tocky.utils import avg_ocr_conf

def extract_djvu_page_text_old(djvu_page: str | etree._Element) -> str:
    if isinstance(djvu_page, str):
       root = etree.fromstring(djvu_page)
    else:
        root = djvu_page
    page_file = root.xpath('./@usemap')[0]

    result = f"\n\n----------- OCR of page {extract_page_index(page_file)} -----------\n\n\n"

    ref_word = next(
        word
        for word in root.findall('.//WORD')
        if len(word.text) > 8
    )
    ref_word_coords = ref_word.xpath("./@coords")[0].split(',')
    ref_word_width = int(ref_word_coords[2]) - int(ref_word_coords[0])
    char_width = ref_word_width / len(ref_word.text)

    for pagecol in root.findall('.//PAGECOLUMN'):
        for par in pagecol.findall('.//PARAGRAPH'):
            for line in par.findall('.//LINE'):
                words = line.findall('.//WORD')
                if words:
                    coords = line.xpath('.//WORD/@coords')[0].split(',')

                    line_indent = math.floor(int(coords[0]) / char_width)
                    line_text = ' '.join(word.text.strip() for word in words)
                    indented_line = ' ' * line_indent + line_text
                    result += indented_line + '\n'

    return result

def extract_djvu_page_text(djvu_page: str | etree._Element, re_ocr=False) -> str:
    if isinstance(djvu_page, str):
       root = etree.fromstring(djvu_page)
    else:
        root = djvu_page
    canvas = ""
    page_file = root.xpath('./@usemap')[0]
    ocaid = page_file.rsplit('_', 1)[0]
    leaf_num = extract_page_index(page_file)

    # Convert inches to pixels
    dpi = int((root.xpath(".//PARAM[@name='DPI']/@value") or [int(get_ia_metadata(ocaid)['ppi'])])[0])
    line_rounding_size = round(0.0333 * dpi)

    if re_ocr and root.xpath('.//HIDDENTEXT/@x-re-ocrd') != ['true']:
      new_ocr = ocr_djvu_page(get_page_scan(ocaid, leaf_num))
      new_ocr_el = etree.fromstring(new_ocr)
      if (avg_ocr_conf(new_ocr_el) or 100) > (avg_ocr_conf(root.find('.//HIDDENTEXT')) or 0):
        root.replace(root.find('.//HIDDENTEXT'), new_ocr_el)

    canvas_width = 120  # dpi // 4
    conv_factor = canvas_width / int(root.xpath('./@width')[0])
    canvas_height = math.ceil(int(root.xpath('./@height')[0]) * conv_factor)
    canvas = ((" " * canvas_width + '\n') * canvas_height)[:-1]

    # if Path('./tmp.log').exists():
    #   Path('./tmp.log').unlink()

    # def log(message: str) -> None:
    #   log_file = Path('./tmp.log')

    #   # Ensure the file and its parent directory exist
    #   log_file.parent.mkdir(parents=True, exist_ok=True)

    #   # Append the message to the file
    #   with open(log_file, 'a') as file:
    #       file.write(message + '\n')

    # log(f'{conv_factor=} {canvas_width=} {canvas_height=}')
    used_regions = index.Index()
    rect_index = 0
    for pagecol in root.findall('.//PAGECOLUMN'):
        for par in pagecol.findall('.//PARAGRAPH'):
            for line in par.findall('.//LINE'):
                # log('LINE')
                line_row = None
                for word in line.findall('.//WORD'):
                    coords = word.xpath('./@coords')[0].split(',')
                    left = int(coords[0])
                    bottom = int(coords[1])
                    right = int(coords[2])
                    top = int(coords[3])

                    baseline = round((top + (bottom - top) / 3) / line_rounding_size) * line_rounding_size
                    line_row = math.floor(baseline * conv_factor) if line_row is None else line_row
                    col = math.floor(left * conv_factor)

                    while list(used_regions.intersection(rect := (col, line_row, col + len(word.text), line_row + 1))):
                      col += 1

                    used_regions.insert(rect_index, rect)
                    rect_index += 1

                    start_idx = (canvas_width + 1) * line_row + col
                    end_idx = start_idx + len(word.text)
                    shift = 0
                    max_shift = 5
                    # log(f'{line_row}:{col}\t{coords}\t{word.text}')
                    # while not canvas[max(0, start_idx - 1):(end_idx + 1)].isspace():
                    #   start_idx += 1
                    #   end_idx += 1
                    #   shift += 1
                    #   if shift >= max_shift:
                    #     break
                    canvas = canvas[0:start_idx] + word.text + canvas[end_idx:]

    def crop_text_canvas(canvas: str) -> str:
      lines = canvas.split('\n')
      line_len = len(lines[0])
      top = 0
      left = line_len
      right = 0
      bottom = 0

      for line in lines:
        left = min(left, line_len - len(line.lstrip()))
        right = max(right, len(line.rstrip()))

      for line in lines:
        if not line.isspace():
          break
        top += 1

      for line in reversed(lines):
        if not line.isspace():
          break
        bottom += 1
      return '\n'.join((
          line[left:right] if not line.isspace() else ''
          for line in lines[top:-max(bottom, 1)]
      ))

    def collapse_newlines(s: str):
        import re
        min_newline_chain = min(map(len, re.findall(r'\n+', s.strip(), re.MULTILINE)), default=1)

        return re.sub(r'\n' * (min_newline_chain -1) + '(\n*)', r'\1', s, flags=re.MULTILINE)
        # return re.sub(r'\n+', '\n', s, flags=re.MULTILINE)

    def collapse_spaces(s: str):
        import re
        min_newline_chain = min(map(len, re.findall(r' +', s.strip(), re.MULTILINE)), default=1)

        return re.sub(r' ' * (min_newline_chain -1) + '( *)', r'\1', s, flags=re.MULTILINE)
        # return re.sub(r'(\S) +', r'\1 ', s)

    return collapse_newlines(crop_text_canvas(canvas))
