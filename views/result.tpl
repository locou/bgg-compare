<html>
% include('head.tpl', title='bgg-compare | '+main_user['username']+'s collection')
% from bgg_collection import make_int, make_float
<body>
<button class="button" id='button-scroll-up'><i class="fas fa-angle-double-up"></i> Scroll back up</button>
<div class="container">
    <div class="wrapper_loading_status">
        % for key, user in enumerate(loading_status):
        % if user['status'] == 1:
        % if key == 0:
        <div class="grid_header block-primary">
            <h1>
                <i class="fas fa-dice-d20"></i>
                Displaying the collection of
                <a href="https://boardgamegeek.com/user/{{user['username']}}">
                    {{user['username']}}
                </a>
            </h1>
            <div>
                <i class="fas fa-cubes"></i> {{"?" if user['total_items'] is None else user['total_items']}} games with
                <i class="fas fa-star-half-alt"></i> {{"?" if user['total_items_rating'] is None else user['total_items_rating']}} ratings and
                <i class="far fa-comment"></i> {{"?" if user['total_items_comment'] is None else user['total_items_comment']}} comments
                <em class="tooltip" data-tooltip="Cache last updated">
                    ({{user['updated_at']}})
                </em>
                <p><a href="/">Back to Main Page</a></p>
            </div>
        </div>

        <div class="grid_add_user block-primary">
            <p>Add additional users to the current collection.</p>
            <form id="form_build_collection" method="post" action="/process" onsubmit="send_user_form()">
                % for etag in exclude_tags:
                <input type="text" name="exclude" value="{{etag}}" hidden>
                % end
                <input type="text" name="main_user" value="{{main_user['username']}}" hidden>
                % for key, a_user in enumerate(loading_status):
                % if key != 0:
                <input type="text" class="add_user_input" name="add_user" value="{{a_user['username']}}" hidden>
                % end
                % end
                <input id="include_buddies" type="checkbox" name="include_buddies" hidden>
                <label for="include_buddies" class="button checkbox reverse-color">
                    <i class="far fa-circle"></i> Include 5 random Buddies
                </label>
                <input id="include_random_users" type="checkbox" name="include_random_users" hidden>
                <label for="include_random_users" class="button checkbox reverse-color">
                    <i class="far fa-circle"></i> Include 5 random, cached Users
                </label>
                <p>
                    <button class="button reverse-color" type="submit"><i class="fas fa-cubes"></i> Submit</button>
                    <a id="add_user_field" class="button reverse-color"><i class="fas fa-user-plus"></i> Add User</a>
                </p>
            </form>
        </div>
        % else:
        <div class="grid_title">
            <a href="https://boardgamegeek.com/user/{{user['username']}}" class="tooltip" data-tooltip="open {{user['username']}}s boardgamegeek profile"><i class="fas fa-user"></i> {{user['username']}}</a>
            <em class="tooltip" data-tooltip="Cache last updated">({{user['updated_at']}})</em>
            <a class="button icon-only tooltip" href="{{user['collection_url']}}" data-tooltip="switch to {{user['username']}}s collection"><i class="fas fa-people-arrows"></i></a>
            <a class="button icon-only tooltip" href="{{user['remove_collection_url']}}" data-tooltip="remove {{user['username']}}s collection"><i class="fas fa-times"></i></a>
        </div>
        <div class="grid_collection">
            <span class="tooltip" data-tooltip="matched {{user['match_items']}} of {{user['total_items']}} games">
                <i class="fas light fa-cubes"></i>
                % if user['total_items'] > 0:
                <b>{{user['match_items']}}</b> / {{user['total_items']}}
                % else:
                0
                % end
            </span>
            <span class="tooltip" data-tooltip="providing {{user['match_items_rating']}} of {{user['total_items_rating']}} ratings">
                <i class="fas light fa-star-half-alt"></i>
                % if user['total_items_rating'] > 0:
                <b>{{user['match_items_rating']}}</b> / {{user['total_items_rating']}}
                % else:
                0
                % end
            </span>
            <span class="tooltip" data-tooltip="providing {{user['match_items_comment']}} of {{user['total_items_comment']}} comments">
                <i class="far light fa-comment"></i>
                % if user['total_items_comment'] > 0:
                <b>{{user['match_items_comment']}}</b> / {{user['total_items_comment']}}
                % else:
                0
                % end
            </span>
        </div>
        <div class="grid_rating">
            % if user['mean_diff_rating'] is not None:
            mean difference in ratings: <div class="tag tooltip rating diff-rating-{{make_int(user['mean_diff_rating'])}}" data-tooltip="mean between all differences in ratings">{{user['mean_diff_rating']}}</div>
            % else:
            <span class="error">No ratings to compare</span>
            % end
        </div>
        <div class="grid_diff_ratings">
            % for diff in user['diff_ratings']:
            <a href="#{{diff['title']}}"><div class="tag tooltip rating diff-rating-{{make_int(diff['diff_rating'])}}" data-tooltip="{{diff['title']}}" ></div></a>
            % end
        </div>
        % end
        % elif "errors" in user:
        <div class="grid_message">Error loading "{{user['username']}}" <a class="button icon-only tooltip" href="{{user['remove_collection_url']}}" data-tooltip="remove {{user['username']}}s collection"><i class="fas fa-times"></i></a>: <span class="error">{{user['errors']}}</span></div>
        % elif "message" in user:
        <div class="grid_message tooltip">Loading <a href="https://boardgamegeek.com/user/{{user['username']}}" data-tooltip="open {{user['username']}}s boardgamegeek profile">{{user['username']}}</a>: <span>{{user['message']}}</span></div>
        % end
        % end
    </div>
