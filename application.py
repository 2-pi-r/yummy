from flask import Flask, render_template, request, redirect, url_for, flash
from database import DBhandler
import sys
application = Flask(__name__)
application.config["SECRET_KEY"] = "yummy"
app = Flask(__name__)
app.config["SECRET_KEY"] = "yummy"

DB = DBhandler()


# route: 시작 페이지
@application.route("/")
def hello():
    # return render_template("list.html")
    return redirect(url_for("view_list", page=0))


# route: 맛집 리스트    
@application.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int) # 페이지 인덱스
    limit = 9 # 한 페이지에 식당 최대 9개
    
    start_idx = limit * page # 이 페이지의 식당 인덱스 (시작)
    end_idx = limit * (page + 1) # 이 페이지의 식당 인덱스 (끝)
    
    data = DB.get_restaurants()
    
    if data == "None": # 예외 처리 : DB에 등록된 맛집이 하나도 없는 상황
        flash("등록된 맛집이 없습니다. 당신의 맛집을 공유해주세요.")
        return redirect(url_for('view_restaurantRegister'))
        
    total_count = len(data) # 레스토랑 총 개수
    page_count = int(((total_count + 8)/ limit)) # 페이지 총 개수
    data = dict(list(data.items())[start_idx:end_idx])

    # print (data)    
    return render_template("list.html", page=page, limit=limit, page_count=page_count, total_count=total_count, datas=data.items())


# route: 맛집 등록
@application.route("/restaurantRegister")
def view_restaurantRegister():
    return render_template("restaurantRegister.html")


# route: 메뉴 등록
@application.route("/menuRegister", methods=['POST'])
def reg_menu():
    data=request.form
    print(data)
    return render_template("menuRegister.html", data=data)


# route: 리뷰 등록
@application.route("/reviewRegister", methods=['POST'])
def view_reviewRegister():
    data=request.form
    return render_template("reviewRegister.html", data=data)


# route: 점메추/저메추
@application.route("/worldCup")
def view_worldCup():
    return render_template("worldCup.html")


# 메뉴/맛집/리뷰 등록 과정에서 DB 받아오는 중간 페이지 (3개)
# 메뉴 등록 과정에서
@application.route("/menuSubmit", methods=['POST'])
def view_menuSubmit():
    global idx
    image_file=request.files["file"]
    image_file.save("./static/image/{}".format(image_file.filename))
    data=request.form
    
    if DB.insert_menu(data['foodname'], data, image_file.filename):
        return render_template("menuResult.html", data=data, image_path="static/image/"+image_file.filename)
    else:
        return "Menu name is already exist."
    
    
# 맛집 등록 과정에서
@application.route("/restaurantSubmit", methods=['POST'])
def view_restaurantSubmit():
    global idx
    image_file=request.files["file"]
    image_file.save("./static/image/{}".format(image_file.filename))
    data=request.form
    
    if DB.insert_restaurant(data, data, image_file.filename):
        return render_template("result.html", data=data, image_path="static/image/"+image_file.filename) 
    else:
        return "Restaurant name already exist!"


# 리뷰 등록 과정에서
@application.route("/reviewSubmit", methods=['POST'])
def view_reviewSubmit():
    image_file=request.files["img"]
    image_file.save("./static/image/{}".format(image_file.filename))
    data=request.form
    
    if DB.insert_review(data['reviewerName'], data, image_file.filename):
        return render_template("reviewResult.html", data=data, image_path="static/image/"+image_file.filename)
    else:
        return "Enter the review!"


# 동적 라우팅
# 각 식당의 경로로 페이지가 라우팅 되도록 필요한 페이지.
@app.route('/dynamicurl/<variable_name>')
def DynamicUrl(variable_name):
    return str(variable_name)


# route: 맛집 상세페이지
@application.route("/view_detail/<name>/")
def view_restaurant_detail(name):
    data = DB.get_restaurant_byname(str(name))
    avg_rate = DB.get_avgrate_byname(str(name))
    
    if data == "None": # 예외 처리 : DB에 등록된 맛집이 하나도 없는 상황
        flash("등록된 맛집이 없습니다. 당신의 맛집을 공유해주세요.")
        return redirect(url_for('view_restaurantRegister'))

    
    # print("####data:", data)
    return render_template("detail.html", data=data, avg_rate = avg_rate)
  
    
# route : 메뉴 조회
@application.route("/list_foods/<name>/")
def view_foods(name):
    data = DB.get_food_byname(str(name))
  #  #tot_count = len(data)
   # #page_count = len(data)sss
    data = {i : data[i] for i in range(len(data))}
    print (data)
    return render_template("menuView.html", datas=data.items())


# route : 리뷰 조회
@application.route("/view_reviewVView/<name>/")
def view_reviewVView(name):
    #avg_rate = DB.get_avgrate_byname(str(name))
    data = DB.get_review_byname(str(name))
    data = {i : data[i] for i in range(len(data))}
    
    # print( data)
    return render_template("reviewView.html", datas=data.items())


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
