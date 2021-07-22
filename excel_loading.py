# You will first need to install the 'xlrd' package

import xlrd


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


class ExcelHeader:
    name: str = 'Sample chatbot'
    description: str = 'This is a sample chatbot'
    welcome_message: str = 'Hello, how can I help you?'
    selection_message: str = 'Please tell me which option fits your question?'
    selection_continuation_message: str = 'There are other options that may help you...'
    formal_offering_message: str = 'Can I help you with anything else?'
    final_message: str = 'Thank you for using this chat, hope to see you soon'


def load_excel_file(filename: str) -> (list[ExcelInput], ExcelHeader):
    wb = xlrd.open_workbook(filename)
    sh = wb.sheet_by_index(0)

    excel_rows_list = []

    for row_num in range(1, sh.nrows):
        row_values = sh.row_values(row_num)

        excelInputElement = ExcelInput()
        excelInputElement.Row = row_values[0]
        excelInputElement.Category_1 = row_values[1]
        excelInputElement.Category_2 = row_values[2]
        excelInputElement.Category_3 = row_values[3]
        excelInputElement.Category_4 = row_values[4]
        excelInputElement.Category_5 = row_values[5]
        excelInputElement.Question = row_values[6]
        excelInputElement.Answer = row_values[7]
        excelInputElement.Show_in_menu = row_values[8]
        excelInputElement.Validation = row_values[9]
        excel_rows_list.append(excelInputElement)

    return excel_rows_list, ExcelHeader()
