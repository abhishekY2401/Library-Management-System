function openAddBookModal() {
    document.getElementById("addBookModal").style.display = "block";
}

function closeAddBookModal() {
    document.getElementById("addBookModal").style.display = "none";
}

window.onclick = function (event) {
    const modal = document.getElementById("addBookModal");
    const memberModal = document.getElementById("memberHistoryModal");
    if (event.target === modal || event.target === memberModal) {
        modal.style.display = "none";
        memberModal.style.display = "none";
    }
};

function addNewBook(event) {
    event.preventDefault(); // Prevent the default form submission

    const token = sessionStorage.getItem("access_token");

    const newBookData = {
        title: document.getElementById("newBookTitle").value,
        author: document.getElementById("newBookAuthor").value,
        category: document.getElementById("newBookCategory").value,
        description: document.getElementById("newBookDescription").value,
        isbn: document.getElementById("newBookISBN").value,
        status: document.getElementById("newBookStatus").value,
    };

    fetch(`/api/books/add/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(newBookData),
    })
    .then((response) => {
        if (response.ok) {
            location.reload(); // Reload the page after successful addition
        } else {
            return response.json().then((error) => {
                console.error("Error:", error);
                alert("Failed to add the book. Please try again."); // Example error handling
            });
        }
    })
    .catch((error) => console.error("Error:", error));
}

function openUpdateModal(bookId) {
    document.getElementById("updateBookModal").style.display = "block";

    const token = sessionStorage.getItem("access_token");

    fetch(`/api/books/${bookId}/`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
    })
    .then((response) => response.json())
    .then((data) => {
        document.getElementById("bookId").value = bookId;
        document.getElementById("bookTitle").value = data.title;
        document.getElementById("bookAuthor").value = data.author;
        document.getElementById("bookCategory").value = data.category;
        document.getElementById("bookDescription").value = data.description;
        document.getElementById("bookISBN").value = data.isbn;
        document.getElementById("bookStatus").value = data.status;
    })
    .catch((error) => console.error("Error fetching book details:", error));
}

function updateBookData(event) {
    event.preventDefault();

    const bookId = document.getElementById("bookId").value;
    const token = sessionStorage.getItem("access_token");

    const updatedData = {
        title: document.getElementById("bookTitle").value,
        author: document.getElementById("bookAuthor").value,
        category: document.getElementById("bookCategory").value,
        description: document.getElementById("bookDescription").value,
        isbn: document.getElementById("bookISBN").value,
        status: document.getElementById("bookStatus").value,
    };

    fetch(`/api/books/${bookId}/update/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(updatedData),
    })
    .then((response) => {
        if (response.ok) {
            location.reload();
        } else {
            return response.json().then((error) => {
                console.error("Error:", error);
                alert("Failed to update the book. Please try again."); // Example error handling
            });
        }
    })
    .catch((error) => console.error("Error:", error));
}

function closeUpdateModal() {
    document.getElementById("updateBookModal").style.display = "none";
}

function confirmDelete(bookId) {
    document.getElementById("confirmDeleteButton").onclick = function () {
        deleteBook(bookId);
    };
    document.getElementById("confirmDeleteModal").style.display = "block";
}

function closeConfirmDeleteModal() {
    document.getElementById("confirmDeleteModal").style.display = "none";
}

function deleteBook(bookId) {
    const token = sessionStorage.getItem("access_token");

    fetch(`/api/books/${bookId}/remove/`, {
        method: "DELETE",
        headers: {
            Authorization: `Bearer ${token}`,
        },
    })
    .then((response) => {
        if (response.ok) {
            location.reload();
        } else {
            alert("Failed to delete the book. Please try again."); // Example error handling
        }
    })
    .catch((error) => console.error("Error:", error));
}

function openMemberHistoryModal(records) {
    const historyContent = document.getElementById("memberHistoryContent");
    historyContent.innerHTML = ""; // Clear previous content

    // Populate history content
    records.forEach(record => {
        const recordDiv = document.createElement("div");
        recordDiv.className = "history-record";
        recordDiv.innerHTML = `
            <p>Book Title: ${record.book.title}</p>
            <p>Action: ${record.action_type}</p>
            <p>Date: ${record.date}</p>
            <hr />
        `;
        historyContent.appendChild(recordDiv);
    });

    // Open the modal
    document.getElementById("memberHistoryModal").style.display = "block";
}

function closeMemberHistoryModal() {
    document.getElementById("memberHistoryModal").style.display = "none";
}
