// lom_control.js — Direct Ableton parameter control via Live Object Model
// Messages accepted:
//   list_params <track> <device>
//   set_param <track> <device> <param_idx> <value_0_to_1>
//   get_tempo
//   get_session_info

function list_params(track_idx, device_idx) {
    var device = new LiveAPI("live_set tracks " + track_idx + " devices " + device_idx);
    var params = device.get("parameters");
    post("--- Params track=" + track_idx + " device=" + device_idx + " ---\n");
    for (var i = 0; i < params.length / 2; i++) {
        var p = new LiveAPI("live_set tracks " + track_idx + " devices " + device_idx + " parameters " + i);
        post(i + ": " + p.get("name") + " = " + p.get("value") + "\n");
    }
    post("---\n");
}

function set_param(track_idx, device_idx, param_idx, value) {
    var path = "live_set tracks " + track_idx + " devices " + device_idx + " parameters " + param_idx;
    var param = new LiveAPI(path);
    if (!param || param.id == 0) {
        post("ERROR: param not found at " + path + "\n");
        return;
    }
    var min = param.get("min")[0];
    var max = param.get("max")[0];
    var scaled = min + (value * (max - min));
    param.set("value", scaled);
    post("SET: " + param.get("name") + " = " + scaled + "\n");
}

function get_tempo() {
    var live_set = new LiveAPI("live_set");
    var tempo = live_set.get("tempo")[0];
    post("TEMPO: " + tempo + "\n");
    outlet(0, "tempo", tempo);
}

function get_session_info() {
    var live_set = new LiveAPI("live_set");
    var tempo = live_set.get("tempo")[0];
    var tracks = live_set.get("tracks");
    var num_tracks = tracks.length / 2;
    post("SESSION: tempo=" + tempo + " tracks=" + num_tracks + "\n");
    outlet(0, "session_info", tempo, num_tracks);
}
