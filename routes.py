from config import app
from controller_functions import index, loginPage, processLogin, registerPage, processUser, home, logout

app.add_url_rule("/", view_func=index)

app.add_url_rule("/login", view_func=loginPage)
app.add_url_rule("/process_login", view_func=processLogin, methods=["POST"])
app.add_url_rule("/register", view_func=registerPage)
app.add_url_rule("/process_user", view_func=processUser, methods=["POST"])

app.add_url_rule("/home", view_func=home)

app.add_url_rule("/logout", view_func=logout)