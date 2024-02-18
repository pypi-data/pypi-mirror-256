        enableRangeSelection: true,
        style: 'custom',
        allowOverlap: true,

        customDataSourceRenderer: function (elt, currentDate, events) {
            var parent = elt.parentElement;
            var bgcolor = 'white';
            var boxShadow = '';
            var ib = 0;

            for (var i=0; i < events.length; i++) {
              var color = events[i].color;
              if (events[i].border == 1) {
                ib = events[i].border_level;
                if (ib - i > 1) boxShadow = boxShadow + `inset 0 -${4*(ib-1)}px ${bgcolor},`;
                boxShadow = boxShadow + `inset 0 -${4*ib}px ${color},`;
              } else {
                bgcolor = color;
                parent.style.backgroundColor = bgcolor;
              }
            }
            if (boxShadow != '') {
                boxShadow = boxShadow.replace(/,$/, '');
                parent.style.boxShadow = boxShadow;
            }
        },
