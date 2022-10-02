__all__ = ['baidu_fanyi_sign']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['baidu_sign', 'n'])
@Js
def PyJsHoisted_n_(t, e, this, arguments, var=var):
    var = Scope({'t':t, 'e':e, 'this':this, 'arguments':arguments}, var)
    var.registers(['t', 'e', 'n', 'r'])
    #for JS loop
    var.put('n', Js(0.0))
    while (var.get('n')<(var.get('e').get('length')-Js(2.0))):
        try:
            var.put('r', var.get('e').callprop('charAt', (var.get('n')+Js(2.0))))
            def PyJs_LONG_0_(var=var):
                return PyJsComma(PyJsComma(var.put('r', ((var.get('r').callprop('charCodeAt', Js(0.0))-Js(87.0)) if (Js('a')<=var.get('r')) else var.get('Number')(var.get('r')))),var.put('r', (PyJsBshift(var.get('t'),var.get('r')) if PyJsStrictEq(Js('+'),var.get('e').callprop('charAt', (var.get('n')+Js(1.0)))) else (var.get('t')<<var.get('r'))))),var.put('t', (((var.get('t')+var.get('r'))&Js(4294967295.0)) if PyJsStrictEq(Js('+'),var.get('e').callprop('charAt', var.get('n'))) else (var.get('t')^var.get('r')))))
            PyJs_LONG_0_()
        finally:
                var.put('n', Js(3.0), '+')
    return var.get('t')
