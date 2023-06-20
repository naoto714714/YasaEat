# -*- coding: utf-8 -*-
from flask import Flask,render_template,redirect,url_for,request
import csv
app = Flask(__name__)
 
@app.route('/', methods=['GET', 'POST'])
def login():
    # ２回目以降データが送られてきた時の処理です
    if request.method == 'POST':
        id = request.form['id']
        userList = []
        userList.append(id)
        userList.append(0)
        print(userList)
        with open('templates/login.csv', 'a', newline="", encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(userList)
                f.close()
        return redirect('/loginCheck')
    # １回目のデータが何も送られてこなかった時の処理です。
    else:
        return render_template('login_form.html')

@app.route('/loginCheck')
def loginCheck():
    return render_template('login.csv')

@app.route('/signup')
def signup():
    return render_template('sign_up.html')

@app.route('/AllFoodList')
def foodlist():
    return render_template('AllFoodList.csv')

@app.route('/home/<user_id>', methods=['GET', 'POST'])
def home(user_id):
    if request.method == 'POST':
        inq = request.form['num_of_inq']
        userList = [user_id, inq]
        rows = []
        with open('Excel/type.csv', 'r', encoding = "utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
            f.close()
    
        changeRow = -1
        i = 0
        for row in rows:
            if (user_id == row[0]):
                changeRow = i
            i += 1
            
        if (changeRow == -1):
            with open('Excel/type.csv', 'a', newline="", encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(userList)
                f.close()
        
        else:
            i = 0
            with open('Excel/type.csv', 'w', newline="", encoding='utf-8') as f:
                writer = csv.writer(f)
                for data in rows:
                    if i == changeRow:
                        writer.writerow(userList)
                    else:
                        writer.writerow(data)
                    i += 1
                f.close()
        return render_template('home.html', user_id = user_id)
    
    else:
        return render_template('home.html', user_id = user_id)

@app.route('/home/choice/<user_id>', methods=['GET', 'POST'])
def choise(user_id):
    # ２回目以降データが送られてきた時の処理です
    if request.method == 'POST':
        inq = request.form['num_of_inq']
        userList = [user_id, inq]
        rows = []
        with open('Excel/type.csv', 'r', encoding = "utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
            f.close()
    
        changeRow = -1
        i = 0
        for row in rows:
            if (user_id == row[0]):
                changeRow = i
            i += 1
            
        if (changeRow == -1):
            with open('Excel/type.csv', 'a', newline="", encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(userList)
                f.close()
        
        else:
            i = 0
            with open('Excel/type.csv', 'w', newline="", encoding='utf-8') as f:
                writer = csv.writer(f)
                for data in rows:
                    if i == changeRow:
                        writer.writerow(userList)
                    else:
                        writer.writerow(data)
                    i += 1
                f.close()
        return render_template('choice.html', user_id = user_id)
    # １回目のデータが何も送られてこなかった時の処理です。
    else:
        return render_template('choice.html', user_id = user_id)

@app.route('/home/food_form/<user_id>', methods=['GET', 'POST'])
def food_form(user_id):
    if request.method == 'POST':
        inq = request.form['user_id']
        date = request.form['date']
        food = request.form['food']
        amount = request.form['amount']
        cal = request.form['cal']
        pro = request.form['pro']
        lip = request.form['lip']
        car = request.form['car']
        dieF = request.form['dieF']
        userList=[]
        userList.append(inq)
        userList.append(date)
        userList.append(food)
        userList.append(amount)
        userList.append(cal)
        userList.append(pro)
        userList.append(lip)
        userList.append(car)
        userList.append(dieF)
        with open('Excel/DietHistory.csv', 'a', newline="", encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(userList)
                f.close()
        return render_template('newfood_form.html', user_id = user_id)
    else:
        return render_template('newfood_form.html', user_id = user_id)

@app.route('/home/calc_form/<user_id>', methods=['GET', 'POST'])
def calc_form(user_id):
    return render_template('calculate_form.html', user_id = user_id)

@app.route('/home/CalclulateAteNutrition', methods=['GET', 'POST'])

def calc():
    user_id=request.form["user_id"]
    day=request.form["day"]
    from CalclulateAteNutrition import CalclulateAteNutrition
    calc = CalclulateAteNutrition(user_id, day)
    missing = calc[0]
    ate = calc[1]
    amount = calc[2]
    need = calc[3]
    sum = calc[4]
    return render_template('calculate.html', user_id = user_id, missing= missing, ate = ate, amount = amount, need = need, sum = sum)

@app.route('/home/RecommendFood/<user_id>', methods=['GET', 'POST'])
def reco(user_id):
    if request.method == 'POST':
        #inq = request.form['user_id']
        #date = request.form['date']
        #print(inq)
        #print("インク")
        #print(date)
        print("日付")
    else:
        from RecommendFood import RecommendFood
        recommendFoods = RecommendFood(user_id)
        foodName = recommendFoods[0]
        nutList = recommendFoods[1]
        lack = recommendFoods[2]
        need = recommendFoods[3]
        sum = recommendFoods[4]
        vegeType = recommendFoods[5]
        return render_template('recommend.html', user_id = user_id, food = foodName, nut = nutList, lack = lack, need = need, sum = sum, vegeType = vegeType)


if __name__ == "__main__":
    #app.run('0.0.0.0',port=5000,debug=True)
    app.run(debug=True)