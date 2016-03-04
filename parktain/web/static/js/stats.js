var compute_stats = {

    class_labels: ['day-key', 'activity', 'activity-two', 'activity-three', 'activity-four'],

    get_values: function(obj){
        var keys = Object.keys(obj);
        var values = [];
        for (var i = 0; i < keys.length; i++) {
            var val = obj[keys[i]];
            values.push(val);
        }
        return values;
    },

    set_start_end: function(data) {
        var values = this.get_values(data);
        this.max = Math.max.apply(null, values);
        this.min = Math.max(1, Math.min.apply(null, values));
        this.range = (this.max - this.min)/4;
    },

    get_classname: function(count) {
        if (count == 0) {
            return this.class_labels[0];
        } else {
            var i = Math.max(1, Math.floor((count - this.min)/4)+1);
            return this.class_labels[i];
        }
    }
}


var drawing = function(data){
    /*** draw months ***/

    var month = moment();
    var outputMonth = "<ol class = 'month'>";
    for (i = 0; i <= 12; i++) {
        var durationMonth = moment.duration({'months' : 1});
        outputMonth += "<li>";
        outputMonth += moment(month).format("MMM");
        outputMonth += "</li>";
        month = moment(month).subtract(durationMonth);
    }
    outputMonth += "</ol>";

    var output = "<ol><div class = 'week'>";
    var day = moment();

    /* Calculate the offset for days of the week to line up correctly */
    var dayOfWeekOffset = 6 - (parseInt(moment().format("d"),10));
    for (i = 0; i < (dayOfWeekOffset); i++) { output += "<li class = 'offset'></li>"; }

    /*** draw calendar ***/

    compute_stats.set_start_end(data);

    for (i = 365; i >= 0; i--) {
        var datestring = moment(day).format("YYYY-MM-DD");

        var message_count = data[datestring] || 0;
        var classname = compute_stats.get_classname(message_count);
        output += '<li class="' + classname + '">';
        output += '<span class = "tooltip">' + message_count + " messages on " + datestring  +  '</span>';
        output += "</li>";

        var duration = moment.duration({'days' : 1});
        day = moment(day).subtract(duration);
    }

    output += "</div></ol>";
    document.getElementById("month").innerHTML = outputMonth;
    document.getElementById("days").innerHTML = output;
}



$(document).ready(function() {

    $.get('/stats/yearly')
        .done(function(data){
            drawing(data);
        })
        .error(function(data){console.log(data);});

});
