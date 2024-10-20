const plotName = encodeURIComponent(window.location.pathname.split("/").pop());
const socket = new WebSocket(
  "ws://" + window.location.host + "/ws/stats/" + plotName + "/"
);

const submitBtn = document.getElementById("submit-btn");
const dataInput = document.getElementById("data-input");
const plot = document.getElementById("plot-name").textContent.trim();
const dataBox = document.getElementById("data-box");

socket.onmessage = function (e) {
  const { message, sender } = JSON.parse(e.data);
  dataBox.innerHTML += `<p>${sender}: ${message}</p>`;
};

submitBtn.onclick = function () {
  const data = dataInput.value;
  socket.send(
    JSON.stringify({
      message: data,
      sender: plot,
    })
  );
};
