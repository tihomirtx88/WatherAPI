from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__);

stations = pd.read_csv("data/stations.txt", skiprows=17);
stations = stations[["STAID", "STANAME                                 "]];

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    if request.method == "POST":
        station = request.form.get("station")
        date = request.form.get("date")

        if not station or not date:
            error = "Please provide both station and date."
        else:
            try:
                filename = "data/TG_STAID" + str(station).zfill(6) + ".txt"
                df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
                df.columns = df.columns.str.strip()

                temperature_series = df.loc[df['DATE'] == date, 'TG']

                if temperature_series.empty:
                    error = "No temperature data found for this date."
                else:
                    temperature = temperature_series.squeeze() / 10
                    result = {
                        "station": station,
                        "date": date,
                        "temperature": temperature
                    }

            except FileNotFoundError:
                error = f"No data file found for station {station}."
            except Exception as e:
                error = f"An error occurred: {str(e)}"

    return render_template("home.html", result=result, error=error, data=stations.to_html())

if __name__ == "__main__":
    app.run(debug=True)