$(document).ready(function() {

    $('.checkbox').click(function() {
        var icon = $(this).find('i');
        icon.toggleClass("fas fa-check-circle");
        icon.toggleClass("far fa-circle");
    });

    $('#toggle_sort_filter_block').click(function () {
        $('#sort_filter_block').slideToggle(100);
        $(this).find("i").toggleClass("fa-sort-up").toggleClass("fa-sort-down");
        $(this).find("span").toggle();
    });

    var items = $('div#game_container'), item = items.children('div.wrapper');
    $('.toggle_tag').not('.deactivated').click(function() {
        var button = $(this);
        var button_icon = button.find('i');
        var tag = $(this).data('tag');

        var tag_group = $(this).data('tag_group');

        var class_show = "fa-eye"
        var class_hidden = "fa-eye-slash"
        var o = button.hasClass("hidden") ? "show" : "hidden";
        var oi = button_icon.hasClass(class_hidden) ? class_show : class_hidden;
        button_icon.removeClass(class_show).removeClass(class_hidden).addClass(oi)
        button.removeClass("show").removeClass("hidden").addClass(o);

        var button_value = button.find("span.toggle_value").text();
        if (button_value === "") {
            $("div[data-"+tag+"='1']").each(function() {

                if(o == "hidden") {
                if($(this).data("hidden_by") == "") {
                    $(this).hide();
                    $(this).data("hidden_by", tag_group);
                    $("#count_items").text(item.filter(":visible").length);
                }
                } else {
                if($(this).data("hidden_by") == tag_group) {
                    $(this).show();
                    $(this).data("hidden_by", "");
                    $("#count_items").text(item.filter(":visible").length);
                }
                }
            });
        } else {
            if(o == "hidden") {
                $("div[data-"+tag+"]").filter(function() {
                    return $(this).data(tag) < button_value;
                }).each(function() {
                    if($(this).data("hidden_by") == "") {
                        $(this).hide();
                        $(this).data("hidden_by", tag_group);
                        $("#count_items").text(item.filter(":visible").length);
                    }
                });
            } else {
                $("div[data-"+tag+"]").each(function() {
                    if($(this).data("hidden_by") == tag_group) {
                        $(this).show();
                        $(this).data("hidden_by", "");
                        $("#count_items").text(item.filter(":visible").length);
                    }
                });
            }
        }
    });
    $('.sort').not('.deactivated').click(function () {
        var button = $(this);
        var button_icon = button.find('i');
        var class_neutral = "fa-sort"
        var class_asc = "fa-sort-up"
        var class_desc = "fa-sort-down"
        var sort_by = $(this).data('sort');
        var o = button.hasClass("desc") ? "asc" : "desc";
        var oi = button_icon.hasClass(class_desc) ? class_asc : class_desc;
        $('div.sort').each(function() {
            $(this).removeClass("asc").removeClass("desc");
            $(this).find('i').removeClass(class_asc).removeClass(class_desc).addClass(class_neutral)
        })
        button.addClass(o);
        button_icon.addClass(oi);
        item.detach().sort(function(a, b) {
            var astts = $(a).data(sort_by);
            var bstts = $(b).data(sort_by);

            if (astts == "None") {
                return 1;
            }
            if (bstts == "None") {
                return -1;
            }
            if (astts > bstts) {
                return button.hasClass("asc") ? 1 : -1;
            }
            if (astts < bstts) {
                return button.hasClass("asc") ? -1 : 1;
            }
            return 0;
        });
        items.append(item);
    });



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
