from fastapi import UploadFile, File

from src.db.models.receipt import Receipt
from src.enums.file_extensions import FileExtensions
from src.schemas.receipts import CreateReceiptSchema


class DockGenerator:
    def parse_file_to_receipt(self, file: UploadFile) -> CreateReceiptSchema:
        pass

    def receipt_to_file(self, receipt: Receipt, file_ext: FileExtensions) -> File:
        pass

