from flask import Flask, render_template, request, redirect, session
from helpers import task_helper
from chat import talk_to_ai, save_memory, load_full_memory

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# In-memory user profiles for demo
user_profiles = {}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        if username in user_profiles:
            session["username"] = username
            return redirect("/chat")
        else:
            return redirect(f"/create_profile/{username}")
    return render_template("login.html")

@app.route("/create_profile/<username>", methods=["GET", "POST"])
def create_profile(username):
    if request.method == "POST":
        profile = {
            "name": request.form["name"],
            "age": request.form["age"],
            "interests": request.form["interests"],
            "favorite_foods": request.form["favorite_foods"],
            "goals": request.form["goals"],
        }
        user_profiles[username] = profile
        session["username"] = username
        return redirect("/chat")
    return render_template("create_profile.html", username=username)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    profile = user_profiles.get(username)   
    if not profile:
        return redirect(f"/create_profile/{username}")

    response = None
    user_input = None

    if request.method == "POST":
        if "user_input" in request.form:
            user_input = request.form["user_input"]
            response = talk_to_ai(user_input, profile)
            save_memory(username, user_input, response)

        elif "task_type" in request.form:
            task_type = request.form["task_type"]
            response = task_helper(task_type, "")
            user_input = f"Quick help requested: {task_type}"
            save_memory(username, user_input, response)

    conversation_history = load_full_memory(username)

    return render_template(
        "chat.html",
        username=username,
        user_input=user_input,
        ai_response=response,
        conversation=conversation_history,
    )

@app.route("/")
def index():
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
