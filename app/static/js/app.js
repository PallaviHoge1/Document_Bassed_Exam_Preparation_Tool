function toggleAnswer(btn) {
  const ans = btn.nextElementSibling;
  if (!ans) return;
  ans.classList.toggle("hidden");
  btn.textContent = ans.classList.contains("hidden") ? "Reveal Answer" : "Hide Answer";
}
