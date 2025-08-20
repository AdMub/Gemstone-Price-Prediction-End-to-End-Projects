// ===========================
// 💎 Form Validation & Theme Toggle
// ===========================
document.addEventListener("DOMContentLoaded", () => {

  // ===========================
  // 1️⃣ Form Validation
  // ===========================
  const form = document.querySelector(".grid-form");
  if (form) {
    const button = form.querySelector("button");

    form.addEventListener("submit", (e) => {
      button.classList.add("loading"); // show spinner

      const numericIds = ["carat", "depth", "table", "x", "y", "z"];
      for (const id of numericIds) {
        const el = document.getElementById(id);
        if (!el) continue;

        const value = parseFloat(el.value);
        if (Number.isNaN(value)) {
          alert(`Please enter a valid number for "${id}".`);
          el.focus();
          e.preventDefault();
          button.classList.remove("loading");
          return;
        }
      }
    });
  }

  // ===========================
  // 2️⃣ Dark / Light Theme Toggle
  // ===========================
  const themeToggles = document.querySelectorAll("#theme-toggle");

  // Load saved theme (default light)
  const savedTheme = localStorage.getItem("theme") || "light";
  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
  }

  // Sync toggles with saved state
  themeToggles.forEach(toggle => {
    toggle.checked = savedTheme === "dark";

    toggle.addEventListener("change", () => {
      const isDark = toggle.checked;

      if (isDark) {
        document.body.classList.add("dark-mode");
        localStorage.setItem("theme", "dark");
      } else {
        document.body.classList.remove("dark-mode");
        localStorage.setItem("theme", "light");
      }

      // Keep all toggles in sync
      themeToggles.forEach(t => t.checked = isDark);
    });
  });
});
