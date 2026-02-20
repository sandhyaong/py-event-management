/* ========================================
   CSRF TOKEN
======================================== */

function getCSRFToken() {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith("csrftoken=")) {
            return cookie.substring("csrftoken=".length);
        }
    }
    return null;
}

/* ========================================
   BASE RESPONSE HANDLER
======================================== */

async function handleResponse(response) {
    const data = await response.json();

    if (!data.status || data.status !== "success") {
        // alert(data.message || "Something went wrong");
        showToast(data.message || "Something went wrong");

        throw data;
    }

    return data;
}

/* ========================================
   POST FORM (ADD / EDIT)
======================================== */

async function apiPostForm(url, formData) {
    const response = await fetch(url, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "X-Requested-With": "XMLHttpRequest"
        }
    });

    return handleResponse(response);
}

/* ========================================
   DELETE
======================================== */

async function apiDelete(url) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "X-Requested-With": "XMLHttpRequest"
        }
    });

    return handleResponse(response);
}
function showToast(message, success=true) {

    const bgClass = success ? "text-bg-success" : "text-bg-danger";

    const toastContainer = document.createElement("div");
    toastContainer.className =
        `toast align-items-center ${bgClass} border-0 show position-fixed bottom-0 start-0 m-3`;
        toastContainer.style.position = "fixed";
        toastContainer.style.bottom = "10px";
        toastContainer.style.left = "10px";
        toastContainer.style.zIndex = "2000";

    toastContainer.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button"
                    class="btn-close btn-close-white m-auto"
                    onclick="this.closest('.toast').remove()">
            </button>
        </div>
    `;

    document.body.appendChild(toastContainer);

    setTimeout(() => toastContainer.remove(), 50000);
}
