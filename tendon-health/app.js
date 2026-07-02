(function () {
  const STORAGE_KEY = "tendon-isometrics-log";
  const grid = document.getElementById("exercise-grid");
  const filtersNav = document.getElementById("filters");
  const template = document.getElementById("exercise-card-template");
  const progressSummary = document.getElementById("progress-summary");

  const totalExercises = REGIONS.reduce((sum, r) => sum + r.exercises.length, 0);

  function todayKey() {
    return new Date().toISOString().slice(0, 10);
  }

  function loadLog() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch (e) {
      return {};
    }
  }

  function saveLog(log) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(log));
  }

  function isDoneToday(log, exerciseId) {
    return log[exerciseId] === todayKey();
  }

  function setDone(exerciseId, done) {
    const log = loadLog();
    if (done) {
      log[exerciseId] = todayKey();
    } else {
      delete log[exerciseId];
    }
    saveLog(log);
    renderProgress();
  }

  function lastDoneText(log, exerciseId) {
    const date = log[exerciseId];
    if (!date) return "Not logged yet";
    if (date === todayKey()) return "Done today";
    return "Last done: " + date;
  }

  function renderProgress() {
    const log = loadLog();
    const doneToday = REGIONS.flatMap((r) => r.exercises).filter((ex) =>
      isDoneToday(log, ex.id)
    ).length;
    progressSummary.textContent = `Today: ${doneToday} / ${totalExercises} exercises logged`;
  }

  function buildFilters(activeRegionId) {
    filtersNav.innerHTML = "";
    const allBtn = document.createElement("button");
    allBtn.className = "filter-btn" + (activeRegionId === "all" ? " active" : "");
    allBtn.textContent = "All";
    allBtn.addEventListener("click", () => render("all"));
    filtersNav.appendChild(allBtn);

    REGIONS.forEach((region) => {
      const btn = document.createElement("button");
      btn.className = "filter-btn" + (activeRegionId === region.id ? " active" : "");
      btn.textContent = region.name;
      btn.addEventListener("click", () => render(region.id));
      filtersNav.appendChild(btn);
    });
  }

  function buildCard(exercise, log) {
    const node = template.content.cloneNode(true);
    const iframe = node.querySelector("iframe");
    iframe.src = `https://www.youtube.com/embed/${exercise.videoId}`;
    iframe.title = exercise.name;

    node.querySelector(".ex-name").textContent = exercise.name;
    node.querySelector(".target-badge").textContent = exercise.target;
    node.querySelector(".protocol").textContent = exercise.protocol;

    const watchLink = node.querySelector(".watch-link");
    watchLink.href = `https://www.youtube.com/watch?v=${exercise.videoId}`;

    const stepsList = node.querySelector(".steps");
    exercise.steps.forEach((step) => {
      const li = document.createElement("li");
      li.textContent = step;
      stepsList.appendChild(li);
    });

    const secondaryWrap = node.querySelector(".secondary-links");
    if (exercise.secondary && exercise.secondary.length) {
      const label = document.createElement("span");
      label.textContent = "More demos: ";
      secondaryWrap.appendChild(label);
      exercise.secondary.forEach((videoId, i) => {
        const a = document.createElement("a");
        a.href = `https://www.youtube.com/watch?v=${videoId}`;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        a.textContent = `video ${i + 1}`;
        secondaryWrap.appendChild(a);
        if (i < exercise.secondary.length - 1) {
          secondaryWrap.appendChild(document.createTextNode(", "));
        }
      });
    }

    const checkbox = node.querySelector(".done-checkbox");
    checkbox.checked = isDoneToday(log, exercise.id);
    checkbox.addEventListener("change", (e) => {
      setDone(exercise.id, e.target.checked);
      lastDoneEl.textContent = lastDoneText(loadLog(), exercise.id);
    });

    const lastDoneEl = node.querySelector(".last-done");
    lastDoneEl.textContent = lastDoneText(log, exercise.id);

    return node;
  }

  function render(regionId) {
    buildFilters(regionId);
    grid.innerHTML = "";
    const log = loadLog();
    const regionsToShow =
      regionId === "all" ? REGIONS : REGIONS.filter((r) => r.id === regionId);

    regionsToShow.forEach((region) => {
      const heading = document.createElement("h2");
      heading.className = "region-heading";
      heading.textContent = region.name;
      grid.appendChild(heading);

      region.exercises.forEach((exercise) => {
        grid.appendChild(buildCard(exercise, log));
      });
    });

    renderProgress();
  }

  render("all");

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("sw.js").catch(() => {});
    });
  }
})();
