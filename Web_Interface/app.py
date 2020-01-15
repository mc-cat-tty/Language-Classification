import os
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import TextAreaField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from flask_table import Table, Col
from Modules.analyzer import LettersFreq, TestoLingua, FileLingua
from tempfile import TemporaryDirectory
from Modules.wikiquality import QualityEvaluator
from Modules.tweetrain import langs_R

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = os.urandom(20).hex()

LettersFreq.set_file("../Frequency_Tables/letters_frequency_twitter.csv")

class TextForm(FlaskForm):
    text = TextAreaField('Text to recognize: ', validators=[DataRequired()])
    submit = SubmitField('Analyze')

class StatTable(Table):
    parameter = Col('Parameter')
    value = Col('Value')
    no_items = ''
    classes = ['table', 'table-borderless', 'table-striped']
    thead_classes = ["table-primary"]

class StatItem(object):
    def __init__(self, parameter, value):
        self.parameter = parameter
        self.value = value

class LettersFreqTable(Table):
    letter = Col('Letter')
    freq = Col('Freq')
    thead_classes = ["table-info"]

class LettersFreqItem(object):
    def __init__(self, letter, freq):
        self.letter = letter
        self.freq = freq

class FileForm(FlaskForm):
    file = FileField('Choose a file...', validators=[FileRequired()])
    submit = SubmitField('Send')

class EvaluateForm(FlaskForm):
    pages_num = IntegerField("Number of Wikipedia's pages to use for evaluation", validators=[DataRequired()])
    submit = SubmitField("Evaluate")

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    text_form = TextForm()
    file_form = FileForm()
    if text_form.validate_on_submit() or file_form.validate_on_submit():
        if text_form.validate_on_submit():
            t = TestoLingua(text_form.text.data)
        else:
            file = file_form.file.data
            filename = secure_filename(file.filename)
            with TemporaryDirectory() as tmp_dir:
                filepath = os.path.join(tmp_dir, filename)
                file.save(filepath)
                t = FileLingua(filepath)
        statistics = t.stat()
        items = [LettersFreqItem(l, f) for l, f in statistics['Chars frequency'].items()]
        letters_freq_table = LettersFreqTable(items)
        items = [StatItem(p, v) if p != 'Chars frequency' else StatItem(p, letters_freq_table)
                 for p, v in statistics.items()]
        stat_table = StatTable(items)
        return render_template('index.html', text_form=text_form, file_form=file_form, stat_table=stat_table)
    return render_template('index.html', text_form=text_form, file_form=file_form)

@app.route("/quality", methods=['GET', 'POST'])
def pie_chart():
    evaluate_form = EvaluateForm()
    if evaluate_form.validate_on_submit():
        LettersFreq.set_file("../Frequency_Tables/letters_frequency_twitter.csv")
        q = QualityEvaluator(5)
        print(q.get_total_dict())  # TODO
        print(q.quality_parameters())  # TODO
        sensitivity = q.sensitivity()
        specificity = q.specificity()
        pages_num = q.get_total_dict()['pages_num']
        data = {'Language' : 'Wikipedia pages'}
        data.update({langs_R[l]:v for l, v in q.quality_parameters()['pages_num'].items()})
        return render_template("charts.html", evaluate_form=evaluate_form, data=data, sensitivity=sensitivity*100,
                               specificity=specificity*100, pages_num=pages_num)
    return render_template("charts.html", evaluate_form=evaluate_form)


if __name__ == '__main__':
    app.run()
