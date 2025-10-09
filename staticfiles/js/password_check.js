document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("signupForm");
  const pass1 = document.getElementById("id_password1");
  const pass2 = document.getElementById("id_password2");
  const matchMsg = document.getElementById("passwordMatchMessage");

  form.addEventListener("submit", (e) => {
    const val1 = pass1.value.trim();
    const val2 = pass2.value.trim();
    let message = "";

    if (val1 !== val2) {
      e.preventDefault();
      message = "❌ Пароли не совпадают";
      matchMsg.style.color = "red";
    } else if (val1.length < 8) {
      e.preventDefault();
      message = "❌ Пароль должен содержать минимум 8 символов";
      matchMsg.style.color = "red";
    } else if (!/[A-Z]/.test(val1) || !/[a-z]/.test(val1) || !/[0-9]/.test(val1)) {
      e.preventDefault();
      message = "❌ Пароль должен содержать строчные, заглавные буквы и цифры";
      matchMsg.style.color = "red";
    } else {
      message = "✅ Пароли совпадают";
      matchMsg.style.color = "green";
    }

    matchMsg.textContent = message;
  });

  // Проверка в реальном времени
  [pass1, pass2].forEach(el => {
    el.addEventListener("input", () => {
      if (pass1.value && pass2.value) {
        if (pass1.value === pass2.value) {
          matchMsg.textContent = "✅ Пароли совпадают";
          matchMsg.style.color = "green";
        } else {
          matchMsg.textContent = "❌ Пароли не совпадают";
          matchMsg.style.color = "red";
        }
      } else {
        matchMsg.textContent = "";
      }
    });
  });
});
