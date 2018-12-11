from process_data import task3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def part2():
    return render_template("part2.html")


@app.route("/", methods=["POST"])
def index_post():
    name = request.form["name"]
    news_list = task3(name)
    news1=news_list[0]
    news2=news_list[1]
    news3=news_list[2]
    news4=news_list[3]
    news5=news_list[4]
    return render_template("part2.html", news1=news1, news2=news2, news3=news3, news4=news4, news5=news5)


if __name__=="__main__":
    app.run(debug=True)