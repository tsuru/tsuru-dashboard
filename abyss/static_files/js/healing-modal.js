$(".error").on("click", function(){
    var text = $(this).find(".to-error").text();
    $(".modal").find('p').text(text);
    $(".modal").modal();
});
