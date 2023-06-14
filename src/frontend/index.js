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
    alert("Your browser doesn't support the XmlHttpRequest object.  Better upgrade to Firefox.");
  };
};


/**
 * Calls the scrape endpoint on the server.
 * @path /run
 * 
 * TODO: Add folders to the body.
 */
function scrape() {
  var xhr = getXmlHttpRequestObject();

  xhr.onreadystatechange = function() {
    if (xhr.readyState == 4 && xhr.status == 200)
      console.log(xhr.responseText);
  };

  var func = document.getElementById("function");
  var category = document.getElementById("category");
  var folders = document.getElementById("folders");

  xhr.open("POST", "http://localhost:3001/run", true);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

  // Parameters.
  const body = {
    function: func.children[func.selectedIndex].text.toLowerCase(),
    category: category.children[category.selectedIndex].text.toLowerCase()
    // folders: folders.children[folders.selectedIndex].text
  };

  xhr.send(JSON.stringify(body));
};
