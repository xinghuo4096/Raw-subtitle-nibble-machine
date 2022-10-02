import js2py
JS_CODE = """
function add(a,b)
{
        return a+b
}
"""

js_add=js2py.eval_js(JS_CODE)
print(js_add(1,2))

add_python=js2py.translate_js(JS_CODE)
print(add_python)

js2py.translate_file('baidu_fanyi_sign.js', 'baidu_fanyi_sign.py')
