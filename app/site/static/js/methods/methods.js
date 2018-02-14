/**
 * @description setup file to be used as requirejs module
 * @return object of helper methods to define methods module
 */
define(function() {

    /**
     * @description create cookie object from items in cookie header
     * @return return cookie object
     */
    const createCookieObject = function() {
        const cookies = document.cookie.split("; ");
        const cookie = {};
        for (let i = 0; i < cookies.length; i++) {
            const item = cookies[i].split("=");
            cookie[item[0]] = item[1];
        }
        return cookie;
    }

    /**
     * @description get a specific cookie
     * @param {string} key cookie key name
     * @return cookie value
     */
    const getCookie = function(key) {
        var cookieValue = null;
        const cookie = createCookieObject();
        if (cookie[key] != undefined) {
            cookieValue = cookie[key];
        }
        return cookieValue;
    }

    /**
     * @description capitalize first letter of all words in string
     * @param {string} str
     * @return string with capitalized words
     */
    const toTitleCase = function(str) {
        return str.replace(/\w\S*/g, function(txt){
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        });
    }

    /**
     * @description split url into a list of items
     * @return list of items
     */
    const splitPath = function() {
        const domain = "localhost:5000/"
        const url = $(location).attr("href");
        const pieces = url.split(domain);
        const items = pieces[1].split("/");
        return items;
    }

    /**
     * @description get item id from url
     * @return item id
     */
    const getItemId = function() {
        const items = splitPath();
        const id = items[1];
        return id;
    }

    /**
     * @description get category name from url
     * @return category name
     */
    const getCategoryName = function() {
        const items = splitPath();
        let categoryName = items[0];
        categoryName = decodeURI(categoryName);
        return categoryName;
    }

    // Create object of methods
    const methods = {
        createCookieObject: createCookieObject,
        getCookie: getCookie,
        toTitleCase: toTitleCase,
        getItemId: getItemId,
        getCategoryName: getCategoryName
    };

    // Return object of methods
    return methods;
});
