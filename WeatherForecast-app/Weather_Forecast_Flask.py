from flask import Flask, render_template, request, send_from_directory
from Weather_Forecast_BackEnd import *
from _socket import gethostname
import logging

app = Flask(__name__)

logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bkg_color = "blue"

@app.route('/', methods=["GET", "POST"])
def home_page():
    data = None
    host = gethostname()
    if request.method == "POST":
        data, location_name, location_country = convert_location_to_forecast(request.form.get("location_input"))

        if location_country:
            logging.info(location_name)
            save_history(data, location_name, location_country)
            return render_template("Weather_Forecast.html", data=data, location=location_name,
                                   country=location_country, host=host)
        else:
            logging.error(request.form.get("location_input"))
            return render_template("Weather_Forecast.html", data=data, location=location_name,
                                   country=location_country, host=host)

    return render_template("Weather_Forecast.html", data=data, host=host, BG_COLOR=bkg_color)


@app.route("/download")
def download():
    return download_image()


@app.route("/dynamodb", methods=['POST'])
def dynamodb():
    data, location_name, location_country = convert_location_to_forecast(request.form.get("location_input"))
    return dynamodb_send_item(data, location_name)

@app.route('/history')
def history():
    history_files = get_history_files()
    return render_template('history.html', history_files=history_files)

@app.route('/download/history/<path:filename>')
def download_history(filename):
    directory = 'history'
    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
