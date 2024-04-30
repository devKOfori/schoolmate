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
        let selectedHostel = document.querySelector('#selectedHostelsList');
        let cardEle = btn.closest("col-md-3");
        console.log(selectedHostel);
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