from flask import Flask, request

app = Flask(__name__)

@app.route("/") ### MAIN PAGE
def mainpage():
    return f"""
        <html>
            <head>
                <title>Main Page</title>
            </head>
            <body>
                <div style='width: 600; height: 215; border: 1px solid #000000; border-radius: 5px; padding: 35; position: absolute; top:25%; left:27%;'>
                    <center>
                        <font size=7><b>WELCOME TO OUR SITE</b></font>
                        </br></br></br>
            
                        <font size=6><b>PLEASE LOG IN</b></font>
                        </br></br>
            
                        <form action="/loginsuccess" method="post">
                        <b>ID:</b> &nbsp;
                        <input type="text" name="id"> 
                        &nbsp;&nbsp;&nbsp;&nbsp;
                        <b>PASSWORD:</b> &nbsp;
                        <input type="text" name="password"><br><br>
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
                                <td><input type="text" name="password"></td>
                            </tr>
                        </table>
                        </br>
                        <input type="reset" value="Reset">
                        <input type="submit" value="Register">
                        </form> 
                    </center>
                </div>
            </body>
        </html>
    """

@app.route("/loginsuccess", methods=['POST'])
def loginsuccesspage():
    id = request.form['id']
    password = request.form['password']
    return f"""
    <html>
        <head>
            <title>Main Page</title>
        </head>
        <body>
            <center>
                <font size=7><b>WELCOME {id}, {password}</b></font>
            </center>
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run()


