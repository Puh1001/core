const plotName = encodeURIComponent(window.location.pathname.split("/").pop());
const socket = new WebSocket(
  "ws://" + window.location.host + "/ws/stats/" + plotName + "/"
);

const submitBtn = document.getElementById("submit-btn");
const dataInput = document.getElementById("data-input");
const plot = document.getElementById("plot-name").textContent.trim();
const dataBox = document.getElementById("data-box");
const startSimBtn = document.getElementById("start-sim-btn");
const stopSimBtn = document.getElementById("stop-sim-btn");
const simulateAlertBtn = document.getElementById("simulate-alert-btn");

let simulationInterval;

const createChart = (ctx, label) => {
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: label,
          data: [],
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
};

const charts = {
  soilPh: createChart(
    document.getElementById("chart-soilPh").getContext("2d"),
    "Soil pH"
  ),
  light: createChart(
    document.getElementById("chart-light").getContext("2d"),
    "Light"
  ),
  ambientTemperature: createChart(
    document.getElementById("chart-ambientTemperature").getContext("2d"),
    "Ambient Temperature"
  ),
  ambientHumidity: createChart(
    document.getElementById("chart-ambientHumidity").getContext("2d"),
    "Ambient Humidity"
  ),
  soilMoistur: createChart(
    document.getElementById("chart-soilMoistur").getContext("2d"),
    "Soil Moisture"
  ),
  soilTemperature: createChart(
    document.getElementById("chart-soilTemperature").getContext("2d"),
    "Soil Temperature"
  ),
};

const alertThresholds = {
  soilPh: { min: 5.5, max: 7.5 },
  light: { min: 0, max: 100 },
  ambientTemperature: { min: 10, max: 40 },
  ambientHumidity: { min: 20, max: 80 },
  soilMoistur: { min: 10, max: 60 },
  soilTemperature: { min: 10, max: 40 },
};

const checkAlerts = (data) => {
  const alerts = [];
  Object.keys(alertThresholds).forEach((key) => {
    if (data[key] !== undefined) {
      const value = parseFloat(data[key]);
      const { min, max } = alertThresholds[key];
      if (value < min || value > max) {
        alerts.push({ parameter: key, value: value });
      }
    }
  });
  return alerts;
};

const sendEmailAlert = (parameter, value) => {
  fetch("/stats/send-email-alert/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      parameter: parameter,
      value: value,
      plot: plot,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status !== "success") {
        console.error("Failed to send email alert");
      }
    });
};

socket.onmessage = function (e) {
  const { message, sender } = JSON.parse(e.data);
  dataBox.innerHTML += `<p>${sender}: ${message}</p>`;

  // Update charts
  const data = JSON.parse(message);
  const timestamp = new Date().toLocaleTimeString();
  Object.keys(charts).forEach((key) => {
    if (data[key] !== undefined) {
      charts[key].data.labels.push(timestamp);
      charts[key].data.datasets[0].data.push(data[key]);
      charts[key].update();
    }
  });
};

submitBtn.onclick = function () {
  const data = dataInput.value;
  socket.send(
    JSON.stringify({
      message: JSON.stringify({ soilPh: data }),
      sender: plot,
    })
  );
};

startSimBtn.onclick = function () {
  if (!simulationInterval) {
    simulationInterval = setInterval(() => {
      const simulatedData = {
        soilPh: (Math.random() * 2 + 5).toFixed(2), // Giả lập giá trị pH từ 5.00 đến 7.00
        light: (Math.random() * 100).toFixed(2),
        ambientTemperature: (Math.random() * 30 + 10).toFixed(2),
        ambientHumidity: (Math.random() * 100).toFixed(2),
        soilMoistur: (Math.random() * 100).toFixed(2),
        soilTemperature: (Math.random() * 30 + 10).toFixed(2),
      };
      socket.send(
        JSON.stringify({
          message: JSON.stringify(simulatedData),
          sender: plot,
        })
      );
    }, 1000); // Gửi dữ liệu mỗi giây
  }
};

stopSimBtn.onclick = function () {
  if (simulationInterval) {
    clearInterval(simulationInterval);
    simulationInterval = null;
  }
};

simulateAlertBtn.onclick = function () {
  const simulatedAlertData = {
    soilPh: 4.0, // Giá trị pH giả lập vượt ngưỡng
    light: 150, // Giá trị ánh sáng giả lập vượt ngưỡng
    ambientTemperature: 50, // Giá trị nhiệt độ giả lập vượt ngưỡng
    ambientHumidity: 90, // Giá trị độ ẩm giả lập vượt ngưỡng
    soilMoistur: 5, // Giá trị độ ẩm đất giả lập vượt ngưỡng
    soilTemperature: 50, // Giá trị nhiệt độ đất giả lập vượt ngưỡng
  };
  const alerts = checkAlerts(simulatedAlertData);
  alerts.forEach((alert) => {
    sendEmailAlert(alert.parameter, alert.value);
  });
};

// Function to get CSRF token
const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};
