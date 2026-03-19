from flask import Flask, render_template, request
import requests, os

app = Flask(__name__)
API_KEY = os.getenv("REMOVE_BG_API_KEY")

@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="POST":
        file = request.files["image"]

        res = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            files={"image_file": file},
            data={"size":"auto"},
            headers={"X-Api-Key": API_KEY}
        )

        if res.status_code==200:
            path="static/output.png"
            with open(path,"wb") as f:
                f.write(res.content)
            return render_template("index.html", result=True, img=path)
        else:
            return "API Error"

    return render_template("index.html", result=False)

if __name__=="__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)