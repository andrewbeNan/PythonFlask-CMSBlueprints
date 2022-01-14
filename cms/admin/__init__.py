from flask import Blueprint, abort, render_template
from cms.admin.models import Type, Content, Setting, User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="templates")


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


@admin_bp.route("/create/<type>")
def create(type):
    if requested_type(type):
        types = Type.query.all()
        return render_template(
            "admin/content_form.html", title="Create", types=types, type_name=type
        )
    else:
        abort(404)


@admin_bp.route("/users")
def users():
    users = User.query.all()
    return render_template("admin/users.html", title="Users", users=users)


@admin_bp.route("/settings")
def settings():
    settings = Setting.query.all()
    return render_template("admin/settings.html", title="Settings", settings=settings)
