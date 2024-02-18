def ocr_djvu_page(ocaid: str, leaf_num: int, engine='easyocr') -> str:
  if engine == 'easyocr':
    from tocky.ocr.easyocr import ocr_djvu_page_easyocr
    return ocr_djvu_page_easyocr(ocaid, leaf_num)
  elif engine == 'tesseract':
    from tocky.ocr.tesseract import ocr_djvu_page_tesseract
    return ocr_djvu_page_tesseract(ocaid, leaf_num)
  else:
    raise ValueError(f'Unknown OCR engine {engine}')