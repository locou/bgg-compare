<table id="collection_table" class="" style="width:100%">
    <thead>
    <tr class="hidden">
        <th data-column="0">boardgame_numowned</th>
        <th data-column="1">boardgame_numrating</th>
        <th data-column="2">boardgame_rating</th>
        <th data-column="3">boardgame_tag_bg</th>
        <th data-column="4">boardgame_tag_bgexp</th>
        <th data-column="5">boardgame_title</th>
        <th data-column="6">boardgame_weight</th>
        <th data-column="7">boardgame_year</th>
        <th data-column="8">combined_count_comments</th>
        <th data-column="9">combined_count_ratings</th>
        <th data-column="10">combined_count_users</th>
        <th data-column="11">combined_mean_diff_rating</th>
        <th data-column="12">combined_mean_rating</th>
        <th data-column="13">combined_numplays</th>
        <th data-column="14">my_has_comment</th>
        <th data-column="15">my_has_rating</th>
        <th data-column="16">my_numplays</th>
        <th data-column="17">my_rating</th>
        <th data-column="18">my_tag_fortrade</th>
        <th data-column="19">my_tag_notag</th>
        <th data-column="20">my_tag_own</th>
        <th data-column="21">my_tag_preordered</th>
        <th data-column="22">my_tag_prevowned</th>
        <th data-column="23">my_tag_want</th>
        <th data-column="24">my_tag_wanttobuy</th>
        <th data-column="25">my_tag_wanttoplay</th>
        <th data-column="26">my_tag_wishlist1</th>
        <th data-column="27">my_tag_wishlist2</th>
        <th data-column="28">my_tag_wishlist3</th>
        <th data-column="29">my_tag_wishlist4</th>
        <th data-column="30">my_tag_wishlist5</th>
        <th data-column="31">my_tags_list</th>
        <th data-column="32">boardgame_categories</th>
        <th data-column="33">boardgame_mechanics</th>
        <th data-column="34">user info</th>
    </tr>
    </thead>
    <tbody>
    % for key, item in collection.items():
    <tr>
        <td class="hidden" data-column="boardgame_numowned">
            {{item['stats']['numowned']}}
        </td>
        <td class="hidden" data-column="boardgame_numrating">
            {{item['stats']['numrating']}}
        </td>
        <td class="hidden" data-column="boardgame_rating">
            {{item['stats']['average']}}
        </td>
        <td class="hidden" data-column="boardgame_tag_bg">
            {{ 1 if item['type'] == 'boardgame' else 0}}
        </td>
        <td class="hidden" data-column="boardgame_tag_bgexp">
            {{ 1 if item['type'] == 'boardgameexpansion' else 0}}
        </td>
        <td class="hidden" data-column="boardgame_title">
            {{item['title']}}
        </td>
        <td class="hidden" data-column="boardgame_weight">
            {{item['stats']['averageweight']}}
        </td>
        <td class="hidden" data-column="boardgame_year">
            {{item['yearpublished']}}
        </td>
        <td class="hidden" data-column="combined_count_comments">
            {{item['calc']['count_comments']}}
        </td>
        <td class="hidden" data-column="combined_count_ratings">
            {{item['calc']['count_ratings']}}
        </td>
        <td class="hidden" data-column="combined_count_users">
            {{item['calc']['count_users']}}
        </td>
        <td class="hidden" data-column="combined_mean_diff_rating">
            {{item['calc']['mean_diff_rating']}}
        </td>
        <td class="hidden" data-column="combined_mean_rating">
            {{item['calc']['mean_rating']}}
        </td>
        <td class="hidden" data-column="combined_numplays">
            {{item['calc']['sum_numplays']}}
        </td>
        <td class="hidden" data-column="my_has_comment">
            {{ 1 if item['user']['comment'] else 0}}
        </td>
        <td class="hidden" data-column="my_has_rating">
            {{ 1 if item['user']['rating'] else 0}}
        </td>
        <td class="hidden" data-column="my_numplays" data-order="{{item['user']['numplays']}}">
            {{item['user']['numplays']}}
        </td>
        <td class="hidden" data-column="my_rating" data-order="{{item['user']['rating'] or ''}}">{{item['user']['rating']}}</td>
        <td class="hidden" data-column="my_tag_fortrade">
            {{1 if 'fortrade' in list(item['user']['tags'].keys()) else 0}}
        </td>
        <td class="hidden" data-column="my_tag_notag">
            {{1 if 'notag' in list(item['user']['tags'].keys()) else 0}}
        </td>
        <td class="hidden" data-column="my_tag_own">
            {{1 if 'own' in list(item['user']['tags'].keys()) else 0}}
        </td>
        <td class="hidden" data-column="my_tag_preordered">
            {{1 if 'preordered' in list(item['user']['tags'].keys()) else 0}}
        </td>
        <td class="hidden" data-column="my_tag_prevowned">
            {{1 if 'prevowned' in list(item['user']['tags'].keys()) else 0}}
        </td>
        <td class="hidden" data-column="my_tag_want">
            {{1 if 'want' in list(item['user']['tags'].keys()) else 0}}
        </td>
        <td class="hidden" data-column="my_tag_wanttobuy">
            {{1 if 'wanttobuy' in list(item['user']['tags'].keys()) else 0}}
        </td>
        <td class="hidden" data-column="my_tag_wanttoplay">
            {{1 if 'wanttoplay' in list(item['user']['tags'].keys()) else 0}}
        </td>
        <td class="hidden" data-column="my_tag_wishlist1">
            {{1 if 'wishlist1' in list(item['user']['tags'].keys()) else 0}}
        </td>
        <td class="hidden" data-column="my_tag_wishlist2">
            {{1 if 'wishlist2' in list(item['user']['tags'].keys()) else 0}}
        </td>
        <td class="hidden" data-column="my_tag_wishlist3">
            {{1 if 'wishlist3' in list(item['user']['tags'].keys()) else 0}}
        </td>
        <td class="hidden" data-column="my_tag_wishlist4">
            {{1 if 'wishlist4' in list(item['user']['tags'].keys()) else 0}}
        </td>
        <td class="hidden" data-column="my_tag_wishlist5">
            {{1 if 'wishlist5' in list(item['user']['tags'].keys()) else 0}}
        </td>
        <td class="hidden" data-column="my_tags_list">
            {{' '.join(item['user']['tags'].keys())}}
        </td>
        <td class="hidden" data-column="boardgame_categories">{{item['stats']['categories']}}</td>
        <td class="hidden" data-column="boardgame_mechanics">{{item['stats']['mechanics']}}</td>

        <td colspan="35">
            <div class="wrapper">
                <div class="bg_img">
                    <img src="{{item['thumbnail']}}">
                </div>
                <div class="bg_head wrapper_bg_head"
                     style="background: linear-gradient(110deg, #2d2944, {{item['dominant_colors'][0]}}00), linear-gradient(15deg, {{item['dominant_colors'][0]}}, {{item['dominant_colors'][1]}});">
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
                        <a class="bg_title" href="https://boardgamegeek.com/{{item['type']}}/{{key}}/"
                           id="{{ item['title']}}">{{item['title']}}</a> (<i>{{item['yearpublished']}}</i>)
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
                            <li>{{item['stats']['minplaytime']}} - {{item['stats']['maxplaytime']}} Min Playing Time
                            </li>
                            % else:
                            <li>{{item['stats']['minplaytime']}} Min Playing Time</li>
                            % end
                            % if item['stats']['averageweight']:
                            <li>
                                <span class="weight-{{'light' if item['stats']['averageweight'] <= 3 else 'heavy'}}">{{f"{item['stats']['averageweight']:.2f}"}}</span>
                                / 5 Weight
                            </li>
                            % else:
                            <li>- Weight</li>
                            % end
                        </ul>
                    </div>
                </div>
                <div class="user_calc block-primary"
                     style="background: linear-gradient(175deg, #3f3a60 10%, #3f3a6000), linear-gradient(-90deg, {{item['dominant_colors'][0]}}, {{item['dominant_colors'][1]}});">
                    <div class="wrapper_user_stats">
                        <div class="user_name tooltip"
                             data-tooltip="{{item['calc']['count_users']}} User/s | {{item['calc']['count_ratings']}} Rating/s | {{item['calc']['count_comments']}} Comment/s">
                            Combined <i class="fas fa-users"></i> {{item['calc']['count_users']}} <i
                                class="fas fa-star-half-alt"></i> {{item['calc']['count_ratings']}} <i
                                class="far fa-comment"></i> {{item['calc']['count_comments']}}
                        </div>
                        <div class="user_rating">
                            <div class="tag tooltip rating rating-{{make_int(item['calc']['mean_rating'])}}"
                                 data-tooltip="Mean rating between the users ratings">
                                {{item['calc']['mean_rating'] if item['calc']['mean_rating'] and item['calc']['mean_rating'] > 0 else '-'}}
                            </div>
                            Rating with <b class="tooltip" data-tooltip="Sum of all plays">{{item['calc']['sum_numplays']}}</b>
                            Play/s

                        </div>
                        <div class="user_diff_rating">
                            % if item['calc']['mean_diff_rating'] is not None:
                            <div class="tag tooltip rating diff-rating-{{make_int(item['calc']['mean_diff_rating'])}}"
                                 data-tooltip="Mean between the differences in rating">
                                {{item['calc']['mean_diff_rating']}}
                            </div>
                            Difference
                            % end
                        </div>
                    </div>
                </div>
                <div class="user_info">

                    % for username, stats in item['users'].items():
                    <div class="wrapper_user_stats">
                        <div class="user_name">
                            <i class="fas light fa-user"></i> <a class="tooltip"
                                                                 data-tooltip="open {{username}}s boardgamegeek profile"
                                                                 href="https://boardgamegeek.com/user/{{username}}">{{username}}</a>
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
                            <div class="tag tooltip rating diff-rating-{{make_int(stats['diff_rating'])}}"
                                 data-tooltip="Difference between {{main_user['username']}} and {{username}}s rating">
                                {{f"{stats['diff_rating']:g}"}}
                            </div>
                            Difference
                            % end
                        </div>
                        % if stats['comment']:
                        <div class="user_comment">
                            <div class="comment-arrow"></div>
                            <div class="comment">{{stats['comment']}}<span class="comment_timestamp">{{stats['lastmodified']}}</span>
                            </div>
                        </div>
                        % end
                    </div>
                    % end
                </div>
                <div class="bg_categories_mechanics">
                    % for category in item['stats']['categories']:
                    <div class="tag tag-category tooltip" data-tooltip="Category">{{category}}</div>
                    % end
                    % for mechanic in item['stats']['mechanics']:
                    <div class="tag tag-mechanic tooltip" data-tooltip="Mechanic">{{mechanic}}</div>
                    % end
                </div>
            </div>
        </td>
    </tr>
    % end
    </tbody>
</table>