<html>
% include('head.tpl', title='bgg-compare')
<body>
<div class="container">
    <div class="block block-primary">
        <h1><i class="fas fa-dice-d20"></i> Welcome to bgg-compare</h1>
        <p>
            This tool makes it possible to compare your collection with the ratings and comments of other selected
            users. Sort by number of plays, ratings and difference between your and their ratings.
        </p>
        <p>
            Start by typing your BGG Username (found in the url like <a href="https://boardgamegeek.com/">boardgamegeek.com</a>/user/USERNAME) into the
            input textfield and hit <i class="fas fa-cubes"></i> <b>Submit</b>. It takes some time for the bgg-api to
            fetch your collection, so be patient. Usually you can refresh the page after a minute to view the results.
        </p>
        <p>
            <ul>
                <li>
                    You may add any amount of additional users by clicking <i class="fas fa-user-plus"></i> <b>Add User</b>.
                </li>
                <li>
                    You may add a random set of up to 5 buddies by enabling <i class="far fa-circle"></i> <b>Include 5 random Buddies</b>.
                </li>
                <li>
                    You may add a random set of 5 random, cached users by enabling <i class="far fa-circle"></i> <b>Include 5 random, cached Users</b>.
                </li>
                <li>
                    Requested user collections are cached for {{ cache_hours }}h, so future requests are handled faster.
                    <a href="/cache"><i class="fas fa-database"></i> View cached collections</a>
                </li>
            </ul>
        </p>
    </div>

    <form id="form_build_collection" method="post" action="process" onsubmit="send_user_form()">
        <div class="is-large">
            <input id="main_user" type="text" placeholder="Username" name="main_user" required>
            <input id="include_buddies" type="checkbox" name="include_buddies" hidden>
            <label for="include_buddies" class="button checkbox">
                <i class="far fa-circle"></i> Include 5 random Buddies
            </label>
            <input id="include_random_users" type="checkbox" name="include_random_users" hidden>
            <label for="include_random_users" class="button checkbox">
                <i class="far fa-circle"></i> Include 5 random, cached Users
            </label>
            <input id="refresh_cache" type="checkbox" name="refresh_cache" hidden>
            <label for="refresh_cache" class="button checkbox">
                <i class="far fa-circle"></i> Refresh Cache
            </label>
            <p>
                <button class="button" type="submit"><i class="fas fa-cubes"></i> Submit</button>
                <button id="reset_fields" class="button reverse-color" type="reset"><i class="fas fa-redo-alt"></i> Reset</button>
                <a id="add_user_field" class="button"><i class="fas fa-user-plus"></i> Add User</a>
            </p>
        </div>
        <h3><i class="fas fa-filter"></i> Advanced Filter</h3>
        <div>
            <h4>Exclude Type</h4>
            <input id="exclude_tag_boardgame" type="checkbox" name="exclude_tag_boardgame" hidden>
            <label for="exclude_tag_boardgame" id="exclude_tag_boardgame_label" class="button checkbox">
                <i class="far fa-circle"></i> Boardgame
            </label>
            <input id="exclude_tag_boardgameexpansion" type="checkbox" name="exclude_tag_boardgameexpansion" hidden>
            <label for="exclude_tag_boardgameexpansion" id="exclude_tag_boardgameexpansion_label" class="button checkbox">
                <i class="far fa-circle"></i> Boardgame Expansion
            </label>
        </div>
        <div>
            <h4>Exclude Tags</h4>
            <input id="exclude_tag_own" type="checkbox" name="exclude_tag_own" hidden>
            <label for="exclude_tag_own" id="exclude_tag_own_label" class="button checkbox">
                <i class="far fa-circle"></i> own
            </label>
            <input id="exclude_tag_prevowned" type="checkbox" name="exclude_tag_prevowned" hidden>
            <label for="exclude_tag_prevowned" id="exclude_tag_prevowned_label" class="button checkbox">
                <i class="far fa-circle"></i> prev. owned
            </label>
            <input id="exclude_tag_preordered" type="checkbox" name="exclude_tag_preordered" hidden>
            <label for="exclude_tag_preordered" id="exclude_tag_preordered_label" class="button checkbox">
                <i class="far fa-circle"></i> preordered
            </label>
            <input id="exclude_tag_wishlist1" type="checkbox" name="exclude_tag_wishlist1" hidden>
            <label for="exclude_tag_wishlist1" id="exclude_tag_wishlist1_label" class="button checkbox">
                <i class="far fa-circle"></i> wishlist 1
            </label>
            <input id="exclude_tag_wishlist2" type="checkbox" name="exclude_tag_wishlist2" hidden>
            <label for="exclude_tag_wishlist2" id="exclude_tag_wishlist2_label" class="button checkbox">
                <i class="far fa-circle"></i> wishlist 2
            </label>
            <input id="exclude_tag_wishlist3" type="checkbox" name="exclude_tag_wishlist3" hidden>
            <label for="exclude_tag_wishlist3" id="exclude_tag_wishlist3_label" class="button checkbox">
                <i class="far fa-circle"></i> wishlist 3
            </label>
            <input id="exclude_tag_wishlist4" type="checkbox" name="exclude_tag_wishlist4" hidden>
            <label for="exclude_tag_wishlist4" id="exclude_tag_wishlist4_label" class="button checkbox">
                <i class="far fa-circle"></i> wishlist 4
            </label>
            <input id="exclude_tag_wishlist5" type="checkbox" name="exclude_tag_wishlist5" hidden>
            <label for="exclude_tag_wishlist5" id="exclude_tag_wishlist5_label" class="button checkbox">
                <i class="far fa-circle"></i> wishlist 5
            </label>
            <input id="exclude_tag_fortrade" type="checkbox" name="exclude_tag_fortrade" hidden>
            <label for="exclude_tag_fortrade" id="exclude_tag_fortrade_label" class="button checkbox">
                <i class="far fa-circle"></i> for trade
            </label>
            <input id="exclude_tag_want" type="checkbox" name="exclude_tag_want" hidden>
            <label for="exclude_tag_want" id="exclude_tag_want_label" class="button checkbox">
                <i class="far fa-circle"></i> want
            </label>
            <input id="exclude_tag_wanttoplay" type="checkbox" name="exclude_tag_wanttoplay" hidden>
            <label for="exclude_tag_wanttoplay" id="exclude_tag_wanttoplay_label" class="button checkbox">
                <i class="far fa-circle"></i> want to play
            </label>
            <input id="exclude_tag_wanttobuy" type="checkbox" name="exclude_tag_wanttobuy" hidden>
            <label for="exclude_tag_wanttobuy" id="exclude_tag_wanttobuy_label" class="button checkbox">
                <i class="far fa-circle"></i> want to buy
            </label>
            <input id="exclude_tag_notag" type="checkbox" name="exclude_tag_notag" hidden>
            <label for="exclude_tag_notag" id="exclude_tag_notag_label" class="button checkbox">
                <i class="far fa-circle"></i> <em>without tag</em>
            </label>
        </div>
        <div>
            <h4>Exclude Input</h4>
            <input id="exclude_tag_norating" type="checkbox" name="exclude_tag_norating" hidden>
            <label for="exclude_tag_norating" id="exclude_tag_norating_label" class="button checkbox">
                <i class="far fa-circle"></i> without rating
            </label>
            <input id="exclude_tag_nocomment" type="checkbox" name="exclude_tag_nocomment" hidden>
            <label for="exclude_tag_nocomment" id="exclude_tag_nocomment_label" class="button checkbox">
                <i class="far fa-circle"></i> without comment
            </label>
            <input id="exclude_tag_noplays" type="checkbox" name="exclude_tag_noplays" hidden>
            <label for="exclude_tag_noplays" id="exclude_tag_noplays_label" class="button checkbox">
                <i class="far fa-circle"></i> without plays
            </label>
        </div>
    </form>
</div>
% include('footer.tpl')
</body>
</html>