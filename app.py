from flask import Flask, render_template, request
from main import main as run_analysis
from db import get_history, get_history_detail

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    page = int(request.args.get("page", 1))
    date_filter = request.args.get("date_filter")
    offset = (page - 1) * 5

    if request.method == "POST":
        stock = request.form.get("stock")
        if stock:
            result = run_analysis(stock, return_result=True)  # proses dan dapatkan hasil

    # Ambil riwayat selalu (baik GET/POST)
    history, has_next = get_history(limit=5, offset=offset, date_filter=date_filter)

    return render_template("index.html", result=result, history=history, page=page, date_filter=date_filter, has_next=has_next)




@app.route("/detail/<int:caller_id>")
def detail(caller_id):
    data = get_history_detail(caller_id)
    if not data["summary"]:
        return "Data tidak ditemukan", 404
    return render_template("detail.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
