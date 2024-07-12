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


// Copyright
const copyrightEle = document.getElementById('copyright');
if (copyrightEle) {
    var today_year = TODAY.getFullYear();
    copyrightEle.innerHTML = today_year;
}

const clsSidebarItem = document.getElementsByClassName('sidebar-list-item');
function disableSidebarItemRedirect() {
    document.querySelectorAll('.sidebar-list-item').forEach(function(link){
        link.addEventListener('click', function(e){
            e.preventDefault();
            var url = this.getAttribute('data-url');
            console.log(url);
            if(url){
                fetch(url)
                    .then(response => response.text())
                    .then(data => {
                        document.getElementById('dashboard-main').innerHTML = data;
                    })
            }   
        })
    })
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