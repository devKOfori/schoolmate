var TODAY = new Date();

function addSelectedHostel(hostelId, hostelName, hostelDetails) {
    let selectedHostelsList = document.getElementById("selectedHostelsList");
    let columnDiv = document.createElement("div");
    columnDiv.classList.add("col-md-3");
    let cardDiv = document.createElement("div")
    cardDiv.classList.add("card");
    cardDiv.setAttribute("id", "card-" + hostelId);
    let imgEle = document.createElement("img")
    imgEle.classList.add("card-img-top");
    imgEle.setAttribute("src", "...")
    imgEle.setAttribute("alt", "...")
    let cardBody = document.createElement("div")
    cardBody.classList.add("card-body");
    let cardTitle = document.createElement("h5");
    cardTitle.classList.add("card-title");
    let hostelLink = document.createElement("a");
    hostelLink.href = "/housing/hostels/" + hostelId;
    hostelLink.textContent = hostelName;
    
    // add link to card title
    cardTitle.appendChild(hostelLink);

    let cardText = document.createElement("p");
    cardText.classList.add("card-text");
    cardText.textContent = hostelDetails;
    let checkbox = document.createElement("input");
    checkbox.type = "checkbox"
    checkbox.classList.add("btn-check");
    checkbox.setAttribute("id", "btn-check-" + hostelId);
    checkbox.autocomplete = "off";
    let checkboxLabel = document.createElement("label");
    checkboxLabel.classList.add("btn");
    checkboxLabel.classList.add("btn-outline-dark");
    checkboxLabel.setAttribute("for", "btn-check-" + hostelId);
    checkboxLabel.textContent = "Remove from Application";
    let readMore = document.createElement("a");
    readMore.href = "/housing/hostels/" + hostelId;
    readMore.classList.add("btn");
    readMore.classList.add("btn-dark");
    readMore.textContent = "Read More";
    // build card-body div
    cardBody.appendChild(cardTitle);
    cardBody.appendChild(cardText);
    cardBody.appendChild(checkbox);
    cardBody.appendChild(checkboxLabel);
    cardBody.appendChild(readMore);

    // build card div
    cardDiv.appendChild(imgEle);
    cardDiv.appendChild(cardBody);

    // build column div
    columnDiv.appendChild(cardDiv);

    // build selectedhostels list
    selectedHostelsList.appendChild(columnDiv);
}

function handleHostelSelection(event) {
    let btn = event.target;
    if (event.target.checked) {
        btnLabel = btn.nextElementSibling;
        btnLabel.classList.remove("btn-outline-dark");
        btnLabel.classList.add("btn-success");
        btnLabel.textContent = "Remove from Application";
        let hostelId = btn.id;
        hostelId = hostelId.split("-")[2];
        // get the parent card element
        let card = btn.closest(".card");
        // retrieve hostel information
        cardTitle = card.querySelector(".card-title a")
        hostelName = cardTitle.textContent.trim();
        cardInfo = card.querySelector("p")
        hostelDetails = cardInfo.textContent.trim();
        addSelectedHostel(hostelId, hostelName, hostelDetails);
        // console.log(hostelDetails);
    } else {
        btnLabel.classList.remove("btn-success");
        btnLabel.classList.add("btn-outline-dark");
        btnLabel.textContent = "Add to Application";
        let selectedHostel = document.querySelector('#selectedHostelsList');
        let cardEle = selectedHostel.querySelector("#" + btn.id);
        cardEle = cardEle.parentNode.parentNode.parentNode;
        if (cardEle) {
            cardEle.remove();
        }
    }
}

//
let checkboxes = document.querySelectorAll('.btn-check');
checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener("click", handleHostelSelection);
})

const opnModRT = document.querySelector('.open-mod-roomtype');
const modRT = document.querySelector('#mod-roomtype');
const modRTx = document.querySelector('.mod-roomtype-close');

if (opnModRT && modRT && modRTx){
opnModRT.addEventListener('click', ()=>{
    modRT.style.display = 'block';
})

modRTx.addEventListener('click', ()=>{
    modRT.style.display = 'none';
    
});
}

