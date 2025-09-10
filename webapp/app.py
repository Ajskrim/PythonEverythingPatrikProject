def calculate_portions(portion_start_grams, portion_end_grams, start_date, duration_months):
    year = start_date.year
    month = start_date.month + duration_months
    day = start_date.day
    while month > 12:
        year += 1
        month -= 12
    from calendar import monthrange
    last_day = monthrange(year, month)[1]
    end_day = min(day, last_day)
    end_date = datetime(year, month, end_day)
    days = (end_date - start_date).days + 1
    step = (portion_end_grams - portion_start_grams) / (days - 1) if days > 1 else 0
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
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import os

app = Flask(__name__)

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No image uploaded", 400
    image = request.files['image']
    if image.filename == '':
        return "No selected file", 400
    # Save image to uploads folder
    upload_folder = os.path.join(os.path.dirname(__file__), 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    image_path = os.path.join(upload_folder, image.filename)
    image.save(image_path)
    return f"Image uploaded: {image.filename}", 200
    # Calculate end date by adding exact months
    year = start_date.year
    month = start_date.month + duration_months
    day = start_date.day
    while month > 12:
        year += 1
        month -= 12
    # If the day does not exist in the target month, use last day of that month
    from calendar import monthrange
    last_day = monthrange(year, month)[1]
    end_day = min(day, last_day)
    end_date = datetime(year, month, end_day)
    days = (end_date - start_date).days + 1
    step = (portion_end_grams - portion_start_grams) / (days - 1) if days > 1 else 0
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
            duration_months = int(request.form.get('duration_months', 1))
            highlight = request.form.get('highlight_weekday')
            if duration_months < 1 or duration_months > 12:
                error = "Duration must be between 1 and 12 months."
            else:
                result = calculate_portions(portion_start_grams, portion_end_grams, start_date, duration_months)
        except Exception:
            error = "Please enter valid numbers, start date, and duration."
            return render_template('index.html', result=None, error=error, weekdays=WEEKDAYS)
    return render_template('index.html', result=result, error=error, weekdays=WEEKDAYS, highlight=highlight)

if __name__ == '__main__':
    app.run(debug=True)
