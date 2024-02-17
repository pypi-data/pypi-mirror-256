
{% for evt in events %}
    {
    startDate: new Date( {{ evt.start_date | date:"Y, n - 1, j" }} ),
    endDate: new Date( {{ evt.end_date | date:"Y, n - 1, j" }} ),
    {% if evt.color %}color: "{{ evt.color }}", {% endif %}
    {% if evt.style %}
    style: "{{ evt.style }}",
    border: {% if evt.style == 'border' %}1{% else %}0{% endif %},
    {% endif %}
    id: "{{ evt.pk }}",
    ct: "{{ evt.ctype_id }}"
    },
{% endfor %}
