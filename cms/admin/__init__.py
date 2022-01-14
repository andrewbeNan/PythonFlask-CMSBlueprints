from datetime import datetime
from flask import Blueprint, abort, render_template, request, redirect, url_for, flash
from cms.admin.models import Type, Content, Setting, User, db

admin_bp = Blueprint(
    "admin", __name__, url_prefix="/admin", template_folder="templates"
)


def requested_type(type):
    types = [row.name for row in Type.query.all()]
    return True if type in types else False


@admin_bp.route("/", defaults={"type": "page"})
@admin_bp.route("/<type>")
def content(type):
    if requested_type(type):
        content = Content.query.join(Type).filter(Type.name == type)
        return render_template("admin/content.html", type=type, content=content)
    else:
        abort(404)


@admin_bp.route("/create/<type>", methods=["GET", "POST"])
def create(type):
    if requested_type(type):
        if request.method == "POST":
            title = request.form.get("title")
            slug = request.form.get("slug")
            type_id = request.form.get("type_id")
            body = request.form.get("body")
            error = None
            if not title:
                error = "Title is required!"
            elif not type_id:
                error = "Type is required"

            if error == None:
                content = Content(title=title, slug=slug, type_id=type_id, body=body)
                db.session.add(content)
                db.session.commit()
                return redirect(url_for("admin.content", type=type))
            flash(error)
        types = Type.query.all()
        return render_template(
            "admin/content_form.html", title="Create", types=types, type_name=type
        )
    else:
        abort(404)


@admin_bp.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    content = Content.query.first_or_404(id)
    type = Type.query.get(content.type_id)
    types = Type.query.all()
    if request.method == "POST":
        content.title = request.form.get("title")
        content.slug = request.form.get("slug")
        content.type_id = request.form.get("type_id")
        content.body = request.form.get("body")
        content.updated_at = datetime.utcnow()
        error = None

        if not request.form["title"]:
            error = "Title is required!"

        if error == None:
            db.session.commit()
            return redirect(url_for("admin.content", type=type.name))
        flash(error)

    return render_template(
        "admin/content_form.html",
        types=types,
        type_name=type.name,
        title="Edit",
        item_title=content.title,
        slug=content.slug,
        type_id=content.type_id,
        body=content.body,
    )


@admin_bp.route("/users")
def users():
    users = User.query.all()
    return render_template("admin/users.html", title="Users", users=users)


@admin_bp.route("/settings")
def settings():
    settings = Setting.query.all()
    return render_template("admin/settings.html", title="Settings", settings=settings)