const rangeInput = document.getElementById('budget');
const rangeInfo = document.getElementById('range-info');


if (rangeInput && rangeInfo){
// rangeMin = rangeInput.min;
// rangeMax = rangeInput.max;
// rangeInfo.textContent = `Min: ${min}, Max: ${max}`;
function updateRangeInfo() {
    rangeMin = rangeInput.min;
    rangeMax = rangeInput.max;

    rangeInfo.textContent = `Min: ${rangeMin}, Max: ${rangeMax}`;
}

updateRangeInfo();

rangeInput.addEventListener('change', updateRangeInfo);
// rangeInput.addEventListener('input', ()=>{
//     rangeMin = rangeInput.min;
//     rangeMax = rangeInput.max;

//     rangeInfo.textContent = `Min: ${min}, Max: ${max}`;

// });
}

function getSystemDate() {
    var date = new Date();
    return date.toDateString();
}

const sysDateEle = document.getElementById("system-date")

function setDashboardDate() {
    if (sysDateEle) {
        sysDateEle.innerHTML = getSystemDate();
    }
}

setDashboardDate();

const registerHostelEle = document.getElementById('btn-register-hostel');
const hostelFormEle = document.getElementById("create-hostel-modal")

// function displayHostelCreationForm() {
//     hostelFormEle.style.display = "block";    
// }

// if (registerHostelEle && hostelFormEle) {
//     registerHostelEle.addEventListener('click', 
//         displayHostelCreationForm());
// }

if (registerHostelEle && hostelFormEle) {
    registerHostelEle.addEventListener('click', ()=>{
        hostelFormEle.style.display = "block";
    });
}

const dca = document.querySelector(".dashboard-content-area");

// Copyright
const copyrightEle = document.getElementById('copyright');
if (copyrightEle) {
    var today_year = TODAY.getFullYear();
    copyrightEle.innerHTML = today_year;
}


const clsSidebarItem = document.getElementsByClassName('sidebar-list-item');
function disableSidebarItemRedirect() {
    const xhr = new XMLHttpRequest();
    const sideBarItems = document.querySelectorAll('.sidebar-list-item')
    if (sideBarItems) {
        
        sideBarItems.forEach(function(link){
            link.addEventListener('click', function(e){
                e.preventDefault();
                // console.log(link);
                const url = link.getAttribute("data-url");
                console.log(url);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === XMLHttpRequest.DONE) {
                        if (xhr.status === 200) {
                            if (dca) {
                                dca.innerHTML = xhr.responseText;
                                // console.log(dca.innerHTML);
                                get_create_floor_form();
                                get_create_block_form();
                                get_create_roomtype_form();
                                get_create_room_form();
                                getCreateHostelForm();
                            } 
                        } else {
                            console.error(`Error: ${xhr.status} - ${xhr.statusText}`);
                        }
                    }
                };
                xhr.open("GET", url);
                xhr.send();
            })
        })
    }
}

function preventDefault(e) {
    e.preventDefault();
}

window.onload = disableSidebarItemRedirect;
// document.addEventListener('DOMContentLoaded', disableSidebarItemRedirect);

document.querySelectorAll('.expand-icon').forEach(expandDiv => {
    const targetSectionID = expandDiv.getAttribute('data-target');
    const sectionContent = document.getElementById(targetSectionID);

    if (expandDiv && sectionContent) {
        expandDiv.addEventListener('click', () => {
            sectionContent.classList.toggle('toggle-section');
        });
    }
});

function get_create_floor_form(){
    const elem = document.getElementById("create-floor-btn");
    // console.log(elem);

    if (elem) {
        const req = new XMLHttpRequest();
        elem.addEventListener("click", function (event) {
            event.preventDefault();
            const nameslug = elem.getAttribute("data-nameslug");
            let url = `/housing/${nameslug}/create-floor/`
            console.log(url);
            req.onreadystatechange = function () {
                if (req.readyState === XMLHttpRequest.DONE) {
                    if (req.status === 200) {
                        if (dca) {
                            dca.innerHTML = req.responseText;
                        }
                    } else {
                        console.error(`Error: ${req.status} - ${req.statusText}`);
                    }
                }
            }
            req.open("GET", url);
            req.send();
        })
    }
}

