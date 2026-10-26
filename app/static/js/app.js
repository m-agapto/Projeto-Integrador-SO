document.addEventListener("DOMContentLoaded", () => {
  const type = document.getElementById("schedule-type");
  const runAtWrap = document.getElementById("run-at-wrap");
  const intervalWrap = document.getElementById("interval-wrap");
  const runAt = document.getElementById("run-at");
  const interval = document.getElementById("interval-minutes");

  function updateScheduleFields() {
    const once = type.value === "once";
    runAtWrap.classList.toggle("hidden", !once);
    intervalWrap.classList.toggle("hidden", once);
    runAt.required = once;
    interval.required = !once;
  }
  if (type) {
    type.addEventListener("change", updateScheduleFields);
    updateScheduleFields();
    const local = new Date(Date.now() + 5 * 60000);
    local.setMinutes(local.getMinutes() - local.getTimezoneOffset());
    if (runAt && !runAt.value) runAt.value = local.toISOString().slice(0, 16);
  }

  const search = document.getElementById("task-search");
  if (search) {
    search.addEventListener("input", () => {
      const query = search.value.trim().toLowerCase();
      document.querySelectorAll("#tasks-table tbody tr").forEach(row => {
        row.hidden = !row.dataset.search.includes(query);
      });
    });
  }
});
