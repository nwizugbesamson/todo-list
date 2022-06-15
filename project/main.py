from unicodedata import name
from project import db
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from project.forms import EntryForm, EditForm, ListForm
from project.models import Task, TaskList
from datetime import datetime


main = Blueprint(name="main", import_name=__name__, static_folder="static", template_folder="templates")




@main.route("/")
@main.route("/home")
def home_page():
    return render_template("index.html")


@main.route("/user/lists/")
@main.route("/user/lists/<int:list_id>", methods=["POST", "GET"])
@login_required
def list_page(list_id=None):
   
    user_task_lists = TaskList.query.filter_by(user_id=current_user.id).all()
    if list_id:
        edit_list = TaskList.query.get(list_id)
        form= ListForm(
            name=edit_list.name
        )
        if form.validate_on_submit():   
            edit_list.name = form.name.data
            db.session.commit()
            return redirect(url_for('main.list_page'))
        return render_template("list.html", user_task_lists=user_task_lists, form=form)
    return render_template("list.html", user_task_lists=user_task_lists)


@main.route("/user/")
@main.route("/user/<int:list_id>", methods=["GET", "POST"])
@main.route("/user/<int:list_id>/<int:task_id>/<action>", methods=["GET", "POST"])
@login_required
def user_page(list_id=None, task_id=None, action=None):
    form = EntryForm()
    
    user_task_lists = TaskList.query.filter_by(user_id=current_user.id).all()
    if list_id:
        tasks = Task.query.filter_by(task_list_id=list_id)
        
        if form.validate_on_submit() and action is None:
            new_task = Task(
                entry=form.entry.data,
                task_list_id=list_id,
                status = "UNDONE"
            )
            db.session.add(new_task)
            db.session.commit()
            return redirect(request.referrer)
        if task_id and action == "edit":
            task = Task.query.get(task_id)
            form2 = EditForm(entry=task.entry)
            
            
            if form2.validate_on_submit():
                task.entry = form2.entry.data
                db.session.commit()
                return redirect(url_for("main.user_page", list_id=list_id))
            return render_template("user.html", user_task_lists=user_task_lists, tasks=tasks, form2=form2)
        return render_template("user.html", user_task_lists=user_task_lists, tasks=tasks, form=form)
    if user_task_lists:
        return render_template("user.html", user_task_lists=user_task_lists)
    return render_template("user.html")


@main.route("/user/newlist")
@login_required
def new_list():
    current_date = datetime.utcnow().date()
    new_name = f"{current_user.username} {current_date}"
    if TaskList.query.filter_by(date=current_date).first():
        simillar = TaskList.query.filter_by(name=new_name).all()
        new_name = f"{current_user.username} {current_date} {len(simillar) + 1}"
    new_list = TaskList(
        user_id=current_user.id,
        date=current_date,
        name=new_name
    )
    db.session.add(new_list)
    db.session.commit()
    return redirect(url_for('main.user_page', list_id=new_list.id))




@main.route('/delete/<int:list_id>')
@login_required
def delete_list_page(list_id):
    del_list = TaskList.query.get(list_id)
    for task in del_list.tasks:
        db.session.delete(task)
    db.session.delete(del_list)
    db.session.commit()
    return redirect(request.referrer)


@main.route('/delete_task/<int:task_id>')
@login_required
def delete_task_page(task_id):
    del_task = Task.query.get(task_id)
    db.session.delete(del_task)
    db.session.commit()
    return redirect(request.referrer)

@main.route('/status/<int:task_id>')
@login_required
def status_page(task_id):
    update_task = Task.query.get(task_id)
    if update_task.status == "COMPLETED":
        update_task.status = "NOT COMPLETED"
        db.session.commit()
        return redirect(request.referrer)
    else:
        update_task.status = "COMPLETED"
        db.session.commit()
        return redirect(request.referrer)






