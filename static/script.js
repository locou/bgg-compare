$(document).ready(function() {
    $('a#add_user_field').click(function() {
        var lastField = $("#form_build_collection div:last");
        var intId = (lastField && lastField.length && lastField.data("idx") + 1) || 1;
        var add_user_field = $("<div class=\"add_user_field\" id=\"field" + intId + "\"/>");
        add_user_field.data("idx", intId);
        var fName = $("<input type=\"text\" class=\"add_user_input\" name=\"add_user\" placeholder=\"Additional Username\" />");
        var removeButton = $("<a class=\"button reverse-color\"><i class=\"fas fa-user-minus\"></i></a>");
        removeButton.click(function() {
            $(this).parent().remove();
        });
        add_user_field.append(fName);
        add_user_field.append(removeButton);
        $("#form_build_collection").append(add_user_field);
    });

    $('#reset_fields').click(function() {
        icon = $('.checkbox').find('i');
        icon.removeClass("fas fa-check-circle");
        icon.addClass("far fa-circle");
        $('.add_user_field').each(function() {
            $(this).remove();
        });
    });

    $('.checkbox').click(function() {
        var icon = $(this).find('i');
        icon.toggleClass("fas fa-check-circle");
        icon.toggleClass("far fa-circle");
    });
});

function send_user_form() {
    var form = document.getElementById("form_build_collection")
    $('input.add_user_input').each(function( index ) {
    if (this.value == "") {
        this.remove();
    }
    });
    document.getElementById("form_build_collection").submit();
}