function get_create_block_form(){
    const elem = document.getElementById("create-block-btn");
    // console.log(elem);

    if (elem) {
        const req = new XMLHttpRequest();
        elem.addEventListener("click", function (event) {
            event.preventDefault();
            const nameslug = elem.getAttribute("data-nameslug");
            let url = `/housing/${nameslug}/create-block/`
            console.log(url);
            req.onreadystatechange = function () {
                if (req.readyState === XMLHttpRequest.DONE) {
                    if (req.status === 200) {
                        if (dca) {
                            dca.innerHTML = req.responseText;
                        }
                    } else {
                        console.error(`Error: ${req.status} - ${req.statusText}`);
                    }
                }
            }
            req.open("GET", url);
            req.send();
        })
    }
}
function get_create_roomtype_form(){
    const elem = document.getElementById("create-roomtype-btn");
    // console.log(elem);

    if (elem) {
        const req = new XMLHttpRequest();
        elem.addEventListener("click", function (event) {
            event.preventDefault();
            const nameslug = elem.getAttribute("data-nameslug");
            let url = `/housing/${nameslug}/create-roomtype/`
            console.log(url);
            req.onreadystatechange = function () {
                if (req.readyState === XMLHttpRequest.DONE) {
                    if (req.status === 200) {
                        if (dca) {
                            dca.innerHTML = req.responseText;
                        }
                    } else {
                        console.error(`Error: ${req.status} - ${req.statusText}`);
                    }
                }
            }
            req.open("GET", url);
            req.send();
        })
    }
}
function get_create_room_form(){
    const elem = document.getElementById("create-room-btn");
    // console.log(elem);

    if (elem) {
        const req = new XMLHttpRequest();
        elem.addEventListener("click", function (event) {
            event.preventDefault();
            const nameslug = elem.getAttribute("data-nameslug");
            let url = `/housing/${nameslug}/create-room/`
            console.log(url);
            req.onreadystatechange = function () {
                if (req.readyState === XMLHttpRequest.DONE) {
                    if (req.status === 200) {
                        if (dca) {
                            dca.innerHTML = req.responseText;
                        }
                    } else {
                        console.error(`Error: ${req.status} - ${req.statusText}`);
                    }
                }
            }
            req.open("GET", url);
            req.send();
        })
    }
}

function getCreateHostelForm() {
    const elem = document.getElementById("create-hostel-lnk");
    if (elem) {
        elem.addEventListener("click", function (event) {
            const req = new XMLHttpRequest();
            event.preventDefault();
            const url = elem.getAttribute("data-url");
            req.onreadystatechange = function () {
                if (req.readyState === XMLHttpRequest.DONE) {
                    if (req.status === 200) {
                        if (dca) {
                            dca.innerHTML = req.responseText;
                        }
                    }else {
                        console.error(`Error: ${req.status} - ${req.statusText}`);
                    }
                }
            }
            req.open("GET", url);
            req.send();
        })

    }
}


function searchHostel(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const params = new URLSearchParams();
    formData.forEach((v, k) => {
        if (k !== "amenities" && k!== "roomtypes") {
            params.append(k, v);
        }
    });

    selectedAmenities = []
    event.target.querySelectorAll("input[name='amenities']:checked").forEach(checkbox => {
        selectedAmenities.push(checkbox.value)
    })

    if (selectedAmenities.length > 0) {
        console.log(selectedAmenities.length);
        params.append('amenities', selectedAmenities.join('||'));
    }

    selectedRoomTypes = [];
    event.target.querySelectorAll("input[name='roomtypes']:checked").forEach(checkbox => {
        selectedRoomTypes.push(checkbox.value)
    })

    if (selectedRoomTypes.length > 0) {
        console.log(selectedRoomTypes.length);
        params.append('roomtypes', selectedRoomTypes.join('||'));
    }

    const queryString = params.toString();
    // console.log(queryString);

    const req = new XMLHttpRequest();
    const url = "/search-hostel?" + queryString
    const hostelListContainer = document.querySelector(".list-hostels-container");
    req.open("GET", url);
    req.onreadystatechange = function () {
        if (req.readyState === XMLHttpRequest.DONE) {
            if (req.status === 200) {
                if (hostelListContainer) {
                    hostelListContainer.innerHTML = req.responseText;
                    // console.log(req.responseText);

                    // loading selected hostels from localStorage
                    loadSelectedHostels();

                    // function to display add to application button on hostel card
                    displayAddHostelBtn();
                } 
            }else {
                console.log(`${req.status} - ${req.statusText}`);
            }
        }
    }
    req.send();
}

