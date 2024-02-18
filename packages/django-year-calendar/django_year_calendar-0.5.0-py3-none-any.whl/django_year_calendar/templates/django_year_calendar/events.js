
{% for evt in events %}
    {
        startDate: new Date( {{ evt.start_date | date:"Y, n - 1, j" }} ),
        endDate: new Date( {{ evt.end_date | date:"Y, n - 1, j" }} ),
    {% if evt.style and not evt.border_level %}
        border: {% if evt.style == 'border' %}1{% else %}0{% endif %},
    {% endif %}
    {% if evt.border_level and evt.border_level > 0 %}
        border: 1, border_level: {{ evt.border_level }},
    {% endif %}
    {% if evt.force_color %}
        color: "{{ evt.force_color }}",
    {% else %}
        {% if evt.color %}color: "{{ evt.color }}", {% endif %}
    {% endif %}
        id: "{{ evt.pk }}",
        ct: "{{ evt.ctype_id }}"
    },
{% endfor %}
