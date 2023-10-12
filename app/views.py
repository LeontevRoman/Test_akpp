from flask_login import login_required, login_user, logout_user
from pony.orm import select
from app import app
from app.models import User, db, Task
from pony.orm.examples.estore import *
from app.forms import FilterForm, TaskForm

from flask import flash, redirect, render_template, request, url_for


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username and password:
            possible_user = User.get(login=username)
            if not possible_user:
                flash('User not found')
                return redirect('/login')
            if possible_user.password == password:
                possible_user.last_login = datetime.now()
                login_user(possible_user)
                return redirect('/')
        flash('Wrong password')
        return redirect('/login')
    else:
        return render_template('login.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username and password:
            exist = User.get(login=username)
            if exist:
                flash('Username %s is already taken, choose another one' % username)
                return redirect('/reg')
        
            user = User(login=username, password=password)
            user.last_login = datetime.now()
            flush()
            login_user(user)
            flash('Successfully registered')
            return redirect('/')
        else:
            flash('Enter the correct Login and Password')
            return redirect('/reg')
    else:
        return render_template('reg.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out')
    return redirect('/')


@app.route("/", methods=['GET', 'POST'])
def view():
    """
    Отображение всех задач + фильтр на статус
    """
    form = FilterForm()
    query = Task.select().order_by(Task.id)
    status = ['', 'Сompleted', 'Process']
    
    if request.method == 'POST':
        try:    
            if form.status.data == "Сompleted":
                query = Task.select(lambda t: t.flag==True).order_by(Task.id)
                return render_template('view.html', form=form, query=query, status=status)
            elif form.status.data == "Process":
                query = Task.select(lambda t: t.flag==False).order_by(Task.id)
                return render_template('view.html', form=form, query=query, status=status)
    
        except Exception as ex:
            flash(f'Данные не найдены - {ex}')
            
    return render_template('view.html', form=form, query=query, status=status)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    """
    Добавление новой задачи
    """
    form = TaskForm()
    count_tasks = len(Task.select().order_by(Task.id))
    if request.method == 'POST':
        try:
            print(form.name.data)
            Task(
                id=count_tasks+1,
                name=form.name.data,
                description=form.description.data,
                date=form.date.data,
                flag=form.flag.data,
                )
            flash(f'Добавлено новое задание')
            return redirect(url_for('view'))
        
        except Exception as ex:
            db.rollback()
            flash(f'Данные не добавлены - {ex}')
            return render_template('add.html', form=form, title='Добавить задание')
    return render_template('add.html', form=form, title='Добавить задание')


@app.route('/task/<int:number_task>')
def view_task(number_task):
    """
    Вывод задачи по её ID
    """
    task = Task[number_task]
    form = TaskForm()
    count_tasks = len(Task.select().order_by(Task.id))
    return render_template('view_task.html', task=task, form=form, count_tasks=count_tasks)


@app.route('/edit/<int:number_task>', methods=['GET', 'POST'])
def edit_task(number_task):
    """
    Редактирование задачи
    """
    task = Task[number_task]
    form = TaskForm()
    if request.method == 'POST':
        try:
            task = Task[number_task]
            task.set(name=form.name.data, 
                     description=form.description.data,
                     flag=form.flag.data)
            flash('Данные сохранены')
            return redirect(url_for('view_task', number_task=number_task))
        except Exception as ex:
            db.rollback()
            flash(f'Данные не добавлены - {ex}')
            return render_template('edit_task.html', task=task, form=form)    

    return render_template('edit_task.html', task=task, form=form)