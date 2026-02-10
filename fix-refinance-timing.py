#!/usr/bin/env python3
"""
Fix refinance timing: Move refinance from Year 4 to end of Year 4
"""
from openpyxl import load_workbook

# Load workbook
wb = load_workbook('/home/ubuntu/.clawdbot/media/inbound/a130e962-3ebd-4341-96bb-8ce6dc6cacc7.xlsx')

# Sheet 5: Update refinance amortization years from 1-10 to 5-14
sheet5 = wb['5_Debt Schedule']
for i, year in enumerate(range(5, 15)):  # Years 5-14
    row = 14 + i  # Starting at row 14
    sheet5[f'K{row}'] = year
    print(f"Updated K{row} to {year}")

# Sheet 6: Change Year 4 debt service to use construction loan
sheet6 = wb['6_Cash Flow Analysis']
# E6 = Year 4 debt service
# Change from referencing refinance loan to construction loan
sheet6['E6'] = "=-'5_Debt Schedule'!$C$10"  # Construction loan annual debt service
print("Updated E6 to reference construction loan debt service")

# Save
output_file = '/home/ubuntu/clawd/oz-fund-proforma-refi-fixed.xlsx'
wb.save(output_file)
print(f"\nSaved to: {output_file}")