document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("search_form_ID");
    if (searchForm) {
        searchForm.addEventListener("submit", function (event) {
            searchHostel(event);
        });
    }

    // call to load selected hostels from localStorage
    loadSelectedHostels();

    // function to display add to application button on hostel card
    displayAddHostelBtn();

    // call to display selected hostels on hostel application form
    addSelectedHostelsToApplicationForm();

    // call to handle saving hostel application
    processHostelApplication();
})

// function to load selected hostels from localStorage
function loadSelectedHostels() {
    const selectedHostels = JSON.parse(localStorage.getItem("selectedHostels"));
    if (selectedHostels) {
        selectedHostels.forEach(function (hostelInfo) {
            hostelInfoArray = hostelInfo.split("||");
            hostelID = hostelInfoArray[0]
            console.log(hostelID);
            const card = document.getElementById(`${hostelID}`)
            if (card) {
                const showSelection = card.querySelector(".selected-hostel");
                const addSelection = card.querySelector(".add-to-application-lnk");
                if (showSelection && addSelection) {
                    card.classList.add("green-box-shadow");
                    showSelection.classList.add("show-selection");
                    updateHoverText(card, showSelection, addSelection);
                }
            }
        });
        displayProceedToApplicationBtn(selectedHostels);
    }
}


// Adding hostels to applications
function displayAddHostelBtn() {
    const cardHeadEle = document.querySelectorAll(".card-head");
    if (cardHeadEle) {
        cardHeadEle.forEach(function (cardHead) {
            cardHead.addEventListener("mouseover", function () {
                const overlayEle = cardHead.querySelector(".hover-overlay");
                const overlayContentEle = cardHead.querySelector(".hover-overlay-content");
                if (overlayEle && overlayContentEle) {
                    overlayEle.style.display = "block";
                    overlayContentEle.style.display = "block";
                }
            });
            
            cardHead.addEventListener("mouseout", function () {
                const overlayEle = cardHead.querySelector(".hover-overlay");
                const overlayContentEle = cardHead.querySelector(".hover-overlay-content");
                if (overlayEle && overlayContentEle) {
                    overlayEle.style.display = "none";
                    overlayContentEle.style.display = "none";
                }
                
            })
        })
        selectAddedHostel();
    }
}

// function to select add hostel when add to application is clicked
function selectAddedHostel() {
    ataEle = document.querySelectorAll(".add-to-application-lnk");
    // console.log(ataEle);
    if (ataEle) {
        ataEle.forEach(function (elem) {
            elem.addEventListener("click", function (event) {
                event.preventDefault();
                const hostelID = elem.getAttribute("data-hostel-id");
                const hostelCard = document.getElementById(`${hostelID}`);
                hostelCard.classList.toggle("green-box-shadow");
                const selectedHostel = hostelCard.querySelector(".selected-hostel");
                selectedHostel.classList.toggle("show-selection");
                updateLocalStorage(hostelCard);
                const headImg = hostelCard.querySelector(".card-head-image");
                headImg.addEventListener("mouseover", function () {
                    updateHoverText(hostelCard, selectedHostel, elem);
                })
            });
        });
    }
}

// function to toggle hover text
function updateHoverText(card, selectedHostel, elem) {
    if (card.classList.contains("green-box-shadow") && selectedHostel.classList.contains("show-selection")) {
        elem.innerHTML = "<span>Remove Selection</span>"
    } else{
        elem.innerHTML = "<span>Add Selection</span>"
    }
}

