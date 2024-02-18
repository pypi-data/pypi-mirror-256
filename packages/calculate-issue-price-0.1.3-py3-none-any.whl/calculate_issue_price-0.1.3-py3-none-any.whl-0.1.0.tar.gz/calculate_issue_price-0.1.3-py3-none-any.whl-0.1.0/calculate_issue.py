def calculate_issue_price(fv, fr, mr, n):
    if fr == mr:
        ip = fv
    elif fr > mr:
        cpwf = 1 / (1 + mr) ** n
        opwf = (1 - 1 / (1 + mr) ** n) / mr
        ppi = fv * fr
        ip = round((fv * cpwf), 0) + round((ppi * opwf), 0)
    else:
        cpwf = 1 / (1 + mr) ** n
        opwf = (1 - 1 / (1 + mr) ** n) / mr
        ppi = fv * fr
        ip = round((fv * cpwf), 0) + round((ppi * opwf), 0)
    return ip

# 輸入參數
fv = float(input('票面金額：'))
fr = float(input('票面利率：例如：8%, 請輸入 0.08 '))
mr = float(input('市場利率：例如：8%, 請輸入 0.08 '))
n = int(input('期數：'))

# 自動判別公司債券的發行方式
if (fr > mr):
  print('溢價發行:市場利率低於票面利率')
elif (fr < mr):
  print('折價發行:市場利率高於票面利率')
else:
  print('平價發行:市場利率等於票面利率')

# 計算發行價格
issue_price = calculate_issue_price(fv, fr, mr, n)
print('公司債之發行價格為', format(issue_price, '.0f'))