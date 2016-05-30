jQuery(document).ready(function() {

  const recipesPerPage = getRecipesPerPageNumber();
  var $recipesNum = $('.recipe-icon').length;
  if ($recipesNum < recipesPerPage) {
    $('.upload-items-button-container').remove();
  }

  function getRecipesPerPageNumber() {
    var result;
    $.ajax({
      type: "GET",
      url: "/recipes/",
      cache: false,
      async: false,
      success: function(data) {
        result = data;
      }
    });
    return result;
  }

  function uploadItemsButtonHandler() {
    var $recipesNum = $('.recipe-icon').length;
    $.get("/recipes/", {recipesNum: $recipesNum}, function(data) {
        $('.recipe-list').append(data);
        if ($('.recipe-icon').length - $recipesNum <= recipesPerPage) {
          $('.upload-items-button-container').remove();
        }
    });
  }

  $('#upload-items-button').click(uploadItemsButtonHandler);
});
