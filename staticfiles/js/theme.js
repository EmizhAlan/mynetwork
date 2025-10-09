document.addEventListener("DOMContentLoaded", function () {
    // ===== Смена темы =====
    const themeBtn = document.getElementById("theme-toggle");
    const body = document.body;

    function applyIcon() {
        themeBtn.textContent = body.classList.contains("dark-theme") ? "☀️" : "🌙";
    }

    if (themeBtn) {
        try {
            const saved = localStorage.getItem("site-theme");
            if (saved === "dark") body.classList.add("dark-theme");
        } catch (e) {}

        applyIcon();

        themeBtn.addEventListener("click", function () {
            body.classList.toggle("dark-theme");
            applyIcon();
            try {
                localStorage.setItem("site-theme", body.classList.contains("dark-theme") ? "dark" : "light");
            } catch (e) {}
        });
    }

    // ===== Раскрытие комментариев =====
    const commentButtons = document.querySelectorAll(".toggle-comments");

    commentButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const postId = btn.getAttribute("data-id");
            const commentsDiv = document.getElementById(`comments-${postId}`);
            if (!commentsDiv) return;

            if (commentsDiv.style.display === "none") {
                commentsDiv.style.display = "block";
                btn.textContent = "Скрыть комментарии";
            } else {
                commentsDiv.style.display = "none";
                btn.textContent = "Показать комментарии";
            }
        });
    });
});
