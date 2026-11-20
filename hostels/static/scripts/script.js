console.log("Hostel Finder loaded!");

function checkSearch() {
    var q = document.getElementById("searchBox").value;
    if (q == "") {
        alert("Please type a location to search.");
        return false;
    }
    return true;
}
