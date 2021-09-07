<html>
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Sans:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link href="/style.css" rel="stylesheet" type="text/css">
    <link rel="icon" href="data:;base64,iVBORw0KGgo=">
    <script src="https://kit.fontawesome.com/9e34df6d41.js" crossorigin="anonymous"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/smoothness/jquery-ui.css">
    <script src="/script.js"></script>
</head>
% from bgg_collection import make_int
<body>
<div class="container">
    <div class="wrapper_loading_status">
        % main_user_total_items = 0
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
                % main_user_total_items = user['total_items']
                <i class="fas fa-cubes"></i> {{user['total_items']}} games with
                <i class="fas fa-star-half-alt"></i> {{user['match_items_rating']}} ratings and
                <i class="far fa-comment"></i> {{user['match_items_comment']}} comments
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
                <input type="text" name="main_user" value="{{main_user}}" hidden>
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
                <i class="fas fa-cubes"></i>
                % if user['total_items'] > 0:
                <b>{{user['match_items']}}</b> / {{user['total_items']}}
                % else:
                0
                % end
            </span>
            <span class="tooltip" data-tooltip="providing {{user['match_items_rating']}} of {{user['total_items_rating']}} ratings">
                <i class="fas fa-star-half-alt"></i>
                % if user['total_items_rating'] > 0:
                <b>{{user['match_items_rating']}}</b> / {{user['total_items_rating']}}
                % else:
                0
                % end
            </span>
            <span class="tooltip" data-tooltip="providing {{user['match_items_comment']}} of {{user['total_items_comment']}} comments">
                <i class="far fa-comment"></i>
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
            <a href="#{{diff['title']}}"><div class="tag tooltip rating diff-rating-{{diff['diff_rating']}}" data-tooltip="{{diff['title']}}" ></div></a>
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
% if main_user_total_items:
<div id="sort_container" class="container">
    <div class="block block-primary">
        <h2><i class="fas fa-cubes"></i> Showing <span id="count_items">{{main_user_total_items}}</span> games</h2>
        <div class="clickable" id="toggle_sort_filter_block"><i class="fas fa-sort-up"></i> <span>Collapse</span><span style="display:none;">Expand</span></div>
    </div>
    <div id="sort_filter_block">
        <h3><i class="fas fa-filter"></i> Hard Filter</h3>
        <em>Will refresh the page and affect calculations (ex: mean difference)</em>
            <form id="form_hard_filter" method="post" action="/process">
                <input type="text" name="main_user" value="{{main_user}}" hidden>
                % for key, a_user in enumerate(loading_status):
                % if key != 0:
                <input type="text" class="add_user_input" name="add_user" value="{{a_user['username']}}" hidden>
                % end
                % end
                <div>
                    Exclude Type
                    <script>
    $(document).ready(function() {
        function set_checkbox(button) {
            var button_label = "#"+button+"_label";
            console.log(button_label);
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
                    Exclude Tags from <i class="fas fa-user"></i> {{main_user}}
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
                    <input id="exclude_tag_wishlist" type="checkbox" name="exclude_tag_wishlist" hidden>
                    <label for="exclude_tag_wishlist" id="exclude_tag_wishlist_label" class="button checkbox reverse-color">
                        <i class="far fa-circle"></i> wishlist
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
                        <i class="far fa-circle"></i> without tag
                    </label>
                </div>
                <div>
                    <button class="button" type="submit"><i class="fas fa-cubes"></i> Submit</button>
                    <button id="reset_fields" class="button reverse-color" type="reset"><i class="fas fa-redo-alt"></i> Reset</button>
                </div>

            </form>
        <h3><i class="fas fa-filter"></i> Soft Filter</h3>
        <div>
            Boardgame
            <div class="toggle_tag tag{{' deactivated' if 'boardgame' in exclude_tags else ''}}" data-tag="boardgame_tag_bg" data-tag_group="type">Boardgame<i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' deactivated' if 'boardgameexpansion' in exclude_tags else ''}}" data-tag="boardgame_tag_bgexp" data-tag_group="type">Boardgame Expansion<i class="fas fa-eye"></i></div>
        </div>
        <div>
            Tags from <i class="fas fa-user"></i> {{main_user}}
            <div class="toggle_tag tag{{' deactivated' if 'own' in exclude_tags else ''}}" data-tag="my_tag_own" data-tag_group="tag">own <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' deactivated' if 'prevowned' in exclude_tags else ''}}" data-tag="my_tag_prevowned" data-tag_group="tag">prev. owned <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' deactivated' if 'preordered' in exclude_tags else ''}}" data-tag="my_tag_preordered" data-tag_group="tag">preordered <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' deactivated' if 'wishlist' in exclude_tags else ''}}" data-tag="my_tag_wishlist" data-tag_group="tag">wishlist <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' deactivated' if 'fortrade' in exclude_tags else ''}}" data-tag="my_tag_fortrade" data-tag_group="tag">for trade <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' deactivated' if 'want' in exclude_tags else ''}}" data-tag="my_tag_want" data-tag_group="tag">want <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' deactivated' if 'wanttoplay' in exclude_tags else ''}}" data-tag="my_tag_wanttoplay" data-tag_group="tag">want to play <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' deactivated' if 'wanttobuy' in exclude_tags else ''}}" data-tag="my_tag_wanttobuy" data-tag_group="tag">want to buy <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' deactivated' if 'notag' in exclude_tags else ''}}" data-tag="my_tag_any" data-tag_group="tag"><em>without tag</em> <i class="fas fa-eye"></i></div>
        </div>
        <div>
            Combined <span id="toggle_combined_slider" class="{{' deactivated' if len(loading_status)-1 <= 1 else ''}}"></span>
            <div class="toggle_tag tag{{' deactivated' if len(loading_status)-1 <= 1 else ''}}" data-tag="combined_count_users" data-tag_group="combined">with less then <span class="toggle_value">{{len(loading_status)-1}}</span> users <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' deactivated' if len(loading_status)-1 == 0 else ''}}" data-tag="combined_count_ratings" data-tag_group="combined">with less then <span class="toggle_value">{{len(loading_status)-1}}</span> ratings <i class="fas fa-eye"></i></div>
            <div class="toggle_tag tag{{' deactivated' if len(loading_status)-1 == 0 else ''}}" data-tag="combined_count_comments" data-tag_group="combined">with less then <span class="toggle_value">{{len(loading_status)-1}}</span> comments <i class="fas fa-eye"></i></div>
            <script>
    $(document).ready(function() {
        $("#toggle_combined_slider").slider({
            min: 1,
            max: {{len(loading_status)-1}},
            value: {{len(loading_status)-1}},
            step: 1,
            animate: true,
            slide: function (event, ui) {
                $(".toggle_value").text(ui.value);
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
        <h3><i class="fas fa-sort-amount-down"></i> Sort</h3>
        <div>
            Boardgame stats
            <div class="sort tag" data-sort="boardgame_title">Title <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-sort="boardgame_rating">Rating <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-sort="boardgame_weight">Weight <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-sort="boardgame_year">Year <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-sort="boardgame_numowned">Number of Owners <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-sort="boardgame_numrating">Number of Ratings <i class="fas fa-sort"></i></div>
        </div>
        <div>
            <i class="fas fa-user"></i> {{main_user}}s stats
            <div class="sort tag" data-sort="my_numplays">Number of Plays <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-sort="my_rating">Rating <i class="fas fa-sort"></i></div>
        </div>
        <div>
            Combined stats
            <div class="sort tag" data-sort="combined_numplays">Number of Plays <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-sort="combined_mean_rating">Rating <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-sort="combined_mean_diff_rating">Difference Rating <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-sort="combined_count_users">Number of users <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-sort="combined_count_ratings">Number of Ratings <i class="fas fa-sort"></i></div>
            <div class="sort tag" data-sort="combined_count_comments">Number of Comments <i class="fas fa-sort"></i></div>
        </div>
    </div>
</div>
% end
<div id="game_container">
% for key, item in collection.items():
<div class="wrapper"
     data-hidden_by=""
     data-boardgame_rating="{{item['stats']['average']}}"
     data-boardgame_title="{{item['title']}}"
     data-boardgame_year="{{ item['yearpublished']}}"
     data-boardgame_numowned="{{item['stats']['numowned']}}"
     data-boardgame_numrating="{{item['stats']['numrating']}}"
     data-boardgame_weight="{{item['stats']['averageweight']}}"
     data-boardgame_tag_bg="{{ 1 if item['type'] == 'boardgame' else 0 }}"
     data-boardgame_tag_bgexp="{{ 1 if item['type'] == 'boardgameexpansion' else 0 }}"
     data-my_rating="{{item['user']['rating']}}"
     data-my_numplays="{{item['user']['numplays']}}"
     data-my_tag_own="{{item['user']['status']['own']}}"
     data-my_tag_prevowned="{{item['user']['status']['prevowned']}}"
     data-my_tag_wishlist="{{item['user']['status']['wishlist']}}"
     data-my_tag_wanttobuy="{{item['user']['status']['wanttobuy']}}"
     data-my_tag_preordered="{{item['user']['status']['preordered']}}"
     data-my_tag_fortrade="{{item['user']['status']['fortrade']}}"
     data-my_tag_want="{{item['user']['status']['want']}}"
     data-my_tag_wanttoplay="{{item['user']['status']['wanttoplay']}}"
     data-my_tag_any="{{ 0 if int(item['user']['status']['own']) + int(item['user']['status']['prevowned']) + int(item['user']['status']['wishlist']) + int(item['user']['status']['wanttobuy']) > 0 else 1}}"
     data-combined_numplays="{{item['calc']['sum_numplays']}}"
     data-combined_mean_rating="{{item['calc']['mean_rating']}}"
     data-combined_mean_diff_rating="{{item['calc']['mean_diff_rating']}}"
     data-combined_count_users="{{item['calc']['count_users']}}"
     data-combined_count_ratings="{{item['calc']['count_ratings']}}"
     data-combined_count_comments="{{item['calc']['count_comments']}}">
    <div class="bg_img">
        <img src="{{item['thumbnail']}}">
    </div>
    <div class="bg_head wrapper_bg_head" style="background: linear-gradient(110deg, #2d2944, {{item['dominant_colors'][0]}}00), linear-gradient(15deg, {{item['dominant_colors'][0]}}, {{item['dominant_colors'][1]}});">
        <div class="grid_bg_rating">
            <div class="tag rating rating-{{make_int(item['stats']['average'])}}">{{item['stats']['average'] if item['stats']['average'] > 0 else '-'}}</div>
        </div>
        <div class="grid_bg_title">
            <a class="bg_title" id="{{ item['title']}}" href="https://boardgamegeek.com/{{item['type']}}/{{key}}/">{{item['title']}}</a> (<i>{{item['yearpublished']}}</i>)
            % if item['type'] == 'boardgameexpansion':
            <span class="tag">Expansion</span>
            % end
        </div>
        <div class="grid_bg_info">
            <ul>
                <li>{{item['stats']['numowned']}} Owner | {{item['stats']['numrating']}} Ratings</li>
                % if item['stats']['minplayers'] != item['stats']['maxplayers']:
                <li>{{item['stats']['minplayers']}} - {{item['stats']['maxplayers']}} Players</li>
                % else:
                <li>{{item['stats']['minplayers']}} Players</li>
                % end
                % if item['stats']['minplaytime'] != item['stats']['maxplaytime']:
                <li>{{item['stats']['minplaytime']}} - {{item['stats']['maxplaytime']}} Min Playing Time</li>
                % else:
                <li>{{item['stats']['minplaytime']}} Min Playing Time</li>
                % end
                % if item['stats']['averageweight']:
                <li>{{item['stats']['averageweight']}} / 5 Weight</li>
                % else:
                <li>- Weight</li>
                % end
            </ul>
        </div>
    </div>
    <div class="user_calc block-primary">
        <div class="wrapper_user_stats">
            <div class="user_name tooltip" data-tooltip="{{item['calc']['count_users']}} User/s | {{item['calc']['count_ratings']}} Rating/s | {{item['calc']['count_comments']}} Comment/s">
                Combined <i class="fas fa-users"></i> {{item['calc']['count_users']}} <i class="fas fa-star-half-alt"></i> {{item['calc']['count_ratings']}} <i class="far fa-comment"></i> {{item['calc']['count_comments']}}
            </div>
            <div class="user_rating">
                <div class="tag tooltip rating rating-{{make_int(item['calc']['mean_rating'])}}" data-tooltip="Mean rating between the users ratings">
                    {{item['calc']['mean_rating'] if item['calc']['mean_rating'] and item['calc']['mean_rating'] > 0 else '-'}}
                </div>
                Rating with <b class="tooltip" data-tooltip="Sum of all plays">{{item['calc']['sum_numplays']}}</b> Play/s

            </div>
            <div class="user_diff_rating">
                % if item['calc']['mean_diff_rating'] is not None:
                <div class="tag tooltip rating diff-rating-{{make_int(item['calc']['mean_diff_rating'])}}" data-tooltip="Mean between the differences in rating">{{item['calc']['mean_diff_rating']}}</div> Difference
                % end
            </div>
        </div>
    </div>
    <div class="user_info">

        % for username, stats in item['users'].items():
        <div class="wrapper_user_stats">
            <div class="user_name">
                <a class="tooltip" href="https://boardgamegeek.com/user/{{username}}" data-tooltip="open {{username}}s boardgamegeek profile">{{username}}</a>
            </div>
            <div class="user_tags">
                % for key, stat in stats['status'].items():
                % if stat == "1":
                <div class="tag tag-{{key}}">{{key}}</div>
                % end
                % end
            </div>
            <div class="user_rating">
                <div class="tag rating rating-{{stats['rating']}}">
                    {{stats['rating'] if stats['rating'] and stats['rating'] > 0 else '-'}}
                </div>
                Rating with <b>{{stats['numplays']}}</b> Play/s
            </div>
            <div class="user_diff_rating">
                % if isinstance(stats['diff_rating'], int):
                <div class="tag tooltip rating diff-rating-{{stats['diff_rating']}}" data-tooltip="Difference between {{main_user}} and {{username}}s rating">{{stats['diff_rating']}}</div> Difference
                % end
            </div>
            % if stats['comment']:
            <div class="user_comment">
                <div class="comment-arrow"></div>
                <div class="comment">{{stats['comment']}}<span class="comment_timestamp">{{stats['status']['lastmodified']}}</span></div>
            </div>
            % end
        </div>
        % end
    </div>
</div>
% end
</div>
% include('footer.tpl')
</body>
</html>