from models import Passes, Registers
import xlsxwriter as xl


def create_passes_excel():
    workbook = xl.Workbook("all_passes_excel.xlsx")
    worksheet = workbook.add_worksheet("Passes")

    bold = workbook.add_format({'bold': True})
    worksheet.set_column('A:F', 18)

    worksheet.write('A1', 'Name', bold)
    worksheet.write('B1', 'Phone', bold)
    worksheet.write('C1', 'Weekdays', bold)
    worksheet.write('D1', 'Weekends', bold)
    worksheet.write('E1', 'Weeks', bold)
    worksheet.write('F1', 'Amount', bold)

    all_passes = Passes.find_all()
    count = 0
    for p in all_passes:
        count += 1
        pass_count = {'d': 0, 'e': 0}
        customer_registers = Registers.find_customer_registers(p.pid)
        for i in customer_registers:
            pass_count['d'] += i.days
            pass_count['e'] += i.ends

        worksheet.write_row(count, 0, [p.name, p.phone, pass_count['d'], pass_count['e'], p.weeks, p.amount])

    workbook.close()


