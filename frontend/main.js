// TODO: Fetch Locations via Endpoint
const locations = ["Chur", "Buchs", "Mels"]
const locationCardSuffix = 'location-card-element'
const selectedLocations = []
const selectLocationInfo = document.getElementById("select-location-info")
selectLocationInfo.innerHTML = "Please choose exactly two Locations"

const createLocationCard = (locationName, index) => {
    const locationCard = `<div data-name="${locationName}" id="${locationCardSuffix}-${index}" class="flex items-center justify-center border border-slate-200 size-40 rounded"><p>${locationName}</p></div>`
    return locationCard
}

// Populate the Cards for each Location
const locationCardContainer = document.getElementById("location-card-container")
locations.map((location, index) => locationCardContainer.innerHTML += createLocationCard(location, index))


// Define Event Handlers for Location Cards
const onLocationCardClicked = (e) => {
    const locationCard = e.target
    const clickedLocationName = locationCard.dataset.name
    const alreadySelected = selectedLocations.indexOf(clickedLocationName) >= 0
    if (alreadySelected && selectedLocations.length !== 0) {
        locationCard.classList.remove("bg-slate-500")
        selectedLocations.pop(clickedLocationName)
    } else {
        locationCard.classList.add("bg-slate-500")
        selectedLocations.push(clickedLocationName)
    }
    console.log(selectedLocations)
    const numberOfSelectedLocations = selectedLocations.length
    if (numberOfSelectedLocations > 2) {
        selectLocationInfo.classList.add("text-red-500")
        selectLocationInfo.innerHTML = `You have choosen ${numberOfSelectedLocations} Locations but you have to choose exactly two`
    } else {
        selectLocationInfo.classList.remove("text-red-500")
        selectLocationInfo.innerHTML = `Please choose exactly two Locations`
    }
}


// Attach Events to the Location Cards
const locationCardElements = document.querySelectorAll(`[id^="${locationCardSuffix}"]`)
locationCardElements.forEach(card => {
    card.addEventListener("click", onLocationCardClicked)
})


