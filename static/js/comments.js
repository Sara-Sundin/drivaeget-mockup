/* jshint esversion: 9 */
/* global bootstrap */


document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript Loaded!"); // Debugging log

    // Ensure delete modal exists before initializing
    let deleteModalElement = document.getElementById("deleteModal");
    let deleteConfirm = document.getElementById("deleteConfirm");

    if (deleteModalElement) {
        let deleteModal = new bootstrap.Modal(deleteModalElement, {
            backdrop: "static",
            keyboard: true
        });

        document.body.addEventListener("click", function (event) {
            if (event.target.classList.contains("btn-delete")) {
                event.preventDefault();
                let commentId = event.target.getAttribute("comment_id") ||
                                event.target.closest(".btn-delete").getAttribute("comment_id");

                // Get the post slug dynamically
                let postSlug = document.getElementById("commentForm").getAttribute("data-post-slug");

                if (commentId && postSlug) {
                    deleteConfirm.href = `/blog/${postSlug}/delete_comment/${commentId}/`; // Add full path & trailing slash
                    deleteModal.show();
                } else {
                    console.error("Post slug or comment ID is missing for delete action.");
                }
            }
        });
    }

    // Handle comment editing with smooth scroll
    let editButtons = document.querySelectorAll(".btn-edit");
    let commentText = document.getElementById("id_body");
    let commentForm = document.getElementById("commentForm");
    let submitButton = document.getElementById("submitButton");

    if (!commentForm || !commentText || !submitButton) {
        console.error("Comment form elements are missing.");
        return;
    }

    editButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            let commentId = button.getAttribute("comment_id");
            let commentContentElement = document.getElementById(`comment${commentId}`);

            // Ensure comment ID is valid before proceeding
            if (!commentId || commentId === "0") {
                console.error("Invalid comment ID for editing.");
                return;
            }

            if (commentContentElement) {
                // Populate the form with the existing comment text
                commentText.value = commentContentElement.innerText.trim();
                submitButton.innerText = "Update";

                // Get the correct post slug
                let postSlug = commentForm.getAttribute("data-post-slug");

                if (postSlug) {
                    // Set the correct action URL for the comment edit form (ENSURE TRAILING SLASH)
                    commentForm.setAttribute("action", `/blog/${postSlug}/edit_comment/${commentId}/`);
                } else {
                    console.error("Post slug is missing for edit action.");
                    return;
                }

                // Smoothly scroll to the comment form
                commentForm.scrollIntoView({ behavior: "smooth", block: "center" });
            } else {
                console.error("Comment content not found for editing.");
            }
        });
    });
});