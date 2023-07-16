/*
 * Author: jon-chow
 * Created: 2023-06-13
 * Last Modified: 2023-07-15
 */

const SERVER = "http://localhost:3001";


/* -------------------------------------------------------------------------- */
/*                                  FUNCTIONS                                 */
/* -------------------------------------------------------------------------- */

/**
 * Returns an XMLHttpRequest object.
 */
function getXmlHttpRequestObject() {
	if (window.XMLHttpRequest)
		return new XMLHttpRequest();
	else if (window.ActiveXObject)
		return new ActiveXObject("Microsoft.XMLHTTP");
	else
		alert("Your browser doesn't support the XmlHttpRequest object.");
};


/**
 * Changes the image of the dropdown for the specified dropdown.
 * @param {String} dropdownId - Id of the dropdown.
 * @param {String} image - Image name.
 */
function changeDropdownImage(dropdownId, image) {
  let dropdown = document.getElementById(dropdownId + "-dropdown");
  let dropdownImage = dropdown.getElementsByTagName("img")[0];
  dropdownImage.src = `images/${image}.webp`;
};


/**
 * Adds options to the functions select.
 * @param {Array} folderNames - Array of folder names.
 */
function addFolderOptions(folderNames) {
  let folders = document.getElementById("folders");

  for (var i = 0; i < folderNames.length; i++) {
    let option = document.createElement("option");
    option.text = folderNames[i];
    option.value = folderNames[i].toLowerCase();
    folders.add(option);
  };
};


/**
 * Updates the session storage with folder names for a category. \
 * @param {Array} folders - Array of folder names.
 * @param {String} category - Category name.
 */
function updateFolders(folders, category) {
  let foldersObj = [];
  for (var i = 0; i < folders.length; i++)
    foldersObj.push(folders[i]);

  // Create object to store in session storage.
  let obj = {};
  let fromSession = JSON.parse(sessionStorage.getItem("folderNames"));
  if (fromSession === null) {
    obj[category] = foldersObj;
  } else {
    obj = fromSession;
    obj[category] = foldersObj;
  };

  sessionStorage.setItem("folderNames", JSON.stringify(obj));
};


/**
 * Checks if the user has selected a category. \
 * Enables the folders select if true.
 */
function checkEnableFolders() {
	let category = document.getElementById("category");
	let folders = document.getElementById("folders");

  let selection = category.children[category.selectedIndex].text.toLowerCase();

	folders.disabled = selection === "none";

  if (folders.disabled)
    folders.innerHTML = "";
  else
    populateFolders(selection);
  
  changeDropdownImage("category", selection);
};


/* -------------------------------------------------------------------------- */
/*                                  REQUESTS                                  */
/* -------------------------------------------------------------------------- */

/**
 * Gathers the possible functions from the server. \
 * Populates the folders select with folders from the selected category.
 * @path /get
 * @async
 */
async function populateFolders(category) {
  let fromSession = JSON.parse(sessionStorage.getItem("folderNames"));

  if (fromSession === null || fromSession[category] === undefined) {
    var xhr = getXmlHttpRequestObject();

    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status == 200) {
        let res = JSON.parse(xhr.responseText);
        let folders = document.getElementById("folders");

        // Refresh folders select.
        folders.innerHTML = "";
        updateFolders(res.message, category);
        addFolderOptions(res.message);
      }
    };

    xhr.open("POST", `${SERVER}/get`, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // Set parameters.
    const body = {
      category: category.toLowerCase(),
    };

    xhr.send(JSON.stringify(body));
  } else {
    let folders = document.getElementById("folders");
    folders.innerHTML = "";
    addFolderOptions(fromSession[category]);
  };
};


/**
 * Calls the scrape endpoint on the server.
 * @path /run
 */
function scrape() {
  var xhr = getXmlHttpRequestObject();

  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4 && xhr.status == 200) {
      let res = JSON.parse(xhr.responseText);
      console.log(res.message);
    };
  };

  xhr.open("POST", `${SERVER}/run`, true);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

  let func = document.getElementById("function");
	let category = document.getElementById("category");
	let folders = document.getElementById("folders");

	let selectedFolders = [];
	for (var i = 0; i < folders.length; i++)
		if (folders[i].selected) selectedFolders.push(folders[i].text);

	// Set parameters.
	const body = {
		function: func.children[func.selectedIndex].text.toLowerCase(),
		category: category.children[category.selectedIndex].text.toLowerCase(),
		folders: selectedFolders,
	};

	xhr.send(JSON.stringify(body));
};
