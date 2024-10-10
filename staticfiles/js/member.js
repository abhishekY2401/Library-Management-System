//

// Borrow a book
function borrowBook(bookId) {
  console.log("inside borrow book function...");
  const token = sessionStorage.getItem("access_token");
  fetch(`/api/books/${bookId}/borrow/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      return_date: returnDate,
    }),
  })
    .then((response) => {
      if (response.ok) {
        location.reload(); // Reload the page after borrowing
      } else {
        return response.json().then((error) => {
          console.error("Error:", error);
        });
      }
    })
    .catch((error) => console.error("Error:", error));
}

// Return a book
function returnBook(bookId) {
  const token = sessionStorage.getItem("access_token");
  fetch(`/api/books/${bookId}/return/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
    .then((response) => {
      if (response.ok) {
        location.reload(); // Reload the page after returning
      } else {
        return response.json().then((error) => {
          console.error("Error:", error);
        });
      }
    })
    .catch((error) => console.error("Error:", error));
}

// Open the member history modal
function openMemberHistoryModal() {
  const token = sessionStorage.getItem("access_token");
  const memberId = sessionStorage.getItem("member_id"); // Assuming member_id is stored

  fetch(`/api/members/${memberId}/history/`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const historyContent = document.getElementById("memberHistoryContent");
      historyContent.innerHTML = ""; // Clear previous content

      data.forEach((record) => {
        const recordDiv = document.createElement("div");
        recordDiv.className = "history-record";
        recordDiv.innerHTML = `
        <p>Book Title: ${record.book_title}</p>
        <p>Action: ${record.action_type}</p>
        <p>Date: ${record.issue_date || record.return_date}</p>
        <hr />
        `;
        historyContent.appendChild(recordDiv);
      });

      // Open the modal
      document.getElementById("memberHistoryModal").style.display = "block";
    })
    .catch((error) => console.error("Error fetching history:", error));
}

// Close the member history modal
function closeMemberHistoryModal() {
  document.getElementById("memberHistoryModal").style.display = "none";
}

// Close the modal if user clicks outside of it
window.onclick = function (event) {
  const modal = document.getElementById("memberHistoryModal");
  if (event.target == modal) {
    modal.style.display = "none";
  }
};