</div>
% if main_user['status'] == 1:
<div id="sort_container" class="container">
    <div class="block block-primary">
        <h2><i class="fas fa-cubes"></i> Showing <span id="count_items">{{main_user['match_items']}}</span> games</h2>
        <div class="clickable" id="toggle_sort_filter_block"><i class="fas fa-sort-up"></i> <span>Collapse</span><span style="display:none;">Expand</span></div>
        <div>
            <i class="fas fa-star-half-alt"></i> <span id="count_ratings">{{main_user['match_items_rating']}}</span> ratings and
            <i class="far fa-comment"></i> <span id="count_comments">{{main_user['match_items_comment']}}</span> comments
            from <i class="fas fa-user"></i> {{main_user['username']}}
        </div>
    </div>
    <div id="sort_filter_block">
        <h3><i class="fas fa-filter"></i> Hard Filter</h3>
        <em>Exclude games by type, tags or <i class="fas light fa-user"></i> {{main_user['username']}}s stats. Select the checkboxes below and hit Submit. This will apply the filter, refresh the page and affect calculations (ex: mean difference)</em>
            <form id="form_hard_filter" method="post" action="/process">
                <input type="text" name="main_user" value="{{main_user['username']}}" hidden>
                % for key, a_user in enumerate(loading_status):
                % if key != 0:
                <input type="text" class="add_user_input" name="add_user" value="{{a_user['username']}}" hidden>
                % end
                % end
                <div>
                    Exclude by type
                    <script>
    $(document).ready(function() {
        function set_checkbox(button) {
            var button_label = "#"+button+"_label";
            $(button_label).click();
        }
                    % from bottle import request
                    % for param in exclude_tags:
        set_checkbox("exclude_tag_{{param}}");
                    % end
    });
                    </script>
                    <input id="exclude_tag_boardgame" type="checkbox" name="exclude_tag_boardgame" hidden>
                    <label for="exclude_tag_boardgame" id="exclude_tag_boardgame_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> Boardgame
                    </label>
                    <input id="exclude_tag_boardgameexpansion" type="checkbox" name="exclude_tag_boardgameexpansion" hidden>
                    <label for="exclude_tag_boardgameexpansion" id="exclude_tag_boardgameexpansion_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> Boardgame Expansion
                    </label>
                </div>
                <div>
                    Exclude by <i class="fas light fa-user"></i> {{main_user['username']}}s tags
                    <input id="exclude_tag_own" type="checkbox" name="exclude_tag_own" hidden>
                    <label for="exclude_tag_own" id="exclude_tag_own_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> own
                    </label>
                    <input id="exclude_tag_prevowned" type="checkbox" name="exclude_tag_prevowned" hidden>
                    <label for="exclude_tag_prevowned" id="exclude_tag_prevowned_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> prev. owned
                    </label>
                    <input id="exclude_tag_preordered" type="checkbox" name="exclude_tag_preordered" hidden>
                    <label for="exclude_tag_preordered" id="exclude_tag_preordered_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> preordered
                    </label>
                    <input id="exclude_tag_wishlist1" type="checkbox" name="exclude_tag_wishlist1" hidden>
                    <label for="exclude_tag_wishlist1" id="exclude_tag_wishlist1_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> wishlist 1
                    </label>
                    <input id="exclude_tag_wishlist2" type="checkbox" name="exclude_tag_wishlist2" hidden>
                    <label for="exclude_tag_wishlist2" id="exclude_tag_wishlist2_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> wishlist 2
                    </label>
                    <input id="exclude_tag_wishlist3" type="checkbox" name="exclude_tag_wishlist3" hidden>
                    <label for="exclude_tag_wishlist3" id="exclude_tag_wishlist3_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> wishlist 3
                    </label>
                    <input id="exclude_tag_wishlist4" type="checkbox" name="exclude_tag_wishlist4" hidden>
                    <label for="exclude_tag_wishlist4" id="exclude_tag_wishlist4_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> wishlist 4
                    </label>
                    <input id="exclude_tag_wishlist5" type="checkbox" name="exclude_tag_wishlist5" hidden>
                    <label for="exclude_tag_wishlist5" id="exclude_tag_wishlist5_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> wishlist 5
                    </label>
                    <input id="exclude_tag_fortrade" type="checkbox" name="exclude_tag_fortrade" hidden>
                    <label for="exclude_tag_fortrade" id="exclude_tag_fortrade_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> for trade
                    </label>
                    <input id="exclude_tag_want" type="checkbox" name="exclude_tag_want" hidden>
                    <label for="exclude_tag_want" id="exclude_tag_want_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> want
                    </label>
                    <input id="exclude_tag_wanttoplay" type="checkbox" name="exclude_tag_wanttoplay" hidden>
                    <label for="exclude_tag_wanttoplay" id="exclude_tag_wanttoplay_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> want to play
                    </label>
                    <input id="exclude_tag_wanttobuy" type="checkbox" name="exclude_tag_wanttobuy" hidden>
                    <label for="exclude_tag_wanttobuy" id="exclude_tag_wanttobuy_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> want to buy
                    </label>
                    <input id="exclude_tag_notag" type="checkbox" name="exclude_tag_notag" hidden>
                    <label for="exclude_tag_notag" id="exclude_tag_notag_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> <em>without tag</em>
                    </label>
                </div>
                <div>
                    Exclude by <i class="fas light fa-user"></i> {{main_user['username']}}s stats
                    <input id="exclude_tag_norating" type="checkbox" name="exclude_tag_norating" hidden>
                    <label for="exclude_tag_norating" id="exclude_tag_norating_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> without rating
                    </label>
                    <input id="exclude_tag_nocomment" type="checkbox" name="exclude_tag_nocomment" hidden>
                    <label for="exclude_tag_nocomment" id="exclude_tag_nocomment_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> without comment
                    </label>
                    <input id="exclude_tag_noplays" type="checkbox" name="exclude_tag_noplays" hidden>
                    <label for="exclude_tag_noplays" id="exclude_tag_noplays_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> without plays
                    </label>
                </div>
                <div>
                    <button class="button" type="submit"><i class="fas fa-cubes"></i> Submit</button>
                    <button id="reset_fields" class="button reverse-color" type="reset"><i class="fas fa-redo-alt"></i> Reset</button>
                </div>

            </form>
        % if main_user['status'] == 1 and main_user['match_items'] > 0:
        <h3><i class="fas fa-filter"></i> Soft Filter</h3>
        <em>Show/Hide games without reloading the page. Tags will be disabled, if they're already filtered by the Hard Filter</em>
        <div>
            Toggle by type
            <div class="toggle_tag tag{{' disabled' if 'boardgame' in exclude_tags or 'boardgameexpansion' in exclude_tags else ''}}" data-tag="boardgame_tag_bg" data-tag_group="type">Boardgame<i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' disabled' if 'boardgame' in exclude_tags or 'boardgameexpansion' in exclude_tags else ''}}" data-tag="boardgame_tag_bgexp" data-tag_group="type">Boardgame Expansion<i class="fas fa-eye"></i></div>
        </div>
        <div>
            Toggle by <i class="fas light fa-user"></i> {{main_user['username']}}s tags
            <div class="toggle_tag tag{{' disabled' if 'own' in  exclude_tags else ''}}" data-column="20">own <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' disabled' if 'prevowned' in  exclude_tags else ''}}" data-column="22">prev. owned <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' disabled' if 'preordered' in  exclude_tags else ''}}" data-column="21">preordered <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' disabled' if 'wishlist1' in  exclude_tags else ''}}" data-column="26">wishlist 1 <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' disabled' if 'wishlist2' in  exclude_tags else ''}}" data-column="27">wishlist 2 <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' disabled' if 'wishlist3' in  exclude_tags else ''}}" data-column="28">wishlist 3 <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' disabled' if 'wishlist4' in  exclude_tags else ''}}" data-column="29">wishlist 4 <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' disabled' if 'wishlist5' in  exclude_tags else ''}}" data-column="30">wishlist 5 <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' disabled' if 'fortrade' in  exclude_tags else ''}}" data-column="18">for trade <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' disabled' if 'want' in  exclude_tags else ''}}" data-column="23">want <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' disabled' if 'wanttoplay' in  exclude_tags else ''}}" data-column="25">want to play <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' disabled' if 'wanttobuy' in  exclude_tags else ''}}" data-column="24">want to buy <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' disabled' if 'notag' in  exclude_tags else ''}}" data-column="19"><em>without tag</em> <i class="fas fa-eye"></i></div>
        </div>
        <div>
            Toggle combined stats <span id="toggle_combined_slider" class="{{' disabled' if len(loading_status) <= 1 else ''}}"></span>
            <div class="toggle_tag slider_tag tag{{' disabled' if len(loading_status) <= 1 else ''}}"
                 data-column="10"
                 data-min="{{len(loading_status)}}"
                 data-max="{{len(loading_status)}}">with less then <span class="toggle_value">{{len(loading_status)}}</span> users <i class="fas fa-eye"></i></div>
            <div class="toggle_tag slider_tag tag{{' disabled' if len(loading_status)-1 == 0 else ''}}"
                 data-column="9"
                 data-min="{{len(loading_status)}}"
                 data-max="{{len(loading_status)}}">with less then <span class="toggle_value">{{len(loading_status)}}</span> ratings <i class="fas fa-eye"></i></div>
            <div class="toggle_tag slider_tag tag{{' disabled' if len(loading_status)-1 == 0 else ''}}"
                 data-column="8"
                 data-min="{{len(loading_status)}}"
                 data-max="{{len(loading_status)}}">with less then <span class="toggle_value">{{len(loading_status)}}</span> comments <i class="fas fa-eye"></i></div>
            <script>
    $(document).ready(function() {
        $("#toggle_combined_slider").slider({
            min: 1,
            max: {{len(loading_status)}},
            value: {{len(loading_status)}},
            step: 1,
            animate: true,
            slide: function (event, ui) {
                $(".toggle_value").text(ui.value);
                $(".slider_tag").data("min", ui.value);
            },
            classes: {
                "ui-slider": "",
                "ui-slider-handle": "",
                "ui-slider-range": ""
            }
        });
    });
            </script>
        </div>
        <div>
            Search by text
            <div class="filter_input"><input type="text" class="global_filter" id="global_filter" placeholder="Global"></div>
            <div class="filter_input"><input type="text" class="column_filter" id="col5_filter" data-column="5" placeholder="Boardgame title"></div>
        </div>
        <h3><i class="fas fa-sort-amount-down"></i> Sort</h3>
        <div>
            Boardgame stats
            <div class="sort tag" data-column="5">Title <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-column="2">Rating <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-column="6">Weight <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-column="7">Year <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-column="0">Number of Owners <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-column="1">Number of Ratings <i class="fas fa-sort"></i></div>
        </div>
        <div>
            <i class="fas light fa-user"></i> {{main_user['username']}}s stats
            <div class="sort tag" data-column="16">Number of Plays <i class="fas fa-sort"></i></div>
            <div class="sort tag desc" data-column="17">Rating <i class="fas fa-sort-up"></i></div>
        </div>
        <div>
            Combined stats
            <div class="sort tag" data-column="13">Number of Plays <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-column="12">Rating <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-column="11">Difference Rating <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-column="10">Number of users <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-column="9">Number of Ratings <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-column="8">Number of Comments <i class="fas fa-sort"></i></div>
        </div>
        % end
    </div>
</div>
% end
% if main_user['status'] == 1 and main_user['match_items'] > 0:
% include('game_container_table.tpl', collection=collection, main_user=main_user)
% end

% include('footer.tpl')
</body>
</html>