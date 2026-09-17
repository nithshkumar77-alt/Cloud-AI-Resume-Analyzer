const resume = document.getElementById("resume");
const jobDescription = document.getElementById("jobDescription");
const fileInput = document.getElementById("fileInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const results = document.getElementById("results");
const statusEl = document.getElementById("status");

fileInput.addEventListener("change", async () => {
  if (!fileInput.files.length) return;
  const form = new FormData();
  form.append("resume", fileInput.files[0]);
  statusEl.textContent = "Reading resume...";
  try {
    const res = await fetch("/api/upload", { method: "POST", body: form });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Upload failed");
    resume.value = data.resume;
    statusEl.textContent = "Resume loaded.";
  } catch (err) {
    statusEl.textContent = err.message;
  }
});

function renderChips(id, items, type = "") {
  const el = document.getElementById(id);
  el.innerHTML = "";
  if (!items.length) {
    el.innerHTML = '<span class="chip">None detected</span>';
    return;
  }
  items.forEach(item => {
    const span = document.createElement("span");
    span.className = "chip " + type;
    span.textContent = item;
    el.appendChild(span);
  });
}

analyzeBtn.addEventListener("click", async () => {
  if (!resume.value.trim()) {
    statusEl.textContent = "Please paste or upload your resume first.";
    return;
  }

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";
  statusEl.textContent = "";

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        resume: resume.value,
        job_description: jobDescription.value
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Analysis failed");

    document.getElementById("score").innerHTML = `${data.score}<span>/100</span>`;
    document.getElementById("ringValue").textContent = `${data.score}%`;
    document.querySelector(".score-ring").style.background =
      `conic-gradient(var(--primary) ${data.score * 3.6}deg, #e8eaf1 0deg)`;

    document.getElementById("scoreText").textContent =
      data.score >= 75 ? "Strong keyword and structure match." :
      data.score >= 50 ? "Good starting point. A few improvements can strengthen it." :
      "There is room to improve structure and job-specific keyword matching.";

    renderChips("matched", data.matched, "ok");
    renderChips("skills", data.skills);
    renderChips("missing", data.missing, "missing");
    renderChips("sections", data.sections);

    const ul = document.getElementById("suggestions");
    ul.innerHTML = "";
    data.suggestions.forEach(item => {
      const li = document.createElement("li");
      li.textContent = item;
      ul.appendChild(li);
    });

    results.classList.remove("hidden");
    results.scrollIntoView({behavior: "smooth"});
  } catch (err) {
    statusEl.textContent = err.message;
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = 'Analyze Resume <span>→</span>';
  }
});
