#!C:\Users\kimur\anaconda3\python.exe

# -*- coding: utf-8 -*-

print("Content-Type: text/html\n")

def CalclulateAteNutrition(userName, day):
    import csv
    
    EatedFoodFilePath = "Excel/DietHistory.csv"
    
    with open(EatedFoodFilePath, 'r', encoding = "utf-8") as f:
        csvreader = csv.reader(f)
        AteFoodList = [row for row in csvreader]
        f.close()
        
    print(day + "<br><br>")
    
    #どれがなんの栄養素かわかりやすいように表示するための配列
    nutritionNameList = [
        "カロリー",
        "タンパク質",
        "脂質",
        "炭水化物",
        "食物繊維"
    ]

    #摂取する食材の栄養素の合計を格納する配列、[合計値（初期値は０）][Excelでの列数 - 1]
    nutritionList = [
        [0, 4], #カロリー エクセルで6列目、Pythonで5
        [0, 5], #タンパク質 エクセルで9列目、Pythonで8
        [0, 6], #脂質 エクセルで11列目、Pythonで10
        [0, 7], #炭水化物 エクセルで17列目、Pythonで16
        [0, 8] #食物繊維 エクセルで21列目、Pythonで20
    ]
    
    userNamePos = 0
    namePos = 2
    amountPos = 3
    dayPos = 1

    #18~29歳男性の、必要な栄養素
    #https://www.glico.com/jp/navi/e07.html
    #ここの値に不足している栄養素を足す
    needNutritionList = [
        2650.0, #カロリー
        65.0, #タンパク質
        73.6, #脂質　総カロリー * 0.25 / 9
        380.9, #炭水化物　総カロリー * 0.575 / 4
        21.0 #食物繊維
    ]
    
    AteFoodPosList = []
    
    for i in range( 1 , len(AteFoodList)):
        listDay = AteFoodList[i][dayPos]
        uName = AteFoodList[i][userNamePos]
        if (listDay == day):
            if (userName == uName):
                AteFoodPosList.append(i)
    
    ateFoodNumber = len(AteFoodPosList)
    ateNameList = [""] * ateFoodNumber
    ateAmountList = [0] * ateFoodNumber
    
    missingNutritionList = [0] * len(nutritionList)
    
    for i in range(ateFoodNumber):
        ateNameList[i] = AteFoodList[AteFoodPosList[i]][namePos]
        ateAmountList[i] = int(AteFoodList[AteFoodPosList[i]][amountPos])
        
        for j in range(len(nutritionList)):   
            arrayNumber = nutritionList[j][1]
            nutritionList[j][0] += float(AteFoodList[AteFoodPosList[i]][arrayNumber])
    
    ate = []
    amount = []
    need = []
    sum = []
    print("----------食べたもの----------<br>")
    for i in range(ateFoodNumber):
        ate.append(ateNameList[i])
        amount.append(ateAmountList[i])
        print(ateNameList[i] + " : " + str(ateAmountList[i]) + "g<br><br>")
    
    print("----------必要栄養素----------<br>")
    for i in range(len(nutritionList)):
        need.append(needNutritionList[i])
        print(nutritionNameList[i] + " : " + str(needNutritionList[i]) + "<br>")
    
    print("----------合計栄養素----------<br>")
    for i in range(len(nutritionList)):
        sum.append(round(nutritionList[i][0], 1))
        nutritionList[i][0] = round(nutritionList[i][0], 1) #小数第一位で丸める
        print(nutritionNameList[i] + " : " +  str(nutritionList[i][0]) + "<br>")
        
    for i in range(len(nutritionList)):
        missingNutritionList[i] = needNutritionList[i] - nutritionList[i][0] #必要栄養素から合計栄養素を引く
        missingNutritionList[i] = round(max(missingNutritionList[i] , 0), 1) #小数第一位で丸める
        
    missingNutritionList.insert(0,userName)
    
    #------------CSV書き込み---------------
    rows = []
    with open('Excel/LackNutrition.csv', 'r', encoding = "utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
        f.close()
    
    changeRow = -1
    i = 0
    for row in rows:
        if (userName == row[0]):
            changeRow = i
        i += 1
    
    if (changeRow == -1):
        with open('Excel/LackNutrition.csv', 'a', newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(missingNutritionList)
            f.close()
        
    else:
        i = 0
        with open('Excel/LackNutrition.csv', 'w', newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            for data in rows:
                if i == changeRow:
                    writer.writerow(missingNutritionList)
                else:
                    writer.writerow(data)
                i += 1
            f.close()
    return missingNutritionList,ate,amount,need,sum