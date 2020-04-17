$("document").ready(function() {
    $("#searchCharBtn").click(function() {
        var query = $("#searchChar").val();
        $.ajax({
            url: "/search",
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify({'query': query})
        }).done(function(data) {
            console.log(data);
        });
    });
});
