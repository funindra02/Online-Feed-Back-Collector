/* ────────────────────────────────────────────────────────
   FeedbackHub — script.js
   - Star rating interaction
   - Form validation
   - AJAX submit
   ──────────────────────────────────────────────────────── */

document.addEventListener("DOMContentLoaded", () => {

  // ── Star Rating ────────────────────────────────────────
  const starGroup = document.getElementById("starGroup");
  if (starGroup) {
    const labels = starGroup.querySelectorAll(".star-label");

    const applyFill = (upToIndex) => {
      labels.forEach((lbl, i) => {
        lbl.classList.toggle("filled", i <= upToIndex);
      });
      starGroup.classList.add("rated");
    };

    labels.forEach((lbl, i) => {
      lbl.addEventListener("mouseenter", () => applyFill(i));
      lbl.addEventListener("click",      () => applyFill(i));
    });

    starGroup.addEventListener("mouseleave", () => {
      const checked = starGroup.querySelector(".star-radio:checked");
      if (checked) {
        const idx = [...labels].indexOf(checked.closest(".star-label"));
        applyFill(idx);
      } else {
        labels.forEach(l => l.classList.remove("filled"));
        starGroup.classList.remove("rated");
      }
    });
  }

  // ── Character Counter ──────────────────────────────────
  const textarea  = document.getElementById("comments");
  const charCount = document.getElementById("charCount");
  if (textarea && charCount) {
    const MAX = 500;
    textarea.addEventListener("input", () => {
      const len = textarea.value.length;
      if (len > MAX) textarea.value = textarea.value.slice(0, MAX);
      charCount.textContent = `${Math.min(len, MAX)} / ${MAX}`;
      charCount.style.color = len >= MAX ? "var(--red)" : "";
    });
  }

  // ── AJAX Form Submit ───────────────────────────────────
  const form      = document.getElementById("feedbackForm");
  const submitBtn = document.getElementById("submitBtn");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    clearErrors();
    const valid = validateForm();
    if (!valid) return;

    // Loading state
    submitBtn.disabled = true;
    submitBtn.querySelector(".btn-text").textContent = "Submitting…";
    const spinner = submitBtn.querySelector(".btn-spinner");
    if (spinner) spinner.hidden = false;

    const data = {
      name:     document.getElementById("name").value.trim(),
      email:    document.getElementById("email").value.trim(),
      rating:   (form.querySelector(".star-radio:checked") || {}).value,
      comments: document.getElementById("comments").value.trim(),
    };

    try {
      const res  = await fetch("/submit-feedback", {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify(data),
      });
      const json = await res.json();

      if (json.success) {
        showSuccess();
      } else {
        (json.errors || ["Something went wrong."]).forEach(msg => showGlobalError(msg));
        resetButton();
      }
    } catch {
      showGlobalError("Network error. Please try again.");
      resetButton();
    }
  });

  // ── Helpers ────────────────────────────────────────────

  function validateForm() {
    let ok = true;

    const name  = document.getElementById("name");
    const email = document.getElementById("email");
    const rated = form.querySelector(".star-radio:checked");

    if (!name.value.trim()) {
      showError("nameError", "Name is required.");
      ok = false;
    }

    const emailVal = email.value.trim();
    if (!emailVal || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailVal)) {
      showError("emailError", "Enter a valid email address.");
      ok = false;
    }

    if (!rated) {
      showError("ratingError", "Please select a star rating.");
      ok = false;
    }

    return ok;
  }

  function showError(id, msg) {
    const el = document.getElementById(id);
    if (el) el.textContent = msg;
  }

  function showGlobalError(msg) {
    let box = document.getElementById("globalError");
    if (!box) {
      box = document.createElement("div");
      box.id = "globalError";
      box.className = "alert alert--error";
      form.prepend(box);
    }
    box.innerHTML = `<strong>Error:</strong> ${msg}`;
  }

  function clearErrors() {
    ["nameError", "emailError", "ratingError"].forEach(id => showError(id, ""));
    const ge = document.getElementById("globalError");
    if (ge) ge.remove();
  }

  function resetButton() {
    submitBtn.disabled = false;
    submitBtn.querySelector(".btn-text").textContent = "Submit Feedback";
    const spinner = submitBtn.querySelector(".btn-spinner");
    if (spinner) spinner.hidden = true;
  }

  function showSuccess() {
    const card = document.getElementById("feedbackCard");
    card.innerHTML = `
      <div class="success-state">
        <div class="success-icon">✓</div>
        <h2>Thank you!</h2>
        <p>Your feedback has been recorded. We really appreciate it.</p>
        <button class="btn btn--primary" onclick="window.location.href='/'">Submit Another</button>
      </div>`;
  }
});
