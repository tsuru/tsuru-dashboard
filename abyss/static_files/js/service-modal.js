$("body").on("click", ".expand-service-list", function(e) {
    var html = $(e.target).parent(".widget").html();
    $(".modal").find(".target").html(html);
    $(".modal").find(".btn").remove();
    $(".modal").find(".expand-service-list").remove();

    $(".modal").modal({
        fadeDuration: 200,    
    });
})
$(".widget").each(function(index, item) {
    if (($(item).height() - $(item).find('.title').height()) < $(item).find("ul").outerHeight()) {
        $(item).append("<a class='expand-service-list'>see all</a>");
    }
});
