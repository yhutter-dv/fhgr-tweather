// TODO: Fetch via appropriate Endpoints
const availableWeatherLocations = ["Chur", "Buchs", "Mels", "St. Gallen", "Zürich"]
const availableWeatherMetrics = [
    {
        "identifier": "temperature",
        "title": "Temperature",
        "subtitle": "Make a comparison based on Temperature in °C"
    }
]

const selectedWeatherLocations = []
const selectedWeatherMetrics = []

const weatherLocationCardSuffix = 'weather-location-card-element'
const weatherMetricCardSuffix = 'weather-metric-card-element'

const weatherLocationInfo = document.getElementById("weather-location-info")
weatherLocationInfo.innerHTML = "Please choose exactly two Locations"

const weatherMetricInfo = document.getElementById("weather-metric-info")
weatherMetricInfo.innerHTML = "Please choose at least one Metric"

const createWeatherLocationCard = (locationName, index) => {
    const weatherCard = `<div class="weather-location-card" data-name="${locationName}" id="${weatherLocationCardSuffix}-${index}">${locationName}</div>`
    return weatherCard
}

const createWeatherMetricCard = (metric, index) => {
    const title = metric.title
    const subtitle = metric.subtitle
    const identifier = metric.identifier
    const weatherCard = `<div class="weather-metric-card" data-metric="${identifier}" id="${weatherMetricCardSuffix}-${index}"><p class="title">${title}</p><p class="subtitle">${subtitle}</p></div>`
    return weatherCard
}

const weatherLocationCardsContainer = document.getElementById("weather-location-cards-container")
availableWeatherLocations.map((location, index) => weatherLocationCardsContainer.innerHTML += createWeatherLocationCard(location, index))

const weatherMetricCardsContainer = document.getElementById("weather-metric-cards-container")
availableWeatherMetrics.map((metric, index) => weatherMetricCardsContainer.innerHTML += createWeatherMetricCard(metric, index))

// Define Event Handlers 
const onWeatherLocationCardClicked = (e) => {
    const weatherLocationCard = e.target
    const weatherLocationName = weatherLocationCard.dataset.name
    const alreadySelected = selectedWeatherLocations.indexOf(weatherLocationName) >= 0
    if (alreadySelected && selectedWeatherLocations.length !== 0) {
        weatherLocationCard.classList.remove("weather-location-card-selected")
        selectedWeatherLocations.pop(weatherLocationName)
    } else {
        weatherLocationCard.classList.add("weather-location-card-selected")
        selectedWeatherLocations.push(weatherLocationName)
    }
    const numberOfSelectedWeatherLocations = selectedWeatherLocations.length
    if (numberOfSelectedWeatherLocations > 2) {
        weatherLocationInfo.classList.add("error-text")
        weatherLocationInfo.innerHTML = `You have choosen ${numberOfSelectedWeatherLocations} Locations but you have to choose exactly two`
    } else {
        weatherLocationInfo.classList.remove("error-text")
        weatherLocationInfo.innerHTML = `Please choose exactly two Locations`
    }
}


const onWeatherMetricCardClicked = (e) => {
    const weatherMetricCard = e.target
    const weatherMetric = weatherMetricCard.dataset.metric
    const alreadySelected = selectedWeatherMetrics.indexOf(weatherMetric) >= 0
    if (alreadySelected && selectedWeatherLocations.length !== 0) {
        weatherMetricCard.classList.remove("weather-metric-card-selected")
        selectedWeatherMetrics.pop(weatherMetric)
    } else {
        weatherMetricCard.classList.add("weather-metric-card-selected")
        selectedWeatherMetrics.push(weatherMetric)
    }
    const numberOfSelectedWeatherMetrics = selectedWeatherMetrics.length
    if (numberOfSelectedWeatherMetrics < 1) {
        weatherMetricInfo.classList.add("error-text")
        weatherMetricInfo.innerHTML = `You have to choose at least one Weather Metric`
    } else {
        weatherMetricInfo.classList.remove("error-text")
        weatherMetricInfo.innerHTML = `Please choose at least one Metric`
    }
}

// Attach Events to the Weather Location Cards
const weatherLocationCards = document.querySelectorAll(`[id^="${weatherLocationCardSuffix}"]`)
weatherLocationCards.forEach(card => {
    card.addEventListener("click", onWeatherLocationCardClicked)
})

const weatherMetricCards = document.querySelectorAll(`[id^="${weatherMetricCardSuffix}"]`)
weatherMetricCards.forEach(card => {
    card.addEventListener("click", onWeatherMetricCardClicked)
})

