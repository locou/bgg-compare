<html>
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Sans:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link href="/style.css" rel="stylesheet" type="text/css">
    <link rel="icon" href="data:;base64,iVBORw0KGgo=">
    <script src="https://kit.fontawesome.com/9e34df6d41.js" crossorigin="anonymous"></script>
</head>
% from bgg_collection import make_int
<body>
<div class="container">
    <div class="wrapper_loading_status">
        % for key, user in enumerate(loading_status):
        % if user['status'] == 1:
        % if key == 0:
        <div class="grid_header block-primary">
            Displaying the collection of <a href="https://boardgamegeek.com/user/{{user['username']}}">{{user['username']}}</a>
            <div>
                <i class="fas fa-cubes"></i> {{user['total_items']}} games with <i class="far fa-comment"></i> {{user['match_items_comment']}} comments
                <p><a href="/">Back to Main Page</a></p>
            </div>
        </div>
        % else:
        <div class="grid_title">
            Added collection of <a href="https://boardgamegeek.com/user/{{user['username']}}"><i class="fas fa-user"></i> {{user['username']}}</a>
            <a class="button icon-only" href="{{user['collection_url']}}" title="switch to collection"><i class="fas fa-random"></i></a>
            <a class="button icon-only" href="{{user['remove_collection_url']}}" title="remove user"><i class="fas fa-times"></i></a>
        </div>
        <div class="grid_collection">
            matched <i class="fas fa-cubes"></i> {{user['match_items']}} of {{user['total_items']}} games providing <i class="far fa-comment"></i> {{user['match_items_comment']}} comments
        </div>
        <div class="grid_rating">
            % if user['mean_diff_rating']:
            mean difference in ratings: <div class="tag rating diff-rating-{{make_int(user['mean_diff_rating'])}}">{{user['mean_diff_rating']}}</div>
            % end
        </div>
        <div class="grid_diff_ratings">
            % for diff in user['diff_ratings']:
            <div class="tag rating diff-rating-{{diff}}"></div>
            % end
        </div>
        % end
        % elif "errors" in user:
        <div class="grid_message">Error loading "{{user['username']}}": <span>{{user['errors']}}</span></div>
        % elif "message" in user:
        <div class="grid_message">Loading <a href="https://boardgamegeek.com/user/{{user['username']}}">{{user['username']}}</a>: <span>{{user['message']}}</span></div>
        % end
        % end
    </div>
</div>
% for key, item in collection.items():
<div class="wrapper">
    <div class="bg_img">
        <img src="{{item['thumbnail']}}">
    </div>
    <div class="bg_head wrapper_bg_head">
        <div class="grid_bg_rating">
            <div class="tag rating rating-{{make_int(item['stats']['average'])}}">{{item['stats']['average'] if item['stats']['average'] > 0 else '-'}}</div>
        </div>
        <div class="grid_bg_title">
            <a class="bg_title" href="https://boardgamegeek.com/{{item['type']}}/{{key}}/">{{item['display_name']}}</a> (<i>{{item['yearpublished']}}</i>)
            <p>{{item['name']}}</p>
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
            </ul>
        </div>
    </div>
    <div class="user_calc block-primary">
        <div class="wrapper_user_stats">
            <div class="user_name">
                Combined
            </div>
            <div class="user_rating">
                <div class="tag rating rating-{{make_int(item['calc']['mean_rating'])}}">
                    {{item['calc']['mean_rating'] if item['calc']['mean_rating'] and item['calc']['mean_rating'] > 0 else '-'}}
                </div>
                Rating with <b>{{item['calc']['sum_numplays']}}</b> Play/s

            </div>
            <div class="user_diff_rating">
                % if item['calc']['mean_diff_rating']:
                <div class="tag rating diff-rating-{{item['calc']['mean_diff_rating']}}">{{item['calc']['mean_diff_rating']}}</div> Difference
                % end
            </div>
        </div>
    </div>
    <div class="user_info">

        % for username, stats in item['users'].items():
        <div class="wrapper_user_stats">
            <div class="user_name">
                <a href="https://boardgamegeek.com/user/{{username}}">{{username}}</a>
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
                <div class="tag rating diff-rating-{{stats['diff_rating']}}">{{stats['diff_rating']}}</div> Difference
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
% include('footer.tpl')
</body>
</html>