from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    name = StringField('Название задачи', validators=[DataRequired()])
    description = StringField('Описание задачи', validators=[DataRequired()])
    date = DateField('Дата создания', validators=[DataRequired('Введите дату релиза')])
    flag = BooleanField('Статус задачи')
    submit = SubmitField('Отправить')
    save = SubmitField('СОХРАНИТЬ')

class FilterForm(FlaskForm):
    status = StringField()
    show = SubmitField('Показать')

