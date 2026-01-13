async function loadEvents() {
  const res = await fetch("/events");
  const events = await res.json();

  const el = document.getElementById("events");
  el.innerHTML = "";

  events.forEach(e => {
    const div = document.createElement("div");
    div.className = "card";
    div.innerHTML = `
      <b>${e.rule}</b><br/>
      Camera: ${e.camera_id}<br/>
      Time: ${e.timestamp}
    `;
    el.appendChild(div);
  });
}

setInterval(loadEvents, 3000);
loadEvents();