// function to update selectedHostels stored in localStorage
function updateLocalStorage(card) {
    const hostelID = card.getAttribute("data-id");
    const hostelName = card.getAttribute("data-hostel-name");
    const hostelInfo = `${hostelID}||${hostelName}`
    console.log(hostelInfo);
    let selectedHostels;
    try {
        selectedHostels = JSON.parse(localStorage.getItem("selectedHostels"));
    } catch (e) {
        console.error("Error parsing localStorage data:", e);
        selectedHostels = [];
    }
    // Ensure selectedHostels is an array
    if (!Array.isArray(selectedHostels)) {
        selectedHostels = [];
    }
    const showSelection = card.querySelector(".selected-hostel");
    const addSelection = card.querySelector(".add-to-application-lnk");
    if (card.classList.contains("green-box-shadow") && showSelection.classList.contains("show-selection")) {
        if (!selectedHostels.includes(hostelInfo)) {
            selectedHostels.push(hostelInfo);
        }
    } else {
        selectedHostels = selectedHostels.filter(info => info !== hostelInfo);
    }
    localStorage.setItem("selectedHostels", JSON.stringify(selectedHostels));

    displayProceedToApplicationBtn(selectedHostels);
}

// function to display "continue to application" button
function displayProceedToApplicationBtn(selectedHostels) {
    const ctp = document.querySelector(".proceed-to-application");
    // if (ctp && selectedHostels.length > 0) {
    //     ctp.style.display = "block";
    // } else {
    //     ctp.style.display = "none";
    // }
    if (ctp) {
        if (selectedHostels.length > 0) {
            ctp.style.display = "block";
        } else {
            ctp.style.display = "none";
        }
    }
    // proceedToApplication();
}

// function to redirect user to application form
function proceedToApplication() {
    const ptaBtn = document.querySelector(".proceed-to-application");
    if (ptaBtn) {
        ptaBtn.addEventListener("click", function (event) {
            event.preventDefault();
        })
    }
}

// this function loads the selected hostels from localStorage and puts them on the application form
function addSelectedHostelsToApplicationForm() {
    const applicationFrm = document.querySelector(".application-form");
    let roomtypeStrings = "";
    if (applicationFrm) {
        const hostelsHolder = applicationFrm.querySelector(".tenant-hostels");
        if (hostelsHolder) {
            const rtHidden = document.querySelector(".roomtypes-hidden");
            if (rtHidden) {
                roomtypeStrings = rtHidden.textContent;
                roomtypeStrings = roomtypeStrings.replace(/\s/g, "");
                // console.log(roomtypeStrings);
            }
            let hostelsHTML = "";
            const selectedHostels = JSON.parse(localStorage.getItem("selectedHostels"));
            if (selectedHostels) {
                if (roomtypeStrings !== "") {
                    rtOptions = createRoomtypeDropdown(roomtypeStrings);
                }
                selectedHostels.forEach(function (hostelInfo) {
                    hostelInfoArray = hostelInfo.split("||");
                    hostelID = hostelInfoArray[0];
                    hostelName = hostelInfoArray[1];
                    hostelsHTML = hostelsHTML + `
                    <div class="application-form-group application-selected-hostels flex">
                        <input type="text" name="hostel_${hostelID}" id="${hostelID}" value="${hostelName}" data-hostel-id="${hostelID}">
                        <select name="roomtype_${hostelID}" id="roomtype">
                            ${rtOptions}
                        </select>
                    </div>
                    `
                });
            }
            hostelsHolder.innerHTML = hostelsHTML;
        }
    }

}

// this function creates the dropdown options for room types on the hostel application form
function createRoomtypeDropdown(roomtypeString) {
    rtOptions = "<option value='------'>Select Roomtype</option>";
    rtsArray = roomtypeString.split("~~");
    rtsArray.forEach(function (roomtype) {
        if (roomtype !== "") {
            rtArray = roomtype.split("||");
            rtOptions += `
            <option value="${rtArray[0]}">${rtArray[1]}</option>
            `
        }
    });
    return rtOptions;
}

// this function handles the hostel application submission
function processHostelApplication() {
    const applicationFrm = document.getElementById("application-form");
    if (applicationFrm) {
        applicationFrm.addEventListener("submit", function (event) {
            // event.preventDefault();
            console.log("here...");
            localStorage.clear();
        });
    }
}