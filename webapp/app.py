from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def calculate_portions(portion_start_grams, portion_end_grams, start_date, end_date):
    days = (end_date - start_date).days + 1
    step = (portion_end_grams - portion_start_grams) / (days - 1)
    values = [round(portion_start_grams + i * step) for i in range(days)]
    date_list = [(start_date + timedelta(days=i)) for i in range(days)]
    results = []
    for idx, val in enumerate(values):
        row_date = date_list[idx]
        date_str = row_date.strftime("%d-%m-%Y")
        found = False
        for x in range(5, val//2 + 1, 5):
            y = val - 2*x
            if abs(x - y) <= 10:
                if x > y:
                    morning = x
                    noon = y
                    evening = x
                else:
                    morning = x
                    noon = x
                    evening = y
                results.append({
                    "date": date_str,
                    "value": val,
                    "morning": morning,
                    "noon": noon,
                    "evening": evening,
                    "weekday": row_date.strftime("%A")
                })
                found = True
                break
        if not found:
            results.append({
                "date": date_str,
                "value": val,
                "morning": "-",
                "noon": "-",
                "evening": "-",
                "weekday": row_date.strftime("%A")
            })
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    highlight = None
    if request.method == 'POST':
        try:
            portion_start_grams = int(request.form.get('portion_start_grams', 0))
            portion_end_grams = int(request.form.get('portion_end_grams', 0))
            start_date = datetime.strptime(request.form.get('start_date'), "%Y-%m-%d")
            end_date = datetime.strptime(request.form.get('end_date'), "%Y-%m-%d")
            highlight = request.form.get('highlight_weekday')
        except Exception:
            error = "Please enter valid numbers and dates."
            return render_template('index.html', result=None, error=error, weekdays=WEEKDAYS)
        if end_date <= start_date:
            error = "End date must be after start date."
        else:
            days = (end_date - start_date).days + 1
            if days < 2:
                error = "Date range must be at least 2 days."
            else:
                result = calculate_portions(portion_start_grams, portion_end_grams, start_date, end_date)
    return render_template('index.html', result=result, error=error, weekdays=WEEKDAYS, highlight=highlight)

if __name__ == '__main__':
    app.run(debug=True)
