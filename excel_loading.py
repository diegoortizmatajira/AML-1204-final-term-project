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

    def __init__(self,Row,Category_1,Category_2,Category_3,Category_4,Category_5,Question,Answer,Show_in_menu,Validation):
        self.Row = Row
        self.Category_1 = Category_1
        self.Category_2 = Category_2
        self.Category_3 = Category_3
        self.Category_4 = Category_4
        self.Category_5 = Category_5
        self.Question = Question
        self.Answer = Answer
        self.Show_in_menu = Show_in_menu
        self.Validation = Validation


class ExcelHeader:
    name: str = 'Sample chatbot'
    description: str = 'This is a sample chatbot'
    welcome_message: str = 'Hello, how can I help you?'
    selection_message: str = 'Please tell me which option fits your question?'
    selection_continuation_message: str = 'There are other options that may help you...'
    formal_offering_message: str = 'Can I help you with anything else?'
    final_message: str = 'Thank you for using this chat, hope to see you soon'
    feedback_message: str = 'Please provide feedback... Was the answer I gave you useful?'


def load_excel_file(filename: str) -> (list[ExcelInput], ExcelHeader):
    wb = load_workbook(filename=filename, data_only=True)
    ws = wb['Q&A']

    excel_rows_list = []

    for row in ws.iter_rows():
        Row = row[0].value
        Category_1 = row[1].value
        Category_2 = row[2].value
        Category_3 = row[3].value
        Category_4 = row[4].value
        Category_5 = row[5].value
        Question = row[6].value
        Answer = row[7].value
        Show_in_menu = row[8].value
        Validation = row[9].value

        excelInputElement = ExcelInput(Row,Category_1,Category_2,Category_3,Category_4,Category_5,Question,Answer,Show_in_menu,Validation)
        excel_rows_list.append(excelInputElement)

    return excel_rows_list, ExcelHeader()
