from openpyxl import load_workbook

class ExcelInput:
    Row = ''
    Category_1 = ''
    Category_2 = ''
    Category_3 = ''
    Category_4 = ''
    Category_5 = ''
    Question = ''
    Answer = ''
    Show_in_menu = ''
    Validation = ''


def load_excel_file(filename: str) -> list[ExcelInput]:
    wb = load_workbook(filename = filename, data_only=True)
    ws = wb['Q&A']

    excel_rows_list = []

    for row in ws.iter_rows():
        excelInputElement = ExcelInput()
        excelInputElement.Row = row[0].value
        excelInputElement.Category_1 = row[1].value
        excelInputElement.Category_2 = row[2].value
        excelInputElement.Category_3 = row[3].value
        excelInputElement.Category_4 = row[4].value
        excelInputElement.Category_5 = row[5].value
        excelInputElement.Question = row[6].value
        excelInputElement.Answer = row[7].value
        excelInputElement.Show_in_menu = row[8].value
        excelInputElement.Validation = row[9].value
        excel_rows_list.append(excelInputElement)

    return excel_rows_list
