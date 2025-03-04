from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint("views", __name__)

@views.route("/home", methods=["GET", "POST"])
@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        if not note or len(note.strip()) < 1:
            flash("Ghi chú không được để trống!", category="error")
        else:
            new_note = Note(data=note.strip(), user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Thêm ghi chú thành công!", category="success")
        return redirect(url_for('views.home'))
    return render_template("index.html", user=current_user)

@views.route("/delete-note", methods=["POST"])
@login_required
def delete_note():
    data = request.get_json()
    note_ids = data.get("note_ids", [])

    if not note_ids:
        return jsonify({"success": False, "message": "Chưa chọn ghi chú nào để xóa"}), 400

    notes = Note.query.filter(Note.id.in_(note_ids), Note.user_id == current_user.id).all()
    if not notes:
        return jsonify({"success": False, "message": "Không tìm thấy ghi chú nào hợp lệ"}), 404

    deleted_count = len(notes)
    for note in notes:
        db.session.delete(note)
    db.session.commit()

    if deleted_count == 1:
        flash("Xóa ghi chú thành công!", category="success")
    else:
        flash(f"Xóa {deleted_count} ghi chú thành công!", category="success")

    return jsonify({
        "success": True,
        "code": 200,
        "message": f"Đã xóa {deleted_count} ghi chú"
    })