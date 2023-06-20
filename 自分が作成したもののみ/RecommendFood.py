#!C:\Users\kimur\anaconda3\python.exe

# -*- coding: utf-8 -*-
print("Content-Type: text/html\n")

def RecommendFood(userName):
    import csv
    import random
    
    VegetarianTypeFilePath = "Excel/type.csv"

    with open(VegetarianTypeFilePath, 'r', encoding = "utf-8")as f:
        csvreader = csv.reader(f)
        vegetarianType = [row for row in csvreader]
        f.close()
        
    Type = "vegan"
    i = 0
    userName = str(userName)
    print(userName)
    for tp in vegetarianType:
        print(vegetarianType[i][0])
        print()
        if (userName == vegetarianType[i][0]):
            Type = str(vegetarianType[i][1])
            print("一致")
        i += 1
  
    vegeType = ""
    
    if (Type == "vegan"):
        vegeType = "ヴィーガン"
        FoodListFilePath = "Excel/eiyoso/vegan.csv"
    if (Type == "fruitarian"):
        vegeType = "フルータリアン"
        FoodListFilePath = "Excel/eiyoso/flu-.csv"
    if (Type == "oriental_vegetarian"):
        vegeType = "オリエンタル・ベジタリアン"
        FoodListFilePath = "Excel/eiyoso/oriental.csv"
    if (Type == "lacto_vegetarian"):
        vegeType = "ラクト・ベジタリアン"
        FoodListFilePath = "Excel/eiyoso/rakuto.csv"
    if (Type == "ovo_vegetarian"):
        vegeType = "オボ・ベジタリアン"
        FoodListFilePath = "Excel/eiyoso/obo.csv"
    if (Type == "lacto_ovo_vegetarian"):
        vegeType = "ラクト・オボベジタリアン"
        FoodListFilePath = "Excel/eiyoso/rakuto_obo.csv"
    if (Type == "pescetarian"):
        vegeType = "ペスコ・タリアン"
        FoodListFilePath = "Excel/eiyoso/pesuki.csv"
    if (Type =="pollo_vegetarian"):
        vegeType = "セミ・ベジタリアン"
        FoodListFilePath = "Excel/eiyoso/poyo.csv"
    
    #食材名と栄養素が入ったCSVを読み込み（CSVはベジタリアンの種類によって変える予定）
    with open(FoodListFilePath, 'r', encoding = "utf-8")as f:
        csvreader = csv.reader(f)
        FoodList = [row for row in csvreader]
        f.close()
        
        
    #-----------CSVから不足栄養素を読み込む----------------
    print("ユーザー名を入力してください<br>")
    #userName = input()
    #userName = "7420032"
    print(userName + "<br><br>")
    
    rows = []
    with open('Excel/LackNutrition.csv', 'r', encoding = "utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
        f.close()
    
    calorie = 0
    protein = 0
    lipid = 0
    carbohydrate = 0
    dietaryFiber = 0
    for row in rows:
        if (userName == row[0]):
            calorie = float(row[1])
            protein = float(row[2])
            lipid = float(row[3])
            carbohydrate = float(row[4])
            dietaryFiber = float(row[5])
        

    #-----------必要に応じてこの数値を変える-----------
    firstFoodNumber = 0 #最初にランダムに選ぶ食材の数
    minimumNutritionRatio = 10 #追加食材の最低限の栄養の割合
    #追加する食材は、必要栄養素　/ minimumNutritionRatio　以上の栄養を持つものにする
    #例. カロリーが不足している場合、(2650 + calorie) / minimumNutritionRatio 以上のカロリーを持つ食材を選ぶ

    #オススメする食材の名前を格納する配列
    recommendFoodList = []
    recFoodNutList = []
    NutList = []
    listNum = 0

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
        [0, 5], #カロリー エクセルで6列目、Pythonで5
        [0, 8], #タンパク質 エクセルで9列目、Pythonで8
        [0, 10], #脂質 エクセルで11列目、Pythonで10
        [0, 16], #炭水化物 エクセルで17列目、Pythonで16
        [0, 20] #食物繊維 エクセルで21列目、Pythonで20
    ]

    #18~29歳男性の、必要な栄養素
    #https://www.glico.com/jp/navi/e07.html
    #ここの値に不足している栄養素を足す
    needNutritionList = [
        calorie, #カロリー
        protein, #タンパク質
        lipid, #脂質　総カロリー * 0.25 / 9
        carbohydrate, #炭水化物　総カロリー * 0.575 / 4
        dietaryFiber #食物繊維
    ]
    needNutritionList2 = [
        calorie, #カロリー
        protein, #タンパク質
        lipid, #脂質　総カロリー * 0.25 / 9
        carbohydrate, #炭水化物　総カロリー * 0.575 / 4
        dietaryFiber #食物繊維
    ]

    #各栄養素があとどのくらい不足しているかを格納する配列
    #ここでは配列を宣言してるだけで値は関係ない
    missingNutritionList = [0] * len(nutritionList)
    
    #不足している栄養素はnutritionList配列の何番かを格納する配列
    missingArrayNumberList = [0] * len(nutritionList)

    #ランダムでfirstFoodNumber回選んだ食材の名前と栄養素を格納する
    #print("※※※※※※※オススメ食材表示※※※※※※※")
    for i in range(firstFoodNumber):
        nutritions = ""
        rand = random.randint(1, len(FoodList) - 1) #エクセルの食材の最初（１行目は除く）から最後の間でランダムに１つ選ぶ
    
        #選んだ食材の各栄養素を足していく
        for j in range(len(nutritionList)):
            arrayNumber = nutritionList[j][1]
            nutritionList[j][0] += float(FoodList[rand][arrayNumber])
            NutList.append(float(FoodList[rand][arrayNumber]))
            nutritions += nutritionNameList[j] + ":" + str(FoodList[rand][arrayNumber]) + ", "
        
        recFoodNutList.append(NutList)
        NutList = []
        
        #選んだ食材名をオススメ食材リストに加える
        recommendFoodList.append(FoodList[rand][3])
        listNum += 1
        #print(FoodList[rand][3])
        #print(nutritions)
        #print()
    
    #print("----------必要栄養素----------")
    #for i in range(len(nutritionList)):
    #    print(nutritionNameList[i] + " : " + str(needNutritionList[i]))

    #print("----------合計栄養素----------")
    for i in range(len(nutritionList)):
        nutritionList[i][0] = round(nutritionList[i][0], 1) #小数第一位で丸める
        #print(nutritionNameList[i] + " : " + str(nutritionList[i][0]))
    
    #print("----------不足栄養素----------")
    missingCount = 0
    for i in range(len(nutritionList)):
        missingNutritionList[i] = needNutritionList[i] - nutritionList[i][0] #必要栄養素から合計栄養素を引く
        missingNutritionList[i] = round(max(missingNutritionList[i] , 0), 1) #小数第一位で丸める
        #missingNutritionList[i]が０より多いなら、その栄養素は不足している
        if (missingNutritionList[i] > 0):
            missingArrayNumberList[missingCount] = i
            missingCount += 1;
        #print(str(missingNutritionList[i]) + "　　　"  +nutritionNameList[i])

    #print("------------------------------")
    #print ("不足している栄養素数：" + str(missingCount))


    #不足している栄養素に応じて新しい食材を選ぶ
    #不足している栄養素が０になるまで繰り返す
    repeatCount = 0
    while missingCount > 0:
        repeatCount += 1
        #print()
        #print()
        #print("※※※※※※※" + str(repeatCount) + "回目　追加食材表示※※※※※※※")
        
        #不足している栄養素の数だけ繰り返す
        for i in range(missingCount):
            arrayNumber1 = nutritionList[missingArrayNumberList[i]][1]
            minimum = needNutritionList2[missingArrayNumberList[i]] / minimumNutritionRatio
            nutritions = ""
            rand = random.randint(1, len(FoodList) - 1)
            
            #不足している各栄養素の最低ライン（minimum)以上の食材を選ぶまで、ランダムで選び直す
            while float(FoodList[rand][arrayNumber1]) < minimum:
                rand = random.randint(1, len(FoodList) - 1)
            #選んだ食材の各栄養素を足していく
            print(FoodList[rand][arrayNumber1])
            print(minimum)
            for j in range(len(nutritionList)):
                arrayNumber2 = nutritionList[j][1]
                nutritionList[j][0] += float(FoodList[rand][arrayNumber2])
                NutList.append(float(FoodList[rand][arrayNumber2]))
                nutritions += nutritionNameList[j] + str(FoodList[rand][arrayNumber2]) + ", "
        
            recFoodNutList.append(NutList)
            NutList = []
            #選んだ食材名をオススメ食材リストに加える
            recommendFoodList.append(FoodList[rand][3])
            listNum += 1
            #print(FoodList[rand][3])
            #print(nutritions)
            #print()
    
        #print("----------必要栄養素----------")
        #for i in range(len(nutritionList)):
            #print(nutritionNameList[i] + " : " + str(needNutritionList[i]))
    
        #print("----------" + str(repeatCount) + "回目　追加後の合計栄養素----------")
        for i in range(len(nutritionList)):
            nutritionList[i][0] = round(nutritionList[i][0], 1) #小数第一位で丸める
            #print(nutritionNameList[i] + " : " +  str(nutritionList[i][0]))

        #print("----------" + str(repeatCount) + "回目　追加後の不足栄養素----------")
        missingCount = 0
        for i in range(len(nutritionList)):
            missingNutritionList[i] = needNutritionList[i] - nutritionList[i][0] #必要栄養素から合計栄養素を引く
            missingNutritionList[i] = round(max(missingNutritionList[i] , 0), 1) #小数第一で丸める
            #missingNutritionList[i]が０より多いなら、その栄養素は不足している
            if (missingNutritionList[i] > 0):
                missingArrayNumberList[missingCount] = i
                missingCount += 1;
            #print(nutritionNameList[i] + " : "  + str(missingNutritionList[i]))

        #print("------------------------------")
        #print (str(repeatCount) + "回目　不足している栄養素数：" + str(missingCount))
        #不足している栄養素数が０になったら実行終了
        #print()
        
    print("タイプ：" + Type + "<br><br>")
    print()
    print("※※※※※※※※※※オススメ食材表示※※※※※※※※※※<br>")
    
    sumCal = 0
    sumPro = 0
    sumLip = 0
    sumCar = 0
    sumDie = 0
    #オススメ食材リストを返す
    for i in range(len(recommendFoodList)):
        print(recommendFoodList[i] + "<br>")
        nutritions = ""
        
        sumCal += recFoodNutList[i][0]
        sumPro += recFoodNutList[i][1]
        sumLip += recFoodNutList[i][2]
        sumCar += recFoodNutList[i][3]
        sumDie += recFoodNutList[i][4]
        for j in range(len(nutritionList)):
            nutritions += nutritionNameList[j] + ":" + str(recFoodNutList[i][j]) + ", "
        
        print(nutritions + "<br><br>")
        print()
    
    sumCal = round(sumCal,1)
    sumPro = round(sumPro,1)
    sumLip = round(sumLip,1)
    sumCar = round(sumCar,1)
    sumDie = round(sumDie,1)
    print()
    print("----------不足栄養素----------<br>")
    print("カロリー:" + str(calorie) + ", タンパク質:" + str(protein) + ", 脂質:" + str(lipid) + ", 炭水化物:" + str(carbohydrate)  +", 食物繊維:" + str(dietaryFiber))
    print()
    print("<br>----------必要栄養素----------<br>")
    print("カロリー:" + str(needNutritionList[0]) + ", タンパク質:" + str(needNutritionList[1]) + ", 脂質:" + str(needNutritionList[2]) + ", 炭水化物:" + str(needNutritionList[3])  +", 食物繊維:" + str(needNutritionList[4]))
    print()
    print("<br>----------合計栄養素----------<br>")
    print("カロリー:" + str(sumCal) + ", タンパク質:" + str(sumPro) + ", 脂質:" + str(sumLip) + ", 炭水化物:" + str(sumCar)  +", 食物繊維:" + str(sumDie))
    
    lack = []
    need = []
    sum = []
    lack.append(calorie)
    lack.append(protein)
    lack.append(lipid)
    lack.append(carbohydrate)
    lack.append(dietaryFiber)
    need.append(round(needNutritionList[0],1))
    need.append(round(needNutritionList[1],1))
    need.append(round(needNutritionList[2],1))
    need.append(round(needNutritionList[3],1))
    need.append(round(needNutritionList[4],1))
    sum.append(sumCal)
    sum.append(sumPro)
    sum.append(sumLip)
    sum.append(sumCar)
    sum.append(sumDie)
    return recommendFoodList,recFoodNutList,lack,need,sum,vegeType