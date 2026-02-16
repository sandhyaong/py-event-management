/* ========================================
   ADD / EDIT FORM HANDLER
======================================== */

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("eventForm");

    if (form) {
        form.addEventListener("submit", async function (e) {
            e.preventDefault();

            const formData = new FormData(form);

            try {
                const result = await apiPostForm(window.location.href, formData);
                showToast(result.message);
                window.location.href = "/dashboard/";
            } catch (error) {
                console.error(error);
            }
        });
    }

});


/* ========================================
   DELETE HANDLER
======================================== */

async function deleteEvent(url, elementId) {
    try {
        const result = await apiDelete(url);
        document.getElementById(elementId).remove();
        showToast(result.message, true);
    } catch (error) {
        console.error(error, false);
    }
}
