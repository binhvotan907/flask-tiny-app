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

    # Lấy số trang từ query string, mặc định là trang 1
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Số ghi chú mỗi trang

    # Truy vấn ghi chú của user hiện tại với phân trang
    notes_query = Note.query.filter_by(user_id=current_user.id).order_by(Note.date.desc())
    pagination = notes_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("index.html", user=current_user, notes=pagination.items, pagination=pagination)


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

@views.route("/update-note", methods=["POST"])
@login_required
def update_note():
    data = request.get_json()
    note_id = data.get("note_id")
    new_data = data.get("data")

    if not note_id or not new_data:
        return jsonify({"success": False, "message": "Thiếu thông tin ghi chú"}), 400

    note = Note.query.get(note_id)
    if not note or note.user_id != current_user.id:
        return jsonify({"success": False, "message": "Ghi chú không hợp lệ hoặc không thuộc về bạn"}), 404

    note.data = new_data.strip()
    db.session.commit()
    #flash("Cập nhật ghi chú thành công!", category="success")

    return jsonify({
        "success": True,
        "code": 200,
        "message": "Đã cập nhật ghi chú thành công!"
    })