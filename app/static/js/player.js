/**
 * Created by Xuan on 07/11/2015.
 */
var index = 0;
var player = jwplayer("media-player");
var next_in_player = true;
var current_caption = 1;
var current_server = '';
var current_time = 0;
var server_gg_default = 9;
var movie_id = $('#media-player').attr('movie-id');
var player_token = $('#media-player').attr('player-token');
var url_playlist = base_url + "movie/loadepisoderss/" + movie_id + "/" + player_token;
var url_playlist_default = url_playlist + "/" + server_gg_default;
var url_episodes = base_url + "movie/loadepisodes/" + movie_id;
var load_count = 0;
var vast = "";
function loadEpisodes() {
    $.get(url_episodes, function (data) {
        $("#list-eps").html(data);
        loadPlaylist(url_playlist_default, false);
    });
}
function loadPlaylist(url, is_change_server) {
    $.get(url, function () {
        if (is_change_server) {
            player.load(url);
        } else {
            setupPlayer(url_playlist_default);
        }
    });
}
function setupPlayer(url) {
    player.setup({
        playlist: url,
        height: "500px",
        allowfullscreen: true,
        width: "100%",
        captions: {
            color: '#f3f378',
            fontSize: 20,
            backgroundOpacity: 0,
            fontfamily: "Helvetica",
            edgeStyle: "raised"
        },
        sharing: {
            heading: "Share movie",
            sites: ['facebook', 'twitter', 'googleplus']
        },
        skin: {
            active: "#79C143",
            inactive: "white",
            background: "black"
        },
        advertising: {
            client: 'vast',
            schedule: {
                adbreak1: {
                    offset: 5,
                    tag: vast,
                    type: 'nonlinear'
                },
                adbreak2: {
                    offset: '50%',
                    tag: vast,
                    type: 'nonlinear'
                }
            }
        }

    });
    player.on('ready', function (e) {
        setDefaultServer();
    });
    player.on('setupError', function (e) {
        loadServerEmbed();
    });
    player.on('playlistItem', function () {
        player.setCurrentCaptions(0);
        $('.btn-eps').removeClass('active');
        if (!next_in_player) {
            $('.server-active #ep-index-' + index).addClass('active');
            next_in_player = true;
        } else {
            $('.server-active #ep-index-' + player.getPlaylistIndex()).addClass('active');
        }
        console.log('Current time: ' + current_time);
        player.playlistItem(index);
        player.seek(current_time);
    });
    player.on('play', function () {
        //if (current_caption == 0) {
        //    player.setCurrentCaptions(1);
        //} else {
        player.setCurrentCaptions(current_caption);
        //}
    });

    player.on('pause', function () {
        current_caption = player.getCurrentCaptions();
        console.log('Current captions: ' + current_caption);
    });

    player.on('time', function () {
        current_time = player.getPosition();
    });

    player.on('error', function (e) {
        //console.log('Current server: ' + current_server);
        //console.log('Current episode: ' + index);
        //load_count++;
        //console.log("load " + load_count);
        //if (load_count < 5) {
        //    loadPlaylist(url_playlist + '/' + current_server, true);
        //}
    });
}
function changeServer(server, episode_index) {
    player.pause();
    current_time = 0;
    current_server = server;
    load_count = 0;
    console.log('Change Server: ' + server);
    console.log('Current server: ' + current_server);
    if (server == 12 || server == 13 || server == 14) {
        $('#media-player').hide();
        player.stop();
        $('.le-server').removeClass('server-active');
        $('#server-' + server).addClass('server-active');
        $('.btn-eps').removeClass('active');
        loadEmbed(episode_index);
    } else {
        index = episode_index;
        $('#media-player').show();
        $('#iframe-embed').attr('src', '');
        $('#content-embed').hide();
        if ($('#server-' + server).hasClass('server-active')) {
            player.playlistItem(episode_index);
        } else {
            next_in_player = false;
            loadPlaylist(url_playlist + '/' + server, true);
            $('.le-server').removeClass('server-active');
            $('#server-' + server).addClass('server-active');
        }
    }
}

function loadServerEmbed() {
    var list_sv = [14, 13, 12];
    if ($('#server-' + list_sv[0]).length > 0) {
        var episode_id = $('#server-' + list_sv[0] + ' a.first-ep').attr('episode-id');
        changeServer(list_sv[0], episode_id);
        current_server = list_sv[0];
        return true;
    } else if ($('#server-' + list_sv[1]).length > 0) {
        var episode_id = $('#server-' + list_sv[1] + ' a.first-ep').attr('episode-id');
        changeServer(list_sv[1], episode_id);
        current_server = list_sv[1];
        return true;
    } else if ($('#server-' + list_sv[2]).length > 0) {
        var episode_id = $('#server-' + list_sv[2] + ' a.first-ep').attr('episode-id');
        changeServer(list_sv[2], episode_id);
        current_server = list_sv[2];
        return true;
    } else {
        return false;
    }
}

function setDefaultServer() {
    if (current_server !== '') {
        $('#server-' + current_server).addClass('server-active');
        player.play();
    } else if ($('#server-' + server_gg_default).length > 0) {
        $('#server-' + server_gg_default).addClass('server-active');
        player.play();
    } else {
        var embed_ready = loadServerEmbed();
        if (!embed_ready) {
            for (var i = 11; i > 0; i--) {
                if ($('#server-' + i).length > 0) {
                    current_server = i;
                    $('#server-' + i).addClass('server-active');
                    player.play();
                    break;
                }
            }
        }
    }
}

function loadEmbed(episode_id) {
    $.ajax({
        url: base_url + 'movie/loadEmbed/' + episode_id,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#iframe-embed').attr('src', data.embed_url);
            $('#content-embed').show();
            $('#ep-index-' + episode_id).addClass('active');
        }
    })
}

loadEpisodes();