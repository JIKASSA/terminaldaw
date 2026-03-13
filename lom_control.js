// lom_control.js — Direct Ableton parameter control via Live Object Model
// Messages accepted:
//   list_params <track> <device>              → prints all params to Max console
//   set_param <track> <device> <param_idx> <value_0_to_1>

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