PyJsHoisted_n_.func_name = 'n'
var.put('n', PyJsHoisted_n_)
@Js
def PyJsHoisted_baidu_sign_(t, this, arguments, var=var):
    var = Scope({'t':t, 'this':this, 'arguments':arguments}, var)
    var.registers(['m', 'h', 's', 'w', 'c', 't', '_', 'g', 'v', 'p', 'x', 'k', 'u', 'l', 'b', 'o', 'f', 'd', 'i', 'y', 'a'])
    var.put('window_gtk', Js('320305.131321201'))
    var.put('i', var.get('t').callprop('match', JsRegExp('/[\\uD800-\\uDBFF][\\uDC00-\\uDFFF]/g')))
    if PyJsStrictEq(var.get(u"null"),var.get('i')):
        var.put('a', var.get('t').get('length'))
        ((var.get('a')>Js(30.0)) and var.put('t', Js('').callprop('concat', var.get('t').callprop('substr', Js(0.0), Js(10.0))).callprop('concat', var.get('t').callprop('substr', (var.get('Math').callprop('floor', (var.get('a')/Js(2.0)))-Js(5.0)), Js(10.0))).callprop('concat', var.get('t').callprop('substr', (-Js(10.0)), Js(10.0)))))
    else:
        #for JS loop
        var.put('s', var.get('t').callprop('split', JsRegExp('/[\\uD800-\\uDBFF][\\uDC00-\\uDFFF]/')))
        var.put('c', Js(0.0))
        var.put('u', var.get('s').get('length'))
        var.put('l', Js([]))
        while (var.get('c')<var.get('u')):
            try:
                def PyJs_LONG_6_(var=var):
                    @Js
                    def PyJs_anonymous_1_(t, this, arguments, var=var):
                        var = Scope({'t':t, 'this':this, 'arguments':arguments}, var)
                        var.registers(['t'])
                        if var.get('Array').callprop('isArray', var.get('t')):
                            return var.get('e')(var.get('t'))
                    PyJs_anonymous_1_._set_name('anonymous')
                    @Js
                    def PyJs_anonymous_2_(t, this, arguments, var=var):
                        var = Scope({'t':t, 'this':this, 'arguments':arguments}, var)
                        var.registers(['t'])
                        if (((Js('undefined')!=var.get('Symbol',throw=False).typeof()) and (var.get(u"null")!=var.get('t').get(var.get('Symbol').get('iterator')))) or (var.get(u"null")!=var.get('t').get('@@iterator'))):
                            return var.get('Array').callprop('from', var.get('t'))
                    PyJs_anonymous_2_._set_name('anonymous')
                    @Js
                    def PyJs_anonymous_3_(t, n, this, arguments, var=var):
                        var = Scope({'t':t, 'n':n, 'this':this, 'arguments':arguments}, var)
                        var.registers(['t', 'n', 'r'])
                        if var.get('t'):
                            if (Js('string')==var.get('t',throw=False).typeof()):
                                return var.get('e')(var.get('t'), var.get('n'))
                            var.put('r', var.get('Object').get('prototype').get('toString').callprop('call', var.get('t')).callprop('slice', Js(8.0), (-Js(1.0))))
                            def PyJs_LONG_4_(var=var):
                                return PyJsComma(((PyJsStrictEq(Js('Object'),var.get('r')) and var.get('t').get('constructor')) and var.put('r', var.get('t').get('constructor').get('name'))),(var.get('Array').callprop('from', var.get('t')) if (PyJsStrictEq(Js('Map'),var.get('r')) or PyJsStrictEq(Js('Set'),var.get('r'))) else (var.get('e')(var.get('t'), var.get('n')) if (PyJsStrictEq(Js('Arguments'),var.get('r')) or JsRegExp('/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/').callprop('test', var.get('r'))) else PyJsComma(Js(0.0), Js(None)))))
                            return PyJs_LONG_4_()
                    PyJs_anonymous_3_._set_name('anonymous')
                    @Js
                    def PyJs_anonymous_5_(this, arguments, var=var):
                        var = Scope({'this':this, 'arguments':arguments}, var)
                        var.registers([])
                        PyJsTempException = JsToPyException(var.get('TypeError').create(Js('Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.')))
                        raise PyJsTempException
                    PyJs_anonymous_5_._set_name('anonymous')
                    return PyJsComma((PyJsStrictNeq(Js(''),var.get('s').get(var.get('c'))) and var.get('l').get('push').callprop('apply', var.get('l'), (((PyJs_anonymous_1_(var.put('o', var.get('s').get(var.get('c')).callprop('split', Js('')))) or PyJs_anonymous_2_(var.get('o'))) or PyJs_anonymous_3_(var.get('o'))) or PyJs_anonymous_5_()))),(PyJsStrictNeq(var.get('c'),(var.get('u')-Js(1.0))) and var.get('l').callprop('push', var.get('i').get(var.get('c')))))
                PyJs_LONG_6_()
            finally:
                    (var.put('c',Js(var.get('c').to_number())+Js(1))-Js(1))
        var.put('p', var.get('l').get('length'))
        ((var.get('p')>Js(30.0)) and var.put('t', ((var.get('l').callprop('slice', Js(0.0), Js(10.0)).callprop('join', Js(''))+var.get('l').callprop('slice', (var.get('Math').callprop('floor', (var.get('p')/Js(2.0)))-Js(5.0)), (var.get('Math').callprop('floor', (var.get('p')/Js(2.0)))+Js(5.0))).callprop('join', Js('')))+var.get('l').callprop('slice', (-Js(10.0))).callprop('join', Js('')))))
    #for JS loop
    var.put('d', Js('').callprop('concat', var.get('String').callprop('fromCharCode', Js(103.0))).callprop('concat', var.get('String').callprop('fromCharCode', Js(116.0))).callprop('concat', var.get('String').callprop('fromCharCode', Js(107.0))))
    var.put('h', var.get('window_gtk').callprop('split', Js('.')))
    var.put('f', (var.get('Number')(var.get('h').get('0')) or Js(0.0)))
    var.put('m', (var.get('Number')(var.get('h').get('1')) or Js(0.0)))
    var.put('g', Js([]))
    var.put('y', Js(0.0))
    var.put('v', Js(0.0))
    while (var.get('v')<var.get('t').get('length')):
        try:
            var.put('_', var.get('t').callprop('charCodeAt', var.get('v')))
            def PyJs_LONG_9_(var=var):
                def PyJs_LONG_8_(var=var):
                    def PyJs_LONG_7_(var=var):
                        return PyJsComma(PyJsComma(var.put('_', ((Js(65536.0)+((Js(1023.0)&var.get('_'))<<Js(10.0)))+(Js(1023.0)&var.get('t').callprop('charCodeAt', var.put('v',Js(var.get('v').to_number())+Js(1)))))),var.get('g').put((var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1)), ((var.get('_')>>Js(18.0))|Js(240.0)))),var.get('g').put((var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1)), (((var.get('_')>>Js(12.0))&Js(63.0))|Js(128.0))))
                    return PyJsComma((PyJs_LONG_7_() if (((Js(55296.0)==(Js(64512.0)&var.get('_'))) and ((var.get('v')+Js(1.0))<var.get('t').get('length'))) and (Js(56320.0)==(Js(64512.0)&var.get('t').callprop('charCodeAt', (var.get('v')+Js(1.0)))))) else var.get('g').put((var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1)), ((var.get('_')>>Js(12.0))|Js(224.0)))),var.get('g').put((var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1)), (((var.get('_')>>Js(6.0))&Js(63.0))|Js(128.0))))
                return (var.get('g').put((var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1)), var.get('_')) if (var.get('_')<Js(128.0)) else PyJsComma((var.get('g').put((var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1)), ((var.get('_')>>Js(6.0))|Js(192.0))) if (var.get('_')<Js(2048.0)) else PyJs_LONG_8_()),var.get('g').put((var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1)), ((Js(63.0)&var.get('_'))|Js(128.0)))))
            PyJs_LONG_9_()
        finally:
                (var.put('v',Js(var.get('v').to_number())+Js(1))-Js(1))
    #for JS loop
    var.put('b', var.get('f'))
    def PyJs_LONG_10_(var=var):
        return (Js('').callprop('concat', var.get('String').callprop('fromCharCode', Js(43.0))).callprop('concat', var.get('String').callprop('fromCharCode', Js(45.0))).callprop('concat', var.get('String').callprop('fromCharCode', Js(97.0)))+Js('').callprop('concat', var.get('String').callprop('fromCharCode', Js(94.0))).callprop('concat', var.get('String').callprop('fromCharCode', Js(43.0))).callprop('concat', var.get('String').callprop('fromCharCode', Js(54.0))))
    var.put('w', PyJs_LONG_10_())
    def PyJs_LONG_11_(var=var):
        return (Js('').callprop('concat', var.get('String').callprop('fromCharCode', Js(43.0))).callprop('concat', var.get('String').callprop('fromCharCode', Js(45.0))).callprop('concat', var.get('String').callprop('fromCharCode', Js(51.0)))+Js('').callprop('concat', var.get('String').callprop('fromCharCode', Js(94.0))).callprop('concat', var.get('String').callprop('fromCharCode', Js(43.0))).callprop('concat', var.get('String').callprop('fromCharCode', Js(98.0))))
    var.put('k', (PyJs_LONG_11_()+Js('').callprop('concat', var.get('String').callprop('fromCharCode', Js(43.0))).callprop('concat', var.get('String').callprop('fromCharCode', Js(45.0))).callprop('concat', var.get('String').callprop('fromCharCode', Js(102.0)))))
    var.put('x', Js(0.0))
    while (var.get('x')<var.get('g').get('length')):
        try:
            var.put('b', var.get('n')(var.put('b', var.get('g').get(var.get('x')), '+'), var.get('w')))
        finally:
                (var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1))
    return PyJsComma(PyJsComma(var.put('b', var.get('n')(var.get('b'), var.get('k'))),((var.put('b', var.get('m'), '^')<Js(0.0)) and var.put('b', (Js(2147483648.0)+(Js(2147483647.0)&var.get('b')))))),Js('').callprop('concat', var.put('b', Js(1000000.0), '%').callprop('toString'), Js('.')).callprop('concat', (var.get('b')^var.get('f'))))
PyJsHoisted_baidu_sign_.func_name = 'baidu_sign'
var.put('baidu_sign', PyJsHoisted_baidu_sign_)
pass
pass
pass
pass


# Add lib to the module scope
baidu_fanyi_sign = var.to_python()