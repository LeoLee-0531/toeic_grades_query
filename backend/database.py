import msoffcrypto
from io import BytesIO
import openpyxl
import os


class GradeDatabase:
    def __init__(self):
        self.excel_path = 'TOEIC_score.xlsx'
        self.password = '3273'
        self.workbook = None
        self.sheet = None
        self.load_excel()

    def decrypt_excel(self):
        decrypted = BytesIO()
        with open(self.excel_path, "rb") as f:
            office_file = msoffcrypto.OfficeFile(f)
            office_file.load_key(password=self.password)
            office_file.decrypt(decrypted)
        return decrypted

    def load_excel(self):
        try:
            decrypted_excel = self.decrypt_excel()
            self.workbook = openpyxl.load_workbook(decrypted_excel)
            self.sheet = self.workbook.active
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            raise

    def get_grades(self, student_id):
        try:
            for row in self.sheet.iter_rows(min_row=2):
                if str(row[2].value).strip() == student_id:
                    return {
                        'student_id': student_id,
                        'listening_score': row[4].value,
                        'reading_score': row[5].value,
                        'total_score': row[6].value
                    }
            return None
        except Exception as e:
            print(f"Error querying grades: {e}")
            raise

    def __del__(self):
        if self.workbook:
            self.workbook.close()
