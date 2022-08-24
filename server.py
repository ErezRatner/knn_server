from flask import Flask, request, render_template
import pymongo, numpy as np, cv2
from PIL import Image
from knn import Knn, load_model

uri = "mongodb://localhost:27017/"
myclient = pymongo.MongoClient(uri)
mydb = myclient["project_with_erez"] # CONNECT DATABASE IF NOT EXISTS CREATES ONE
users = mydb["users"] # CONNECT TO COLLECTION

app = Flask(__name__)

@app.route("/")
def loginpage():
    return f"""
        <html>
            <head>
                <title>Login Page</title>
            </head>
            <body>
                <div style='width: 600; height: 215; border: 1px solid #000000; border-radius: 5px; padding: 35; position: absolute; top:25%; left:27%;'>
                    <center>
                        <font size=7><b>WELCOME TO OUR SITE</b></font>
                        </br></br></br>
            
                        <font size=6><b>PLEASE LOG IN</b></font>
                        </br></br>
            
                        <form action="/mainpage" method="post">
                        <b>ID:</b> &nbsp;
                        <input type="text" name="id"> 
                        &nbsp;&nbsp;&nbsp;&nbsp;
                        <b>PASSWORD:</b> &nbsp;
                        <input type="password" name="password"><br><br>
                        <input type="button" onclick="location.href='/register'" value="Register">
                        <input type="reset" value="Reset">
                        <input type="submit" value="Submit">
                        </form> 
                    </center>
                </div>
            </body>
        </html>
    """

@app.route("/register")
def registerpage():
    return f"""
        <html>
            <head>
                <title>Register Page</title>
            </head>
            <body>
                <div style="width: 600; height: 240; border: 1px solid #000000; border-radius: 5px; padding: 35; position: absolute; top:25%; left:27%;">
                    <center>
                        <font size=7><b>REGISTER PAGE</b></font>
                        </br></br></br>
                        <form action="/registrationstatus" method="post">
                        <table>
                            <tr>
                                <td><b>FIRST NAME:</b></td>
                                <td><input type="text" name="fname"></td>
                            </tr>
                            <tr>
                                <td><b>LAST NAME:</b></td>
                                <td><input type="text" name="lname"></td>
                            </tr>
                            <tr>
                                <td><b>ID:</b></td>
                                <td><input type="text" name="id"></td>
                            </tr>
                            <tr>
                                <td><b>PASSWORD:</b></td>
                                <td><input type="password" name="password"></td>
                            </tr>
                        </table>
                        </br>
                        <input type="reset" value="Reset">
                        <input type="submit" value="Submit">
                        </form> 
                    </center>
                </div>
            </body>
        </html>
    """

@app.route("/registrationstatus", methods=['POST'])
def success():
    fname = request.form['fname'].title()
    lname = request.form['lname'].title()
    id = request.form['id']
    password = request.form['password']   

    if len(id)>0 and len(password)>0 and len(fname)>0 and len(lname)>0:
        user = users.find_one({"id":id})

        if user == None:
            users.insert_one({"id":id, "password":password, "first_name":fname, "last_name":lname})
            return """
                <html>
                    <head>
                        <title>Register Successed</title>
                    </head>
                    <body>
                        <center>
                            <font size=7><b>REGISTER SUCCESSED</b></font></br>
                        </center>
                        <script>
                            setTimeout(function(){window.location.href = '/'}, 2000);
                        </script>
                    </body>
                </html>
            """

        # USER ALLREADY EXISTS IN DB
        return """
            <html>
                <head>
                    <title>Register Failed</title>
                </head>
                <body>
                    <center>
                        <font size=7><b>REGISTER FAILED</b></font></br>
                        <font size=5><b>USERNAME ALLREADY EXISTS</b></font></br>
                    </center>
                    <script>
                        setTimeout(function(){window.location.href = '/register'}, 1500);
                    </script>
                </body>
            </html>
        """ 
    
@app.route("/mainpage", methods=['POST'])
def mainpage():
    id = request.form['id']
    password = request.form['password']
    
    user = users.find_one({"id":id, "password":password})

    if len(id)>0 and len(password)>0:
        # USER NOT EXISTS
        if user == None:
            return """
                <html>
                    <script>
                        setTimeout(function(){window.location.href = '/'}, 100);
                    </script>
                </html>        
            """

        return f"""
            <html>
                <head>
                    <title>Main Page</title>
                </head>
                <body>
                    <center>
                        <font size=7><b>WELCOME {user["first_name"]} {user["last_name"]}</b></font>
                        </br></br></br>
                        <font size=4><b>PLEASE CHOOSE PICTURE AND UPLOAD IT TO SERVER</b></font>
                        </br></br>
                        <form action="/photoprediction" method="post" enctype="multipart/form-data">
                            <label for="img">Select image:</label>
                            <input type="file" id="img" name="img" accept="image/*">
                            <input type="submit" style="width:100">
                        </form>
                    </center>
                </body>
            </html>
        """


@app.route("/photoprediction", methods=['GET', 'POST'])
def photoprediction():
    img = request.files['img']
    imgstr = request.files['img'].read()
    img_in_np = cv2.imdecode(np.fromstring(imgstr, np.uint8), cv2.IMREAD_GRAYSCALE)
    print(img_in_np.shape)

    knn = load_model("knn_server/knn")
    pred = knn.predict([img_in_np.reshape(28*28,)])

    # image = Image.fromarray(img_in_np, 'RGB')
    # image.show()

    return f"""
        <html>
            <head>
                <title>digit Prediction</title>
            </head>
            <body>
                <center>
                    <font size=7><b>PREDICTION IS </b></font>
                    </br></br></br>
                    <font size=6><b>{pred[0]}</b></font>

                </center>
            </body>
        </html>
    """
if __name__ == "__main__":
    app.run()


