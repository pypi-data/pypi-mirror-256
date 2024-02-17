{% comment %}
/******************************************
    Allows to define the display style per day.
    The default style is 'background'; if the event instance model
    checks event_inst.style == 'border' then the day style is 'border'.
******************************************/
{% endcomment %}

    style: 'custom',
    allowOverlap: true,

    customDataSourceRenderer: function (elt, currentDate, events) {
        var parent = elt.parentElement;
        for (var i=0; i < events.length; i++) {
          if (events[i].border == 1) {
            parent.style.boxShadow = "inset 0 -4px ".concat(events[i].color);
          } else {
            parent.style.backgroundColor = events[i].color;
          }
        }
    },
