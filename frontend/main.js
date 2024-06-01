import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

// TODO: Fetch via appropriate Endpoints
const availableWeatherLocations = [
  "Chur",
  "Buchs",
  "Mels",
  "St. Gallen",
  "Zürich",
];
const availableWeatherMetrics = [
  {
    identifier: "temperature",
    title: "Temperature",
    subtitle: "Make a comparison based on Temperature in °C",
  },
  {
    identifier: "rain",
    title: "Rain",
    subtitle: "Amount of rain",
  },
];

const selectedWeatherLocations = [];
const selectedWeatherMetrics = [];

const weatherLocationCardSuffix = "weather-location-card-element";
const weatherMetricCardSuffix = "weather-metric-card-element";

const root = document.querySelector(":root");
const lightAppleBlueColor =
  getComputedStyle(root).getPropertyValue("--light-apple-blue");
const lightAppleYellowColor = getComputedStyle(root).getPropertyValue(
  "--light-apple-yellow",
);

const weatherLocationInfo = document.getElementById("weather-location-info");
weatherLocationInfo.innerHTML = "Please choose exactly two Locations";

const weatherMetricInfo = document.getElementById("weather-metric-info");
weatherMetricInfo.innerHTML = "Please choose at least one Metric";

const chartContext = document.getElementById("my-chart");
new Chart(chartContext, {
  type: "bar",
  data: {
    labels: ["Buchs", "Chur"],
    datasets: [
      {
        label: "Temperature in °C",
        data: [10, 15],
        backgroundColor: [lightAppleBlueColor, lightAppleYellowColor],
        borderWidth: 0,
      },
    ],
  },
});

const createWeatherLocationCard = (locationName, index) => {
  const weatherCard = `<div class="weather-location-card" data-name="${locationName}" id="${weatherLocationCardSuffix}-${index}"><p>${locationName}</p></div>`;
  return weatherCard;
};

const createWeatherMetricCard = (metric, index) => {
  const title = metric.title;
  const subtitle = metric.subtitle;
  const identifier = metric.identifier;
  const weatherCard = `<div class="weather-metric-card" data-metric="${identifier}" id="${weatherMetricCardSuffix}-${index}"><p class="title">${title}</p><p class="subtitle">${subtitle}</p></div>`;
  return weatherCard;
};

const weatherLocationCardsContainer = document.getElementById(
  "weather-location-cards-container",
);
availableWeatherLocations.map(
  (location, index) =>
    (weatherLocationCardsContainer.innerHTML += createWeatherLocationCard(
      location,
      index,
    )),
);

const weatherMetricCardsContainer = document.getElementById(
  "weather-metric-cards-container",
);
availableWeatherMetrics.map(
  (metric, index) =>
    (weatherMetricCardsContainer.innerHTML += createWeatherMetricCard(
      metric,
      index,
    )),
);

// Define Event Handlers
const onWeatherLocationCardClicked = (e) => {
  const weatherLocationCard = e.currentTarget;
  const weatherLocationName = weatherLocationCard.dataset.name.toString();
  const index = selectedWeatherLocations.indexOf(weatherLocationName);
  const alreadySelected = index >= 0 && selectedWeatherLocations.length !== 0;
  if (alreadySelected) {
    selectedWeatherLocations.splice(index, 1);
  } else {
    selectedWeatherLocations.push(weatherLocationName);
  }
  weatherLocationCard.classList.toggle("weather-location-card-selected");
  const numberOfSelectedWeatherLocations = selectedWeatherLocations.length;
  if (numberOfSelectedWeatherLocations > 2) {
    weatherLocationInfo.classList.add("error-text");
    weatherLocationInfo.innerHTML = `You have choosen ${numberOfSelectedWeatherLocations} Locations but you have to choose exactly two`;
  } else {
    weatherLocationInfo.classList.remove("error-text");
    weatherLocationInfo.innerHTML = `Please choose exactly two Locations`;
  }
};

const onWeatherMetricCardClicked = (e) => {
  const weatherMetricCard = e.currentTarget;
  const weatherMetric = weatherMetricCard.dataset.metric;
  const index = selectedWeatherLocations.indexOf(weatherMetric);
  const alreadySelected = index >= 0 && selectedWeatherMetrics.length !== 0;
  if (alreadySelected) {
    selectedWeatherMetrics.splice(index, 1);
  } else {
    selectedWeatherMetrics.push(weatherMetric);
  }
  weatherMetricCard.classList.toggle("weather-metric-card-selected");
  const numberOfSelectedWeatherMetrics = selectedWeatherMetrics.length;
  if (numberOfSelectedWeatherMetrics < 1) {
    weatherMetricInfo.classList.add("error-text");
    weatherMetricInfo.innerHTML = `You have to choose at least one Weather Metric`;
  } else {
    weatherMetricInfo.classList.remove("error-text");
    weatherMetricInfo.innerHTML = `Please choose at least one Metric`;
  }
};

const onAnalyzeButtonClicked = (e) => {
  console.log("Analyze Button clicked");
};

const onResetButtonClicked = (e) => {
  console.log("Reset Button clicked");
};

// Attach Events to the Weather Location and Metric Cards
const weatherLocationCards = document.querySelectorAll(
  `[id^="${weatherLocationCardSuffix}"]`,
);
weatherLocationCards.forEach((card) => {
  card.addEventListener("click", onWeatherLocationCardClicked);
});

const weatherMetricCards = document.querySelectorAll(
  `[id^="${weatherMetricCardSuffix}"]`,
);
weatherMetricCards.forEach((card) => {
  card.addEventListener("click", onWeatherMetricCardClicked);
});

// Attach Events to the Analyze and Reset Button
const analyzeButton = document.getElementById("analyze-button");
analyzeButton.addEventListener("click", onAnalyzeButtonClicked);
const resetButton = document.getElementById("reset-button");
resetButton.addEventListener("click", onResetButtonClicked);
