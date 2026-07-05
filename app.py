import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RestrictBot Server</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                background: radial-gradient(circle, #0f172a, #020617);
                color: #e2e8f0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                padding: 40px;
                border-radius: 16px;
                background: rgba(30, 41, 59, 0.7);
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
                background: linear-gradient(to right, #38bdf8, #818cf8);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            p {
                color: #94a3b8;
                font-size: 1.1rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Study Bot Server is Active ⚝</h1>
            <p>Powered by 𝗖𝗛𝗢𝗦𝗘𝗡 𝗢𝗡Ｅ ⚝</p>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    # Default to port 5000 if PORT is not set in the environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
