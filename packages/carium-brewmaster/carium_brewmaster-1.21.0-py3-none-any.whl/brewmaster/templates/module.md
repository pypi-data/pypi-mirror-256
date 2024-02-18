# brew.{{ command }}

{% for function in functions %}
## {{ function.name }}

{{ function.docs.short_description }}

{{ function.docs.long_description }}

### Args
{% for param in function.docs.params %}
 * `{{ param.arg_name }}`: <`{{ param.type_name }}`>

 {{ param.description }}
{% endfor %}

### Returns
<`{{ function.docs.returns.type_name }}`> : {{ function.docs.returns.description }}

{% endfor %}
