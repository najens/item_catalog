define(function() {
  const domain = 'localhost:5000/'

  // Create cookie object
  const createCookieObject = function() {
    var cookies = document.cookie.split("; ");
    var cookie = {};
    for (var i = 0; i < cookies.length; i++) {
      var item = cookies[i].split("=");
      cookie[item[0]] = item[1];
    }
    return cookie;
  }

  // Get a specific cookie
  const getCookie = function(name) {
    var cookieValue = null;
    var cookie = createCookieObject();
    if (cookie[name] != undefined) {
      cookieValue = cookie[name];
    }
    return cookieValue;
  }

  // Capitalize first letter of all strings
  const toTitleCase = function(str) {
      return str.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
      });
  }

  // Split url path
  const splitPath = function() {
    var url = $(location).attr('href');
    var pieces = url.split(domain);
    var items = pieces[1].split('/');
    return items;
  }

  // Get item id from url
  const getItemId = function() {
    var items = splitPath();
    var id = items[1];
    return id;
  }

  // Get category name from url
  const getCategoryName = function() {
    var items = splitPath();
    var categoryName = items[0];
    categoryName = decodeURI(categoryName);
    return categoryName;
  }

  // Create object of methods
  var methods = {};
  methods.createCookieObject = createCookieObject
  methods.getCookie = getCookie
  methods.toTitleCase = toTitleCase
  methods.getItemId = getItemId
  methods.getCategoryName = getCategoryName

  return methods;

});
