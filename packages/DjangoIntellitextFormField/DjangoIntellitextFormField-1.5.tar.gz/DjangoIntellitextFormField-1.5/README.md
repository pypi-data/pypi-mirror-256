# <center><u>DjangoIntellitextFormField</u>
 <div style="text-align: center;font-size: medium;">
    <i>Adds intellitext forms and fields to a django project</i>
</div>

### django Template:
* The class can be implemented using the following Django Template Stub:


    `{% block Intellitext %}
        {{ Field }}
        <datalist id="{{ datalist_id }}">
            {% for results in list %}
                <option value="{{ results }}">
            {% endfor %}
        </datalist>
    {% endblock %}`


* The stub can then be included using the `{% include...%}` template tag. See example below.

    
    `{% include 'BackflowPreventionValveCatalog/IntellitextStub.html' with Field=SearchOption.SerialSearch datalist_id="Seriallist" list=Serials %}`