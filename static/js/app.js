document.addEventListener("DOMContentLoaded", () => {
  // плавный вход блока страницы
  const shell = document.getElementById("pageShell");
  if (shell) {
    shell.classList.add("fade-enter");
    requestAnimationFrame(() => shell.classList.add("active"));
  }

  // AOS анимации
  if (window.AOS) AOS.init({ duration: 700, once: true, offset: 60 });

  // тема из памяти
  const saved = localStorage.getItem("theme");
  if (saved === "dark") document.body.classList.add("dark");

  // переключатель темы
  const toggle = document.getElementById("themeToggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      document.body.classList.toggle("dark");
      localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
    });
  }

  // микро-анимация лайка
  document.querySelectorAll(".like-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      btn.classList.add("like-pop");
      setTimeout(() => btn.classList.remove("like-pop"), 350);
    });
  });

  // частицы на фоне
  if (window.tsParticles) {
    tsParticles.load("particles", {
      background: { color: { value: "transparent" } },
      fpsLimit: 60,
      interactivity: {
        events: { onHover: { enable: true, mode: "repulse" }, onClick: { enable: true, mode: "push" } },
        modes: { repulse: { distance: 110 }, push: { quantity: 2 } }
      },
      particles: {
        color: { value: ["#2A6FF2", "#67B7FF", "#8CF0D6", "#FFD6A6", "#FFB3C7"] },
        links: { enable: true, color: "#67B7FF", distance: 135, opacity: 0.25, width: 1 },
        move: { enable: true, speed: 1.1, outModes: { default: "out" } },
        number: { value: 45, density: { enable: true, area: 900 } },
        opacity: { value: 0.55 },
        shape: { type: "circle" },
        size: { value: { min: 1, max: 4 } }
      },
      detectRetina: true
    });
  }
});