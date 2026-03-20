function setupTextCounter() {
  const textarea = document.getElementById("text");
  const counter = document.getElementById("charCount");
  if (!textarea || !counter) return;

  const max = textarea.maxLength || 1200;
  const update = () => {
    const v = textarea.value || "";
    counter.textContent = String(v.length);
    counter.style.color = v.length > max * 0.9 ? "rgb(255 0 110)" : "";
  };

  textarea.addEventListener("input", update);
  update();
}

function animateBars() {
  const fills = Array.from(document.querySelectorAll(".bar__fill"));
  if (!fills.length) return;

  const widths = fills.map((el) => el.style.width);
  fills.forEach((el) => (el.style.width = "0%"));

  // Next frame: trigger CSS transition.
  requestAnimationFrame(() => {
    fills.forEach((el, i) => {
      el.style.width = widths[i] || "0%";
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setupTextCounter();
  animateBars();
});

