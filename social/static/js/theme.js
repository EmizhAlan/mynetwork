document.addEventListener("DOMContentLoaded", function () {
  const btn = document.getElementById("theme-toggle");
  if (!btn) return; // если кнопки нет — ничего не падает

  const body = document.body;

  function applyIcon() {
    btn.textContent = body.classList.contains("dark-theme") ? "☀️" : "🌙";
  }

  // применяем сохранённую тему
  try {
    const saved = localStorage.getItem("site-theme");
    if (saved === "dark") body.classList.add("dark-theme");
  } catch (e) {
    // localStorage может быть недоступен — игнорируем
  }

  applyIcon();

  btn.addEventListener("click", function () {
    body.classList.toggle("dark-theme");
    applyIcon();
    try {
      localStorage.setItem("site-theme", body.classList.contains("dark-theme") ? "dark" : "light");
    } catch (e) {}
  });
});
