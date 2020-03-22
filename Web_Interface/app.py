import os
from flask import Flask, render_template, flash, redirect, url_for, current_app
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
import logging

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = os.urandom(20).hex()

dirname = os.path.dirname(__file__)
tableFilename = os.path.join(dirname, "../Frequency_Tables/letters_frequency_twitter.csv")
LettersFreq.set_file(tableFilename)

def start():
    app.run()
    logging.info('App started')

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
    file = FileField("Choose a file...", validators=[FileRequired()])
    submit = SubmitField("Evaluate")

class ConfusionMatrix(Table):
    row = Col("")
    pos = Col("Actual Positive")
    neg = Col("Actual Negative")
    classes = ['table', 'table-borderless', 'table-striped', 'my-table']
    thead_classes = ['table-primary']


class ConfusionMatrixItem(object):
    def __init__(self, row, pos, neg):
        self.row = row
        self.pos = pos
        self.neg = neg

@app.route('/', methods=['GET', 'POST'])
def home():
    LettersFreq.set_file(tableFilename)  # Original Table
    text_form = TextForm()
    file_form = FileForm()
    if text_form.validate_on_submit() or file_form.validate_on_submit():
        logging.info("Valid text submitted. Analyzing...")
        if text_form.validate_on_submit():
            t = TestoLingua(text_form.text.data)
        else:
            file = file_form.file.data
            filename = secure_filename(file.filename)
            logging.info("Filename secured")
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
        logging.info("Valid data submitted. Estimating...")
        file = evaluate_form.file.data
        filename = secure_filename(file.filename)
        logging.info("Filename secured")
        with TemporaryDirectory() as tmp_dir:
            filepath = os.path.join(tmp_dir, filename)
            file.save(filepath)
            logging.info("File saved in temporary directory")
            try:
                LettersFreq.set_file(filepath)
            except:
                logging.error("File format Error. LettersFreq class is not able to initialize frequency table")
                return render_template("charts.html", evaluate_form=evaluate_form, message="File format Error")
            try:
                q = QualityEvaluator(evaluate_form.pages_num.data)
            except:
                logging.error("QualityEvaluator class error. File uploaded doesn't contain all supported languages")
                return render_template("charts.html", evaluate_form=evaluate_form, message="File doesn't contain all supported languages")
            quality_parameters = q.quality_parameters()
            total = q.get_total_dict()
            items = [ConfusionMatrixItem("Predicted Positive", total['true_pos'], total['false_neg']), ConfusionMatrixItem("Predicted Negative", total['false_neg'], total['true_neg'])]
            confusion_matrix = ConfusionMatrix(items)
            sensitivity = q.sensitivity()
            specificity = q.specificity()
            pages_num = total['pages_num']
            data = {'Language' : 'Wikipedia pages'}
            data.update({langs_R[l]:v for l, v in quality_parameters['pages_num'].items()})
            chart = {'Parameter' : 'Percent of the total'}
            chart.update({"Correct": total["true_pos"]+total["true_neg"], "Wrong": total["false_pos"]+total["false_neg"]})
            return render_template("charts.html", evaluate_form=evaluate_form, data=data, sensitivity=sensitivity*100,
                               specificity=specificity*100, pages_num=pages_num, chart=chart, confusion_matrix=confusion_matrix)
    return render_template("charts.html", evaluate_form=evaluate_form)


if __name__ == '__main__':
    start()