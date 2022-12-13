import sys

sys.stdin = open('provinces.txt', 'r')
sys.stdout = open('provinces-options.txt', 'w')

for i in range(38):
    row = input()
    province = row.split('. ')[1].split(' (')[0]
    print(f'<option value="{province}">{province}</option>')