// TODO: Fetch Locations via Endpoint
const availableWeatherLocations = ["Chur", "Buchs", "Mels", "St. Gallen", "Zürich"]
const weatherLocationCardSuffix = 'weather-location-card-element'
const selectedWeatherLocations = []
const weatherLocationInfo = document.getElementById("weather-location-info")
weatherLocationInfo.innerHTML = "Please choose exactly two Locations"

const createWeatherLocationCard = (locationName, index) => {
    const weatherCard = `<div class="weather-location-card" data-name="${locationName}" id="${weatherLocationCardSuffix}-${index}">${locationName}</div>`
    return weatherCard
}

const weatherLocationCardsContainer = document.getElementById("weather-location-cards-container")
availableWeatherLocations.map((location, index) => weatherLocationCardsContainer.innerHTML += createWeatherLocationCard(location, index))


// Define Event Handlers for Location Cards
const onWeatherLocationCardClicked = (e) => {
    const weatherLocationCard = e.target
    const weatherLocationName = weatherLocationCard.dataset.name
    console.log(weatherLocationName)
    const alreadySelected = selectedWeatherLocations.indexOf(weatherLocationName) >= 0
    if (alreadySelected && selectedWeatherLocations.length !== 0) {
        weatherLocationCard.classList.remove("weather-location-card-selected")
        selectedWeatherLocations.pop(weatherLocationName)
    } else {
        weatherLocationCard.classList.add("weather-location-card-selected")
        selectedWeatherLocations.push(weatherLocationName)
    }
    console.log(selectedWeatherLocations)
    const numberOfSelectedWeatherLocations = selectedWeatherLocations.length
    if (numberOfSelectedWeatherLocations > 2) {
        weatherLocationInfo.classList.add("error-text")
        weatherLocationInfo.innerHTML = `You have choosen ${numberOfSelectedWeatherLocations} Locations but you have to choose exactly two`
    } else {
        weatherLocationInfo.classList.remove("error-text")
        weatherLocationInfo.innerHTML = `Please choose exactly two Locations`
    }
}


// Attach Events to the Location Cards
const weatherLocationCards = document.querySelectorAll(`[id^="${weatherLocationCardSuffix}"]`)
weatherLocationCards.forEach(card => {
    card.addEventListener("click", onWeatherLocationCardClicked)
})


