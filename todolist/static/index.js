// Hiển thị/ẩn nút "Xóa nhiều" dựa trên checkbox được chọn
function toggleDeleteButton() {
  const checkboxes = document.querySelectorAll(
    'input[name="note-checkbox"]:checked'
  );
  const deleteButton = document.getElementById("delete-selected");
  deleteButton.style.display = checkboxes.length > 0 ? "block" : "none";
}

// Xóa nhiều ghi chú
const deleteSelectedNotes = () => {
  const checkboxes = document.querySelectorAll(
    'input[name="note-checkbox"]:checked'
  );
  const noteIds = Array.from(checkboxes).map((cb) => parseInt(cb.value));

  if (noteIds.length === 0) {
    alert("Vui lòng chọn ít nhất một ghi chú để xóa!");
    return;
  }

  if (!confirm(`Bạn có chắc muốn xóa ${noteIds.length} ghi chú không?`)) {
    return;
  }

  console.log(`Đang xóa các ghi chú với IDs: ${noteIds}`);
  fetch("/delete-note", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ note_ids: noteIds }),
  })
    .then((response) => {
      if (!response.ok) throw new Error("Lỗi khi xóa ghi chú");
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        console.log(`Xóa ${noteIds.length} ghi chú thành công`);
        noteIds.forEach((noteId) => {
          const noteElement = document.querySelector(
            `input[value="${noteId}"]`
          ).parentElement;
          noteElement.style.transition = "opacity 0.3s";
          noteElement.style.opacity = "0";
        });
        setTimeout(() => {
          window.location.reload(); // Tải lại để hiển thị flash
        }, 300);
      } else {
        console.error("Xóa thất bại:", data.message);
        alert("Không thể xóa các ghi chú: " + data.message);
      }
    })
    .catch((error) => {
      console.error("Lỗi:", error);
      alert("Có lỗi xảy ra khi xóa các ghi chú!");
    });
};

// Gọi hàm toggleDeleteButton khi trang tải để kiểm tra trạng thái ban đầu
document.addEventListener("DOMContentLoaded", toggleDeleteButton);
