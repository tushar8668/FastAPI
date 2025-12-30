from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

users_db = []

class User(BaseModel):
    name: str
    email: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Create User</title>
    </head>
    <body>
        <h2>Create User</h2>
        <input id="name" placeholder="Name"><br><br>
        <input id="email" placeholder="Email"><br><br>
        <button onclick="createUser()">Create</button>

        <script>
        async function createUser() {
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;

            const response = await fetch('/users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: name, email: email })
            });

            const data = await response.json();
            alert(JSON.stringify(data));
        }
        </script>
    </body>
    </html>
    """

@app.post("/users")
def create_user(user: User):
    users_db.append(user)
    return {"message": "User created", "user": user}

@app.get("/users")
def get_users():
    return users_db
