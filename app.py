from flask import Flask, request, render_template, url_for

app = Flask(__name__)


def countries_name(x):
    if x == 'Spain': return 'ES1'
    if x == 'France': return 'FR1'
    if x == 'England': return 'GB1'
    if x == 'Greece': return 'GR1'
    if x == 'Italy': return 'IT1'
    if x == 'Germany': return 'L1'
    if x == 'Russia': return 'RU1'
    return 'Options: Spain France England Greece Italy Germany Russia'


@app.route('/', methods=["GET", "POST"])
def check():
    if request.method == 'POST':
        query = request.form['our_params']
        ans = countries_name(query)
        if ans != 'Options: Spain France England Greece Italy Germany Russia':
            return render_template(f'{ans}.html', result=query)
        else:
            return render_template('home.html')
    else:
        return render_template('home.html')


@app.route('/ES1', methods=["GET", "POST"])
def es1():
    if request.method == 'POST':
        query = request.form['our_params']
        ans = countries_name(query)
        if ans != 'options: Spain France England Greece Italy Germany Russia':
            return render_template(f'{ans}.html', result=query)
        else:
            return render_template('home.html')
    else:
        return render_template('ES1.html')


@app.route('/FR1', methods=["GET", "POST"])
def fr1():
    if request.method == 'POST':
        query = request.form['our_params']
        ans = countries_name(query)
        if ans != 'options: Spain France England Greece Italy Germany Russia':
            return render_template(f'{ans}.html', result=query)
        else:
            return render_template('home.html')
    else:
        return render_template('FR1.html')


@app.route('/GB1', methods=["GET", "POST"])
def gb1():
    if request.method == 'POST':
        query = request.form['our_params']
        ans = countries_name(query)
        if ans != 'options: Spain France England Greece Italy Germany Russia':
            return render_template(f'{ans}.html', result=query)
        else:
            return render_template('home.html')
    else:
        return render_template('GB1.html')


@app.route('/GR1', methods=["GET", "POST"])
def gr1():
    if request.method == 'POST':
        query = request.form['our_params']
        ans = countries_name(query)
        if ans != 'options: Spain France England Greece Italy Germany Russia':
            return render_template(f'{ans}.html', result=query)
        else:
            return render_template('home.html')
    else:
        return render_template('GR1.html')


@app.route('/IT1', methods=["GET", "POST"])
def it1():
    if request.method == 'POST':
        query = request.form['our_params']
        ans = countries_name(query)
        if ans != 'options: Spain France England Greece Italy Germany Russia':
            return render_template(f'{ans}.html', result=query)
        else:
            return render_template('home.html')
    else:
        return render_template('IT1.html')


@app.route('/RU1', methods=["GET", "POST"])
def ru1():
    if request.method == 'POST':
        query = request.form['our_params']
        ans = countries_name(query)
        if ans != 'options: Spain France England Greece Italy Germany Russia':
            return render_template(f'{ans}.html', result=query)
        else:
            return render_template('home.html')
    else:
        return render_template('RU1.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4708)
