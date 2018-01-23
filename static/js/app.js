// Get items from html
var navButton = document.getElementById("nav-btn");
var navList = document.getElementById("nav-lst");
var navListItems = navList.getElementsByTagName("a");

// Display nav list on click
navButton.addEventListener("click", function() {
    navList.classList = navList.classList == "nav-list flex-col" ? "nav-list hidden" : "nav-list flex-col";
});
// Hide nav list when nav list item is clicked
for (var i = 0; i < navListItems.length; i++) {
    navListItems[i].addEventListener("click", function() {
        navList.classList = "nav-list hidden";
    });
}
