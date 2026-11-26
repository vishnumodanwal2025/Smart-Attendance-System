import re

builder_path = "build_full_frontend.py"
with open(builder_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace all occurrences of Dr. Shubham Singh with Dr. Ashish Kumar
count_shubham = content.count("Dr. Shubham Singh")
content = content.replace("Dr. Shubham Singh", "Dr. Ashish Kumar")
print(f"Replaced {count_shubham} occurrences of 'Dr. Shubham Singh' with 'Dr. Ashish Kumar'")

# 2. Adjust rowspan from 6 to 5 for break-col and lunch-col
content = content.replace('<td rowspan="6" class="break-col">B R E A K</td>', '<td rowspan="5" class="break-col">B R E A K</td>')
content = content.replace('<td rowspan="6" class="lunch-col">L U N C H</td>', '<td rowspan="5" class="lunch-col">L U N C H</td>')

# 3. Remove Saturday row from the table
sat_block = """            <!-- SAT -->
            <tr>
              <td class="day-col">SAT</td>
              <td colspan="5"><div class="tt-cell-item" style="background:#fef9c3; color:#854d0e; font-weight:700;">Mock Test &amp; Departmental Activities</div></td>
              <td colspan="3"><div class="tt-cell-item" style="background:#fef9c3; color:#854d0e; font-weight:700;">Mock Test &amp; Departmental Activities</div></td>
            </tr>"""

sat_block_crlf = sat_block.replace("\n", "\r\n")

if sat_block in content:
    content = content.replace(sat_block, "")
    print("Successfully removed SAT block (LF)")
elif sat_block_crlf in content:
    content = content.replace(sat_block_crlf, "")
    print("Successfully removed SAT block (CRLF)")
else:
    # Regex fallback
    content = re.sub(r'\s*<!-- SAT -->\s*<tr>\s*<td class="day-col">SAT</td>.*?</tr>', '', content, flags=re.DOTALL)
    print("Removed SAT block via regex")

with open(builder_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated build_full_frontend.py successfully!")
