% for key, item in collection.items():
<div class="wrapper"
     data-hidden_by=""
     data-boardgame_rating="{{item['stats']['average']}}"
     data-boardgame_title="{{item['title']}}"
     data-boardgame_year="{{ item['yearpublished']}}"
     data-boardgame_numowned="{{item['stats']['numowned']}}"
     data-boardgame_numrating="{{item['stats']['numrating']}}"
     data-boardgame_weight="{{item['stats']['averageweight']}}"
     data-boardgame_tag_bg="{{ 1 if item['type'] == 'boardgame' else 0}}"
     data-boardgame_tag_bgexp="{{ 1 if item['type'] == 'boardgameexpansion' else 0}}"
     data-my_has_rating="{{ 1 if item['user']['rating'] else 0}}"
     data-my_has_comment="{{ 1 if item['user']['comment'] else 0}}"
     data-my_rating="{{item['user']['rating']}}"
     data-my_numplays="{{item['user']['numplays']}}"
     data-my_tag_own="{{1 if 'own' in list(item['user']['tags'].keys()) else 0}}"
     data-my_tag_prevowned="{{1 if 'prevowned' in list(item['user']['tags'].keys()) else 0}}"
     data-my_tag_wishlist1="{{1 if 'wishlist1' in list(item['user']['tags'].keys()) else 0}}"
     data-my_tag_wishlist2="{{1 if 'wishlist2' in list(item['user']['tags'].keys()) else 0}}"
     data-my_tag_wishlist3="{{1 if 'wishlist3' in list(item['user']['tags'].keys()) else 0}}"
     data-my_tag_wishlist4="{{1 if 'wishlist4' in list(item['user']['tags'].keys()) else 0}}"
     data-my_tag_wishlist5="{{1 if 'wishlist5' in list(item['user']['tags'].keys()) else 0}}"
     data-my_tag_wanttobuy="{{1 if 'wanttobuy' in list(item['user']['tags'].keys()) else 0}}"
     data-my_tag_preordered="{{1 if 'preordered' in list(item['user']['tags'].keys()) else 0}}"
     data-my_tag_fortrade="{{1 if 'fortrade' in list(item['user']['tags'].keys()) else 0}}"
     data-my_tag_want="{{1 if 'want' in list(item['user']['tags'].keys()) else 0}}"
     data-my_tag_wanttoplay="{{1 if 'wanttoplay' in list(item['user']['tags'].keys()) else 0}}"
     data-my_tag_notag="{{1 if 'notag' in list(item['user']['tags'].keys()) else 0}}"
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
            <div class="hexagon rating rating-{{make_int(item['stats']['average']) if item['stats']['numrating'] >= 30 else 0}}">
                % if item['stats']['average'] == 10:
                {{f"{item['stats']['average']:g}"}}
                % else:
                {{item['stats']['average'] if item['stats']['average'] > 0 else '-'}}
                % end
            </div>
        </div>
        <div class="grid_bg_title">
            <a class="bg_title" id="{{ item['title']}}" href="https://boardgamegeek.com/{{item['type']}}/{{key}}/">{{item['title']}}</a> (<i>{{item['yearpublished']}}</i>)
            % if item['type'] == 'boardgameexpansion':
            <span class="tag tag-expansion">Expansion</span>
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
                <li>
                    <span class="weight-{{'light' if item['stats']['averageweight'] <= 3 else 'heavy'}}">{{f"{item['stats']['averageweight']:.2f}"}}</span> / 5 Weight</li>
                % else:
                <li>- Weight</li>
                % end
            </ul>
        </div>
    </div>
    <div class="user_calc block-primary" style="background: linear-gradient(175deg, #3f3a60 10%, #3f3a6000), linear-gradient(-90deg, {{item['dominant_colors'][0]}}, {{item['dominant_colors'][1]}});">
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
                <i class="fas light fa-user"></i> <a class="tooltip" href="https://boardgamegeek.com/user/{{username}}" data-tooltip="open {{username}}s boardgamegeek profile">{{username}}</a>
            </div>
            <div class="user_tags">
                % for key, tag in stats['tags'].items():
                % if key != 'notag':
                % if tag[1] is None:
                <div class="tag tag-{{key}}">{{tag[0]}}</div>
                % else:
                <div class="tag tag-{{key}} tooltip" data-tooltip="{{tag[1]}}">{{tag[0]}}</div>
                % end
                % end
                % end
            </div>
            <div class="user_rating">
                <div class="tag rating rating-{{make_int(stats['rating'])}}">
                    {{f"{stats['rating']:g}" if stats['rating'] and stats['rating'] > 0 else '-'}}
                </div>
                Rating with <b>{{stats['numplays']}}</b> Play/s
            </div>
            <div class="user_diff_rating">
                % if isinstance(stats['diff_rating'], float):
                <div class="tag tooltip rating diff-rating-{{make_int(stats['diff_rating'])}}" data-tooltip="Difference between {{main_user['username']}} and {{username}}s rating">{{f"{stats['diff_rating']:g}"}}</div> Difference
                % end
            </div>
            % if stats['comment']:
            <div class="user_comment">
                <div class="comment-arrow"></div>
                <div class="comment">{{stats['comment']}}<span class="comment_timestamp">{{stats['lastmodified']}}</span></div>
            </div>
            % end
        </div>
        % end
    </div>
</div>
% end