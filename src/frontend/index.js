/*
 * Author: jon-chow
 * Created: 2023-06-13
 * Last Modified: 2023-06-13
 */


/**
 * Returns an XMLHttpRequest object.
 */
getXmlHttpRequestObject = function() {
  if (window.XMLHttpRequest) {
    return new XMLHttpRequest();
  } else if (window.ActiveXObject) {
    return new ActiveXObject("Microsoft.XMLHTTP");
  } else {
    alert("Your browser doesn't support the XmlHttpRequest object. Better upgrade to Firefox.");
  };
};


/**
 * Gathers the possible functions from the server. \
 * Populates the folders select with folders from the selected category.
 * @path /get
 */
async function populateFolders(category) {
	var xhr = getXmlHttpRequestObject();

	xhr.onreadystatechange = function () {
		if (xhr.readyState == 4 && xhr.status == 200) {
			let res = JSON.parse(xhr.responseText);
      let folders = document.getElementById("folders");

      // Clear folders.
      folders.innerHTML = "";

      // Populate folders.
      for (var i = 0; i < res.message.length; i++) {
        let option = document.createElement("option");
        option.text = res.message[i];
        option.value = res.message[i].toLowerCase();
        folders.add(option);
      };
		}
	};

	xhr.open("POST", "http://localhost:3001/get", true);
	xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

	// Set parameters.
	const body = {
		category: category.toLowerCase(),
	};

	xhr.send(JSON.stringify(body));
};


/**
 * Checks if the user has selected a category. \
 * Enables the folders select if true.
 */
function checkEnableFolders() {
	let category = document.getElementById("category");
	let folders = document.getElementById("folders");

	folders.disabled = (category.children[category.selectedIndex].text.toLowerCase() === "none");

  if (!folders.disabled) {
    populateFolders(category.children[category.selectedIndex].text);
  } else {
    folders.innerHTML = "";
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

  xhr.open("POST", "http://localhost:3001/run", true);
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
