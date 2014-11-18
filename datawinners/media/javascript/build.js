 /* underscore.min.js */
(function() {
    function V(b, n, m) {
        if (b === n) {
            return b !== 0 || 1 / b == 1 / n
        }
        if (b == null || n == null) {
            return b === n
        }
        if (b._chain) {
            b = b._wrapped
        }
        if (n._chain) {
            n = n._wrapped
        }
        if (b.isEqual && ah.isFunction(b.isEqual)) {
            return b.isEqual(n)
        }
        if (n.isEqual && ah.isFunction(n.isEqual)) {
            return n.isEqual(b)
        }
        var l = ad.call(b);
        if (l != ad.call(n)) {
            return false
        }
        switch (l) {
            case "[object String]":
                return b == String(n);
            case "[object Number]":
                return b != +b ? n != +n : b == 0 ? 1 / b == 1 / n : b == +n;
            case "[object Date]":
            case "[object Boolean]":
                return +b == +n;
            case "[object RegExp]":
                return b.source == n.source && b.global == n.global && b.multiline == n.multiline && b.ignoreCase == n.ignoreCase
        }
        if (typeof b != "object" || typeof n != "object") {
            return false
        }
        for (var k = m.length; k--; ) {
            if (m[k] == b) {
                return true
            }
        }
        m.push(b);
        var k = 0, j = true;
        if (l == "[object Array]") {
            if (k = b.length, j = k == n.length) {
                for (; k--; ) {
                    if (!(j = k in b == k in n && V(b[k], n[k], m))) {
                        break
                    }
                }
            }
        } else {
            if ("constructor" in b != "constructor" in n || b.constructor != n.constructor) {
                return false
            }
            for (var i in b) {
                if (ac.call(b, i) && (k++, !(j = ac.call(n, i) && V(b[i], n[i], m)))) {
                    break
                }
            }
            if (j) {
                for (i in n) {
                    if (ac.call(n, i) && !k--) {
                        break
                    }
                }
                j = !k
            }
        }
        m.pop();
        return j
    }
    var T = this, N = T._, aa = {}, ae = Array.prototype, Z = Object.prototype, ag = ae.slice, h = ae.unshift, ad = Z.toString, ac = Z.hasOwnProperty, L = ae.forEach, g = ae.map, e = ae.reduce, c = ae.reduceRight, Y = ae.filter, X = ae.every, U = ae.some, W = ae.indexOf, S = ae.lastIndexOf, Z = Array.isArray, f = Object.keys, R = Function.prototype.bind, ah = function(b) {
        return new ab(b)
    };
    if (typeof exports !== "undefined") {
        if (typeof module !== "undefined" && module.exports) {
            exports = module.exports = ah
        }
        exports._ = ah
    } else {
        T._ = ah
    }
    ah.VERSION = "1.3.0";
    var af = ah.each = ah.forEach = function(j, m, i) {
        if (j != null) {
            if (L && j.forEach === L) {
                j.forEach(m, i)
            } else {
                if (j.length === +j.length) {
                    for (var l = 0, k = j.length; l < k; l++) {
                        if (l in j && m.call(i, j[l], l, j) === aa) {
                            break
                        }
                    }
                } else {
                    for (l in j) {
                        if (ac.call(j, l) && m.call(i, j[l], l, j) === aa) {
                            break
                        }
                    }
                }
            }
        }
    };
    ah.map = function(j, l, i) {
        var k = [];
        if (j == null) {
            return k
        }
        if (g && j.map === g) {
            return j.map(l, i)
        }
        af(j, function(b, n, m) {
            k[k.length] = l.call(i, b, n, m)
        });
        if (j.length === +j.length) {
            k.length = j.length
        }
        return k
    };
    ah.reduce = ah.foldl = ah.inject = function(b, l, k, j) {
        var i = arguments.length > 2;
        b == null && (b = []);
        if (e && b.reduce === e) {
            return j && (l = ah.bind(l, j)), i ? b.reduce(l, k) : b.reduce(l)
        }
        af(b, function(n, m, o) {
            i ? k = l.call(j, k, n, m, o) : (k = n, i = true)
        });
        if (!i) {
            throw new TypeError("Reduce of empty array with no initial value")
        }
        return k
    };
    ah.reduceRight = ah.foldr = function(b, m, l, k) {
        var j = arguments.length > 2;
        b == null && (b = []);
        if (c && b.reduceRight === c) {
            return k && (m = ah.bind(m, k)), j ? b.reduceRight(m, l) : b.reduceRight(m)
        }
        var i = ah.toArray(b).reverse();
        k && !j && (m = ah.bind(m, k));
        return j ? ah.reduce(i, m, l, k) : ah.reduce(i, m)
    };
    ah.find = ah.detect = function(j, l, i) {
        var k;
        Q(j, function(b, n, m) {
            if (l.call(i, b, n, m)) {
                return k = b, true
            }
        });
        return k
    };
    ah.filter = ah.select = function(j, l, i) {
        var k = [];
        if (j == null) {
            return k
        }
        if (Y && j.filter === Y) {
            return j.filter(l, i)
        }
        af(j, function(b, n, m) {
            l.call(i, b, n, m) && (k[k.length] = b)
        });
        return k
    };
    ah.reject = function(j, l, i) {
        var k = [];
        if (j == null) {
            return k
        }
        af(j, function(b, n, m) {
            l.call(i, b, n, m) || (k[k.length] = b)
        });
        return k
    };
    ah.every = ah.all = function(j, l, i) {
        var k = true;
        if (j == null) {
            return k
        }
        if (X && j.every === X) {
            return j.every(l, i)
        }
        af(j, function(b, n, m) {
            if (!(k = k && l.call(i, b, n, m))) {
                return aa
            }
        });
        return k
    };
    var Q = ah.some = ah.any = function(b, k, j) {
        k || (k = ah.identity);
        var i = false;
        if (b == null) {
            return i
        }
        if (U && b.some === U) {
            return b.some(k, j)
        }
        af(b, function(m, l, n) {
            if (i || (i = k.call(j, m, l, n))) {
                return aa
            }
        });
        return !!i
    };
    ah.include = ah.contains = function(j, k) {
        var i = false;
        if (j == null) {
            return i
        }
        return W && j.indexOf === W ? j.indexOf(k) != -1 : i = Q(j, function(b) {
            return b === k
        })
    };
    ah.invoke = function(b, j) {
        var i = ag.call(arguments, 2);
        return ah.map(b, function(k) {
            return (ah.isFunction(j) ? j || k : k[j]).apply(k, i)
        })
    };
    ah.pluck = function(b, i) {
        return ah.map(b, function(j) {
            return j[i]
        })
    };
    ah.max = function(b, k, j) {
        if (!k && ah.isArray(b)) {
            return Math.max.apply(Math, b)
        }
        if (!k && ah.isEmpty(b)) {
            return -Infinity
        }
        var i = {computed: -Infinity};
        af(b, function(m, l, n) {
            l = k ? k.call(j, m, l, n) : m;
            l >= i.computed && (i = {value: m,computed: l})
        });
        return i.value
    };
    ah.min = function(b, k, j) {
        if (!k && ah.isArray(b)) {
            return Math.min.apply(Math, b)
        }
        if (!k && ah.isEmpty(b)) {
            return Infinity
        }
        var i = {computed: Infinity};
        af(b, function(m, l, n) {
            l = k ? k.call(j, m, l, n) : m;
            l < i.computed && (i = {value: m,computed: l})
        });
        return i.value
    };
    ah.shuffle = function(j) {
        var k = [], i;
        af(j, function(b, l) {
            l == 0 ? k[0] = b : (i = Math.floor(Math.random() * (l + 1)), k[l] = k[i], k[i] = b)
        });
        return k
    };
    ah.sortBy = function(b, j, i) {
        return ah.pluck(ah.map(b, function(l, k, m) {
            return {value: l,criteria: j.call(i, l, k, m)}
        }).sort(function(l, k) {
            var n = l.criteria, m = k.criteria;
            return n < m ? -1 : n > m ? 1 : 0
        }), "value")
    };
    ah.groupBy = function(b, k) {
        var j = {}, i = ah.isFunction(k) ? k : function(l) {
            return l[k]
        };
        af(b, function(m, l) {
            var n = i(m, l);
            (j[n] || (j[n] = [])).push(m)
        });
        return j
    };
    ah.sortedIndex = function(b, m, l) {
        l || (l = ah.identity);
        for (var k = 0, j = b.length; k < j; ) {
            var i = k + j >> 1;
            l(b[i]) < l(m) ? k = i + 1 : j = i
        }
        return k
    };
    ah.toArray = function(b) {
        return !b ? [] : b.toArray ? b.toArray() : ah.isArray(b) ? ag.call(b) : ah.isArguments(b) ? ag.call(b) : ah.values(b)
    };
    ah.size = function(b) {
        return ah.toArray(b).length
    };
    ah.first = ah.head = function(j, i, k) {
        return i != null && !k ? ag.call(j, 0, i) : j[0]
    };
    ah.initial = function(j, i, k) {
        return ag.call(j, 0, j.length - (i == null || k ? 1 : i))
    };
    ah.last = function(j, i, k) {
        return i != null && !k ? ag.call(j, Math.max(j.length - i, 0)) : j[j.length - 1]
    };
    ah.rest = ah.tail = function(j, i, k) {
        return ag.call(j, i == null || k ? 1 : i)
    };
    ah.compact = function(b) {
        return ah.filter(b, function(i) {
            return !!i
        })
    };
    ah.flatten = function(b, i) {
        return ah.reduce(b, function(j, k) {
            if (ah.isArray(k)) {
                return j.concat(i ? k : ah.flatten(k))
            }
            j[j.length] = k;
            return j
        }, [])
    };
    ah.without = function(b) {
        return ah.difference(b, ag.call(arguments, 1))
    };
    ah.uniq = ah.unique = function(b, k, j) {
        var j = j ? ah.map(b, j) : b, i = [];
        ah.reduce(j, function(n, m, l) {
            if (0 == l || (k === true ? ah.last(n) != m : !ah.include(n, m))) {
                n[n.length] = m, i[i.length] = b[l]
            }
            return n
        }, []);
        return i
    };
    ah.union = function() {
        return ah.uniq(ah.flatten(arguments, true))
    };
    ah.intersection = ah.intersect = function(b) {
        var i = ag.call(arguments, 1);
        return ah.filter(ah.uniq(b), function(j) {
            return ah.every(i, function(k) {
                return ah.indexOf(k, j) >= 0
            })
        })
    };
    ah.difference = function(b) {
        var i = ah.flatten(ag.call(arguments, 1));
        return ah.filter(b, function(j) {
            return !ah.include(i, j)
        })
    };
    ah.zip = function() {
        for (var b = ag.call(arguments), k = ah.max(ah.pluck(b, "length")), j = Array(k), i = 0; i < k; i++) {
            j[i] = ah.pluck(b, "" + i)
        }
        return j
    };
    ah.indexOf = function(b, k, j) {
        if (b == null) {
            return -1
        }
        var i;
        if (j) {
            return j = ah.sortedIndex(b, k), b[j] === k ? j : -1
        }
        if (W && b.indexOf === W) {
            return b.indexOf(k)
        }
        for (j = 0, i = b.length; j < i; j++) {
            if (j in b && b[j] === k) {
                return j
            }
        }
        return -1
    };
    ah.lastIndexOf = function(j, i) {
        if (j == null) {
            return -1
        }
        if (S && j.lastIndexOf === S) {
            return j.lastIndexOf(i)
        }
        for (var k = j.length; k--; ) {
            if (k in j && j[k] === i) {
                return k
            }
        }
        return -1
    };
    ah.range = function(j, i, n) {
        arguments.length <= 1 && (i = j || 0, j = 0);
        for (var n = arguments[2] || 1, m = Math.max(Math.ceil((i - j) / n), 0), l = 0, k = Array(m); l < m; ) {
            k[l++] = j, j += n
        }
        return k
    };
    var P = function() {
    };
    ah.bind = function(b, k) {
        var j, i;
        if (b.bind === R && R) {
            return R.apply(b, ag.call(arguments, 1))
        }
        if (!ah.isFunction(b)) {
            throw new TypeError
        }
        i = ag.call(arguments, 2);
        return j = function() {
            if (!(this instanceof j)) {
                return b.apply(k, i.concat(ag.call(arguments)))
            }
            P.prototype = b.prototype;
            var l = new P, m = b.apply(l, i.concat(ag.call(arguments)));
            return Object(m) === m ? m : l
        }
    };
    ah.bindAll = function(b) {
        var i = ag.call(arguments, 1);
        i.length == 0 && (i = ah.functions(b));
        af(i, function(j) {
            b[j] = ah.bind(b[j], b)
        });
        return b
    };
    ah.memoize = function(b, j) {
        var i = {};
        j || (j = ah.identity);
        return function() {
            var k = j.apply(this, arguments);
            return ac.call(i, k) ? i[k] : i[k] = b.apply(this, arguments)
        }
    };
    ah.delay = function(j, i) {
        var k = ag.call(arguments, 2);
        return setTimeout(function() {
            return j.apply(j, k)
        }, i)
    };
    ah.defer = function(b) {
        return ah.delay.apply(ah, [b, 1].concat(ag.call(arguments, 1)))
    };
    ah.throttle = function(b, p) {
        var o, n, m, l, k, j = ah.debounce(function() {
            k = l = false
        }, p);
        return function() {
            o = this;
            n = arguments;
            var i;
            m || (m = setTimeout(function() {
                m = null;
                k && b.apply(o, n);
                j()
            }, p));
            l ? k = true : b.apply(o, n);
            j();
            l = true
        }
    };
    ah.debounce = function(j, i) {
        var k;
        return function() {
            var l = this, b = arguments;
            clearTimeout(k);
            k = setTimeout(function() {
                k = null;
                j.apply(l, b)
            }, i)
        }
    };
    ah.once = function(j) {
        var i = false, k;
        return function() {
            if (i) {
                return k
            }
            i = true;
            return k = j.apply(this, arguments)
        }
    };
    ah.wrap = function(j, i) {
        return function() {
            var b = [j].concat(ag.call(arguments, 0));
            return i.apply(this, b)
        }
    };
    ah.compose = function() {
        var b = arguments;
        return function() {
            for (var i = arguments, j = b.length - 1; j >= 0; j--) {
                i = [b[j].apply(this, i)]
            }
            return i[0]
        }
    };
    ah.after = function(j, i) {
        return j <= 0 ? i() : function() {
            if (--j < 1) {
                return i.apply(this, arguments)
            }
        }
    };
    ah.keys = f || function(j) {
        if (j !== Object(j)) {
            throw new TypeError("Invalid object")
        }
        var i = [], k;
        for (k in j) {
            ac.call(j, k) && (i[i.length] = k)
        }
        return i
    };
    ah.values = function(b) {
        return ah.map(b, ah.identity)
    };
    ah.functions = ah.methods = function(b) {
        var j = [], i;
        for (i in b) {
            ah.isFunction(b[i]) && j.push(i)
        }
        return j.sort()
    };
    ah.extend = function(b) {
        af(ag.call(arguments, 1), function(i) {
            for (var j in i) {
                i[j] !== void 0 && (b[j] = i[j])
            }
        });
        return b
    };
    ah.defaults = function(b) {
        af(ag.call(arguments, 1), function(i) {
            for (var j in i) {
                b[j] == null && (b[j] = i[j])
            }
        });
        return b
    };
    ah.clone = function(b) {
        return !ah.isObject(b) ? b : ah.isArray(b) ? b.slice() : ah.extend({}, b)
    };
    ah.tap = function(j, i) {
        i(j);
        return j
    };
    ah.isEqual = function(j, i) {
        return V(j, i, [])
    };
    ah.isEmpty = function(b) {
        if (ah.isArray(b) || ah.isString(b)) {
            return b.length === 0
        }
        for (var i in b) {
            if (ac.call(b, i)) {
                return false
            }
        }
        return true
    };
    ah.isElement = function(b) {
        return !!(b && b.nodeType == 1)
    };
    ah.isArray = Z || function(b) {
        return ad.call(b) == "[object Array]"
    };
    ah.isObject = function(b) {
        return b === Object(b)
    };
    ah.isArguments = function(b) {
        return ad.call(b) == "[object Arguments]"
    };
    if (!ah.isArguments(arguments)) {
        ah.isArguments = function(b) {
            return !(!b || !ac.call(b, "callee"))
        }
    }
    ah.isFunction = function(b) {
        return ad.call(b) == "[object Function]"
    };
    ah.isString = function(b) {
        return ad.call(b) == "[object String]"
    };
    ah.isNumber = function(b) {
        return ad.call(b) == "[object Number]"
    };
    ah.isNaN = function(b) {
        return b !== b
    };
    ah.isBoolean = function(b) {
        return b === true || b === false || ad.call(b) == "[object Boolean]"
    };
    ah.isDate = function(b) {
        return ad.call(b) == "[object Date]"
    };
    ah.isRegExp = function(b) {
        return ad.call(b) == "[object RegExp]"
    };
    ah.isNull = function(b) {
        return b === null
    };
    ah.isUndefined = function(b) {
        return b === void 0
    };
    ah.noConflict = function() {
        T._ = N;
        return this
    };
    ah.identity = function(b) {
        return b
    };
    ah.times = function(j, i, l) {
        for (var k = 0; k < j; k++) {
            i.call(l, k)
        }
    };
    ah.escape = function(b) {
        return ("" + b).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#x27;").replace(/\//g, "&#x2F;")
    };
    ah.mixin = function(b) {
        af(ah.functions(b), function(i) {
            d(i, ah[i] = b[i])
        })
    };
    var a = 0;
    ah.uniqueId = function(j) {
        var i = a++;
        return j ? j + i : i
    };
    ah.templateSettings = {evaluate: /<%([\s\S]+?)%>/g,interpolate: /<%=([\s\S]+?)%>/g,escape: /<%-([\s\S]+?)%>/g};
    var O = /.^/;
    ah.template = function(b, k) {
        var j = ah.templateSettings, j = "var __p=[],print=function(){__p.push.apply(__p,arguments);};with(obj||{}){__p.push('" + b.replace(/\\/g, "\\\\").replace(/'/g, "\\'").replace(j.escape || O, function(m, l) {
            return "',_.escape(" + l.replace(/\\'/g, "'") + "),'"
        }).replace(j.interpolate || O, function(m, l) {
            return "'," + l.replace(/\\'/g, "'") + ",'"
        }).replace(j.evaluate || O, function(m, l) {
            return "');" + l.replace(/\\'/g, "'").replace(/[\r\n\t]/g, " ").replace(/\\\\/g, "\\") + ";__p.push('"
        }).replace(/\r/g, "\\r").replace(/\n/g, "\\n").replace(/\t/g, "\\t") + "');}return __p.join('');", i = new Function("obj", "_", j);
        return k ? i(k, ah) : function(l) {
            return i.call(this, l, ah)
        }
    };
    ah.chain = function(b) {
        return ah(b).chain()
    };
    var ab = function(b) {
        this._wrapped = b
    };
    ah.prototype = ab.prototype;
    var M = function(b, i) {
        return i ? ah(b).chain() : b
    }, d = function(b, i) {
        ab.prototype[b] = function() {
            var j = ag.call(arguments);
            h.call(j, this._wrapped);
            return M(i.apply(ah, j), this._chain)
        }
    };
    ah.mixin(ah);
    af("pop,push,reverse,shift,sort,splice,unshift".split(","), function(j) {
        var i = ae[j];
        ab.prototype[j] = function() {
            var k = this._wrapped;
            i.apply(k, arguments);
            var b = k.length;
            (j == "shift" || j == "splice") && b === 0 && delete k[0];
            return M(k, this._chain)
        }
    });
    af(["concat", "join", "slice"], function(j) {
        var i = ae[j];
        ab.prototype[j] = function() {
            return M(i.apply(this._wrapped, arguments), this._chain)
        }
    });
    ab.prototype.chain = function() {
        this._chain = true;
        return this
    };
    ab.prototype.value = function() {
        return this._wrapped
    }
}).call(this);
/* json2.js */
if (!this.JSON) {
    this.JSON = {}
}
(function() {
    function f(n) {
        return n < 10 ? "0" + n : n
    }
    if (typeof Date.prototype.toJSON !== "function") {
        Date.prototype.toJSON = function(key) {
            return isFinite(this.valueOf()) ? this.getUTCFullYear() + "-" + f(this.getUTCMonth() + 1) + "-" + f(this.getUTCDate()) + "T" + f(this.getUTCHours()) + ":" + f(this.getUTCMinutes()) + ":" + f(this.getUTCSeconds()) + "Z" : null
        };
        String.prototype.toJSON = Number.prototype.toJSON = Boolean.prototype.toJSON = function(key) {
            return this.valueOf()
        }
    }
    var cx = /[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g, escapable = /[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g, gap, indent, meta = {"\b": "\\b","\t": "\\t","\n": "\\n","\f": "\\f","\r": "\\r",'"': '\\"',"\\": "\\\\"}, rep;
    function quote(string) {
        escapable.lastIndex = 0;
        return escapable.test(string) ? '"' + string.replace(escapable, function(a) {
            var c = meta[a];
            return typeof c === "string" ? c : "\\u" + ("0000" + a.charCodeAt(0).toString(16)).slice(-4)
        }) + '"' : '"' + string + '"'
    }
    function str(key, holder) {
        var i, k, v, length, mind = gap, partial, value = holder[key];
        if (value && typeof value === "object" && typeof value.toJSON === "function") {
            value = value.toJSON(key)
        }
        if (typeof rep === "function") {
            value = rep.call(holder, key, value)
        }
        switch (typeof value) {
            case "string":
                return quote(value);
            case "number":
                return isFinite(value) ? String(value) : "null";
            case "boolean":
            case "null":
                return String(value);
            case "object":
                if (!value) {
                    return "null"
                }
                gap += indent;
                partial = [];
                if (Object.prototype.toString.apply(value) === "[object Array]") {
                    length = value.length;
                    for (i = 0; i < length; i += 1) {
                        partial[i] = str(i, value) || "null"
                    }
                    v = partial.length === 0 ? "[]" : gap ? "[\n" + gap + partial.join(",\n" + gap) + "\n" + mind + "]" : "[" + partial.join(",") + "]";
                    gap = mind;
                    return v
                }
                if (rep && typeof rep === "object") {
                    length = rep.length;
                    for (i = 0; i < length; i += 1) {
                        k = rep[i];
                        if (typeof k === "string") {
                            v = str(k, value);
                            if (v) {
                                partial.push(quote(k) + (gap ? ": " : ":") + v)
                            }
                        }
                    }
                } else {
                    for (k in value) {
                        if (Object.hasOwnProperty.call(value, k)) {
                            v = str(k, value);
                            if (v) {
                                partial.push(quote(k) + (gap ? ": " : ":") + v)
                            }
                        }
                    }
                }
                v = partial.length === 0 ? "{}" : gap ? "{\n" + gap + partial.join(",\n" + gap) + "\n" + mind + "}" : "{" + partial.join(",") + "}";
                gap = mind;
                return v
        }
    }
    if (typeof JSON.stringify !== "function") {
        JSON.stringify = function(value, replacer, space) {
            var i;
            gap = "";
            indent = "";
            if (typeof space === "number") {
                for (i = 0; i < space; i += 1) {
                    indent += " "
                }
            } else {
                if (typeof space === "string") {
                    indent = space
                }
            }
            rep = replacer;
            if (replacer && typeof replacer !== "function" && (typeof replacer !== "object" || typeof replacer.length !== "number")) {
                throw new Error("JSON.stringify")
            }
            return str("", {"": value})
        }
    }
    if (typeof JSON.parse !== "function") {
        JSON.parse = function(text, reviver) {
            var j;
            function walk(holder, key) {
                var k, v, value = holder[key];
                if (value && typeof value === "object") {
                    for (k in value) {
                        if (Object.hasOwnProperty.call(value, k)) {
                            v = walk(value, k);
                            if (v !== undefined) {
                                value[k] = v
                            } else {
                                delete value[k]
                            }
                        }
                    }
                }
                return reviver.call(holder, key, value)
            }
            text = String(text);
            cx.lastIndex = 0;
            if (cx.test(text)) {
                text = text.replace(cx, function(a) {
                    return "\\u" + ("0000" + a.charCodeAt(0).toString(16)).slice(-4)
                })
            }
            if (/^[\],:{}\s]*$/.test(text.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, "@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]").replace(/(?:^|:|,)(?:\s*\[)+/g, ""))) {
                j = eval("(" + text + ")");
                return typeof reviver === "function" ? walk({"": j}, "") : j
            }
            throw new SyntaxError("JSON.parse")
        }
    }
}());
/* jquery.jqmodal.min.js */
(function(d) {
    d.fn.jqm = function(f) {
        var e = {overlay: 50,overlayClass: "jqmOverlay",closeClass: "jqmClose",trigger: ".jqModal",ajax: o,ajaxText: "",target: o,modal: o,toTop: o,onShow: o,onHide: o,onLoad: o};
        return this.each(function() {
            if (this._jqm) {
                return n[this._jqm].c = d.extend({}, n[this._jqm].c, f)
            }
            p++;
            this._jqm = p;
            n[p] = {c: d.extend(e, d.jqm.params, f),a: o,w: d(this).addClass("jqmID" + p),s: p};
            if (e.trigger) {
                d(this).jqmAddTrigger(e.trigger)
            }
        })
    };
    d.fn.jqmAddClose = function(f) {
        return l(this, f, "jqmHide")
    };
    d.fn.jqmAddTrigger = function(f) {
        return l(this, f, "jqmShow")
    };
    d.fn.jqmShow = function(e) {
        return this.each(function() {
            e = e || window.event;
            d.jqm.open(this._jqm, e)
        })
    };
    d.fn.jqmHide = function(e) {
        return this.each(function() {
            e = e || window.event;
            d.jqm.close(this._jqm, e)
        })
    };
    d.jqm = {hash: {},open: function(B, A) {
            var m = n[B], q = m.c, i = "." + q.closeClass, v = (parseInt(m.w.css("z-index"))), v = (v > 0) ? v : 3000, f = d("<div></div>").css({height: "100%",width: "100%",position: "fixed",left: 0,top: 0,"z-index": v - 1,opacity: q.overlay / 100});
            if (m.a) {
                return o
            }
            m.t = A;
            m.a = true;
            m.w.css("z-index", v);
            if (q.modal) {
                if (!a[0]) {
                    k("bind")
                }
                a.push(B)
            } else {
                if (q.overlay > 0) {
                    m.w.jqmAddClose(f)
                } else {
                    f = o
                }
            }
            m.o = (f) ? f.addClass(q.overlayClass).prependTo("body") : o;
            if (c) {
                d("html,body").css({height: "100%",width: "100%"});
                if (f) {
                    f = f.css({position: "absolute"})[0];
                    for (var w in {Top: 1,Left: 1}) {
                        f.style.setExpression(w.toLowerCase(), "(_=(document.documentElement.scroll" + w + " || document.body.scroll" + w + "))+'px'")
                    }
                }
            }
            if (q.ajax) {
                var e = q.target || m.w, x = q.ajax, e = (typeof e == "string") ? d(e, m.w) : d(e), x = (x.substr(0, 1) == "@") ? d(A).attr(x.substring(1)) : x;
                e.html(q.ajaxText).load(x, function() {
                    if (q.onLoad) {
                        q.onLoad.call(this, m)
                    }
                    if (i) {
                        m.w.jqmAddClose(d(i, m.w))
                    }
                    j(m)
                })
            } else {
                if (i) {
                    m.w.jqmAddClose(d(i, m.w))
                }
            }
            if (q.toTop && m.o) {
                m.w.before('<span id="jqmP' + m.w[0]._jqm + '"></span>').insertAfter(m.o)
            }
            (q.onShow) ? q.onShow(m) : m.w.show();
            j(m);
            return o
        },close: function(f) {
            var e = n[f];
            if (!e.a) {
                return o
            }
            e.a = o;
            if (a[0]) {
                a.pop();
                if (!a[0]) {
                    k("unbind")
                }
            }
            if (e.c.toTop && e.o) {
                d("#jqmP" + e.w[0]._jqm).after(e.w).remove()
            }
            if (e.c.onHide) {
                e.c.onHide(e)
            } else {
                e.w.hide();
                if (e.o) {
                    e.o.remove()
                }
            }
            return o
        },params: {}};
    var p = 0, n = d.jqm.hash, a = [], c = d.browser.msie && (d.browser.version == "6.0"), o = false, g = d('<iframe src="javascript:false;document.write(\'\');" class="jqm"></iframe>').css({opacity: 0}), j = function(e) {
        if (c) {
            if (e.o) {
                e.o.html('<p style="width:100%;height:100%"/>').prepend(g)
            } else {
                if (!d("iframe.jqm", e.w)[0]) {
                    e.w.prepend(g)
                }
            }
        }
        h(e)
    }, h = function(f) {
        try {
            d(":input:visible", f.w)[0].focus()
        } catch (e) {
        }
    }, k = function(e) {
        d()[e]("keypress", b)[e]("keydown", b)[e]("mousedown", b)
    }, b = function(m) {
        var f = n[a[a.length - 1]], i = (!d(m.target).parents(".jqmID" + f.s)[0]);
        if (i) {
            h(f)
        }
        return !i
    }, l = function(e, f, i) {
        return e.each(function() {
            var m = this._jqm;
            d(f).each(function() {
                if (!this[i]) {
                    this[i] = [];
                    d(this).click(function() {
                        for (var q in {jqmShow: 1,jqmHide: 1}) {
                            for (var r in this[q]) {
                                if (n[this[q][r]]) {
                                    n[this[q][r]].w[q](this)
                                }
                            }
                        }
                        return o
                    })
                }
                this[i].push(m)
            })
        })
    }
})(jQuery);

/* kor.events.js */
(function() {
    var d = {}, m = {}, g = {}, a = 0;
    var c = {};
    c.listen = function(v) {
        var s = v.subject, o = v.verb, r = v.args;
        var n = a++, q = {s: s,v: o,p: v.priority,a: r,i: n,c: v.callback};
        var u;
        if (h(s)) {
            u = d
        } else {
            u = i(true, m, f(s))
        }
        var p = u[o];
        if (h(p)) {
            p = u[o] = {all: {},arg: {}}
        }
        if (!h(r)) {
            for (var t in r) {
                i(true, p, "arg", t)[n] = q
            }
        }
        p.all[n] = q;
        g[n] = q;
        return n
    };
    var e = c.fire = function(A) {
        if (h(A)) {
            throw new Error("need to provide options to fire on!")
        }
        var u = A.subject, p = A.verb, s = A.args;
        if (p == null) {
            throw new Error("need to provide a verb at minimum!")
        }
        var r = {};
        var o = i(d, p) || {all: {},arg: {}};
        var n = j(o.all);
        if (!h(u)) {
            var v = f(u);
            var x = i(m, v, p);
            if (!h(x)) {
                j(x.all, n)
            }
        }
        if (n.length === 0) {
            return true
        }
        if (!h(s)) {
            for (var z in s) {
                var t = s[z], w = j(o.arg[z]);
                if (!h(u)) {
                    j(x.arg[z], w)
                }
                for (var q = 0; q < w.length; q++) {
                    var y = w[q];
                    if (t === y.a[z]) {
                        r[y.i] = (r[y.i] || 0) + 1
                    }
                }
            }
        }
        n.sort(function(D, C) {
            var F = D.p || b(D.a), E = C.p || b(C.a);
            var B = E - F;
            if (B !== 0) {
                return B
            }
            return D.i - C.i
        });
        for (var q = 0; q < n.length; q++) {
            var y = n[q];
            if ((r[y.i] || 0) < b(y.a)) {
                continue
            }
            if (y.c(A) === false) {
                return false
            }
        }
        return true
    };
    c.derez = function(o) {
        var n = e({subject: o,verb: "derez"});
        delete m[f(o)];
        return n
    };
    c.unlisten = function(o) {
        var p = g[o];
        if (h(p)) {
            throw new Error("No event found by this id!")
        }
        var q;
        if (h(p.s)) {
            q = d[p.v]
        } else {
            q = m[f(p.s)][p.v]
        }
        delete q.all[o];
        for (var n in p.args) {
            delete q.arg[n][id]
        }
        delete g[o];
        return p
    };
    c.unlistenAll = function() {
        d = {};
        m = {};
        g = {}
    };
    var h = function(n) {
        return n === void 0
    };
    var j = function(q, o) {
        var n = o || [];
        if (q != null) {
            for (var p in q) {
                n.push(q[p])
            }
        }
        return n
    };
    var b = function(p) {
        if (p == null) {
            return 0
        }
        var n = 0;
        for (var o in p) {
            n++
        }
        return n
    };
    var i = function() {
        var n = 0;
        var p = false;
        if (arguments[0] === true) {
            n++;
            p = true
        }
        var q = arguments[n++];
        for (; n < arguments.length; n++) {
            var o = arguments[n];
            if (h(q[o])) {
                if (!p) {
                    return undefined
                } else {
                    q[o] = {}
                }
            }
            q = q[o]
        }
        return q
    };
    var f = function(o) {
        var n, p = c.key || "_kor_events_key";
        if (!h(o.jquery)) {
            if (h(n = o.data(p))) {
                o.data(p, n = a++)
            }
        } else {
            if (h(n = o[p])) {
                n = o[p] = a++
            }
        }
        return n
    };
    var l = this;
    if ((typeof module !== "undefined") && module.exports) {
        module.exports = c
    } else {
        var k = l.kor;
        if (h(k)) {
            k = l.kor = {}
        }
        k.events = c
    }
})();
/* awesomemarkup.js */
(function() {
    var j = function(n) {
        if (d(n) || (n === null)) {
            return ""
        } else {
            if (f(n)) {
                var l = [];
                for (var o = 0; o < n.length; o++) {
                    l.push(j(n[o]))
                }
                return l.join("")
            } else {
                if (a(n) || h(n)) {
                    return n.toString()
                }
            }
        }
        var p = n._, l = ["<", p];
        if (d(p)) {
            if (n.i === true) {
                return j(n.t)
            } else {
                if (n.i === false) {
                    return j(n.e)
                }
            }
            return ""
        }
        for (var k in n) {
            if ((k == "_") || (k == "contents")) {
                continue
            }
            var m = e(n[k], k);
            if (a(m) && (m !== "")) {
                l.push(" " + k + '="' + b(m) + '"')
            }
        }
        if ((p == "input") || (p == "meta") || (p == "link") || (p == "img")) {
            l.push("/>")
        } else {
            l.push(">" + j(n.contents) + "</" + p + ">")
        }
        return l.join("")
    };
    var e = function(o, l) {
        if (d(o) || (o === null)) {
            return ""
        } else {
            if (f(o)) {
                var k = [];
                for (var n = 0; n < o.length; n++) {
                    k.push(e(o[n]))
                }
                return k.join(" ")
            } else {
                if (a(o) || h(o)) {
                    return o.toString()
                }
            }
        }
        if ((o === true) && (l == "checked" || l == "selected" || l == "disabled" || l == "readonly" || l == "multiple" || l == "ismap" || l == "defer" || l == "declare" || l == "noresize" || l == "nowrap" || l == "noshade" || l == "compact")) {
            return l
        }
        if (o === false) {
            return ""
        }
        if (o.i === true) {
            return e(o.t)
        } else {
            if (o.i === false) {
                return e(o.e)
            }
        }
        if (l == "style") {
            var k = [];
            for (var m in o) {
                k.push(c(m) + ":" + e(o[m]))
            }
            return k.join(";")
        }
        if (typeof o.toString == "function") {
            return o.toString()
        }
    };
    var b = function(k) {
        return k.replace(/"/g, "&quot;").replace(/'/g, "&#39;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/&(?!(?:[a-z0-9]{1,6}|#x?[a-f0-9]{1,4});)/ig, "&amp;")
    };
    var c = function(k) {
        return k.replace(/[A-Z]/g, function(l) {
            return "-" + l.toLowerCase()
        })
    };
    var d = function(k) {
        return k === void 0
    };
    var h = function(k) {
        return !!(k === 0 || (k && k.toExponential && k.toFixed))
    };
    var a = function(k) {
        return !!(k === "" || (k && k.charCodeAt && k.substr))
    };
    var f = Array.isArray || function(k) {
        return Object.prototype.toString.call(k) === "[object Array]"
    };
    var g = this;
    if ((typeof module !== "undefined") && module.exports) {
        module.exports = {tag: j}
    } else {
        g.awesomemarkup = j
    }
    var i = g.jQuery;
    if (!d(i)) {
        i.tag = function(k, l) {
            if (l === false) {
                return j(k)
            } else {
                return i(j(k))
            }
        }
    }
})();
/* namespace.js */
if (!odkmaker) {
    var odkmaker = {}
}
if (!odkmaker.namespace) {
    odkmaker.namespace = {}
}
odkmaker.namespace.load = function(c) {
    var d = c.split(".");
    var a = window;
    for (var b = 0; b < d.length; b++) {
        var e = d[b];
        if (!a[e]) {
            a[e] = {}
        }
        a = a[e]
    }
    return a
};
/* util.js */
(function(a) {
    a.fn.spacingTop = function() {
        var b = a(this);
        return parseInt(b.css("margin-top")) + parseInt(b.css("padding-top"))
    };
    a.displayText = function(b) {
        if (b === true) {
            return "yes"
        } else {
            if (b === false) {
                return "no"
            } else {
                return b || "&nbsp;"
            }
        }
    };
    a.emptyString = function(c, b) {
        if ((c === null) || (c === undefined) || (c === "")) {
            return b
        } else {
            return c
        }
    };
    a.h = function(b) {
        if ((b === null) || (b === undefined)) {
            return ""
        } else {
            return b.replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/&/g, "&amp;")
        }
    };
    String.prototype.trim = function() {
        return this.replace(/^\s+|\s+$/g, "")
    };
    a.sanitizeString = function(b) {
        return b.replace(/([^a-z0-9]+)/ig, "-")
    };
    a.live = function(b, c, e) {
        var d = a([]);
        d.selector = b;
        d.context = document;
        if (c && e) {
            d.live(c, e)
        }
        return d
    };
    a.removeFromArray = function(b, c) {
        c.splice(a.inArray(b, c), 1)
    };
    a.toast = function(b) {
        var c = a(".toast");
        c.empty().append("<span>" + b + "</span>").animate({bottom: "-" + (c.outerHeight(true) - c.find("span").outerHeight(true) - 20) + "px"}, "slow", function() {
            setTimeout(function() {
                c.animate({bottom: "-15em"}, "slow")
            }, 3000)
        })
    };
    a.fn.debugName = function() {
        var c = a(this);
        var b = c.get(0).tagName.toLowerCase();
        if (c.attr("id") !== "") {
            b += "#" + c.attr("id")
        } else {
            if (c.attr("class") !== "") {
                b += "." + c.attr("class").split(/ +/).join(".")
            }
        }
        if (c.get(0).tagName !== "BODY") {
            b = c.parent().debugName() + " " + b
        }
        return b
    }
})(jQuery);
/* triangle.js */
(function(a) {
    a.fn.triangle = function() {
        this.each(function() {
            var d = a(this);
            var b = d.height();
            var c = d.width();
            _(b).times(function(e) {
                var f = a('<div class="slice"></div>');
                d.append(f);
                f.css({position: "absolute",top: e,left: e * 0.57735,height: 1,width: c - (e * 1.1547)})
            })
        })
    }
})(jQuery);
/* data.js */
var dataNS = odkmaker.namespace.load("odkmaker.data");
(function(g) {
    var j = function(m) {
        var n = {};
        _.each(m.data("odkControl-properties"), function(p, o) {
            n[o] = p.value
        });
        n.type = m.data("odkControl-type");
        return n
    };
    var f = function(n) {
        var m = [];
        n.children(".control").each(function() {
            var p = g(this);
            var o = j(p);
            if (o.type == "group") {
                o.children = f(p.children(".workspaceInnerWrapper").children(".workspaceInner"))
            } else {
                if (o.type == "branch") {
                    o.branches = [];
                    p.find(".workspaceInner").each(function() {
                        var q = {};
                        q.conditions = g(this).data("odkmaker-branchConditions");
                        q.children = f(g(this));
                        o.branches.push(q)
                    })
                }
            }
            m.push(o)
        });
        return m
    };
    odkmaker.data.extract = function() {
        return {title: g("h1").text(),controls: f(g(".workspace")),metadata: {activeLanguages: odkmaker.i18n.activeLanguages(),optionsPresets: odkmaker.options.presets}}
    };
    var b = function(n, m) {
        _.each(m, function(q) {
            var o = null;
            if ((q.type == "group") || (q.type == "branch") || (q.type == "metadata")) {
                o = g.extend(true, {}, g.fn.odkControl.controlProperties[q.type])
            } else {
                o = g.extend(true, g.extend(true, {}, g.fn.odkControl.defaultProperties), g.fn.odkControl.controlProperties[q.type])
            }
            _.each(o, function(s, r) {
                s.value = q[r]
            });
            var p = g("#templates .control").clone().addClass(q.type).odkControl(q.type, null, o).appendTo(n);
            if (q.type == "group") {
                b(p.find(".workspaceInner"), q.children)
            }
        })
    };
    odkmaker.data.load = function(m) {
        g("h1").text(m.title);
        g(".workspace").empty();
        odkmaker.i18n.setActiveLanguages(m.metadata.activeLanguages);
        odkmaker.options.presets = m.metadata.optionsPresets;
        b(g(".workspace"), m.controls);
        g(".workspace .control:first").trigger("odkControl-select")
    };
    var e = {inputText: "input",inputNumeric: "input",inputDate: "input",inputLocation: "input",inputMedia: "upload",inputBarcode: "input",inputSelectOne: "select1",inputSelectMany: "select"};
    var a = function(o, n, m) {
        _.each(m.children, function(s) {
            var p = [];
            var q = o[s.attrs.lang];
            if (q) {
                var r;
                while (r = q.match(/\$\{[^}]+\}/)) {
                    if (r.index > 0) {
                        p.push(q.slice(0, r.index));
                        q = q.slice(r.index)
                    }
                    p.push({name: "output",attrs: {value: q.slice(2, r[0].length - 1)}});
                    q = q.slice(r[0].length)
                }
                if (q.length > 0) {
                    p.push(q)
                }
                if (p.length === 0) {
                    p = o[s.attrs.lang]
                }
            }
            s.children.push({name: "text",attrs: {id: n},children: [{name: "value",_noWhitespace: true,children: p}]})
        })
    };
    var d = function(s, v, z, r, t, u, q) {
        if (q === undefined) {
            q = []
        }
        var n = [];
        if (s.type == "group") {
            var o = {name: s.name,attrs: {},children: []};
            z.children.push(o);
            var m = {name: "group",attrs: {},children: []};
            u.children.push(m);
            if ((s.label !== undefined) && (s.label !== "")) {
                m.children.push({name: "label",attrs: {ref: "jr:itext('" + v + s.name + ":label')"}});
                a(s.label, v + s.name + ":label", r)
            }
            if (s.loop === true) {
                o.attrs["jr:template"] = "";
                var y = {name: "repeat",attrs: {nodeset: v + s.name,},children: []};
                m.children.push(y);
                m = y
            }
            if (s.fieldList === true) {
                m.attrs.appearance = "field-list"
            }
            if ((s.relevance !== undefined) && (s.relevance !== "")) {
                q.push(s.relevance);
                var x = {name: "bind",attrs: {nodeset: s.destination || (v + s.name),relevant: "(" + q.join(") and (") + ")"}};
                t.children.push(x)
            }
            _.each(s.children, function(A) {
                d(A, v + s.name + "/", o, r, t, m, g.extend([], q))
            });
            return
        }
        if (s.type == "metadata") {
            var o = {name: s.name};
            z.children.push(o);
            var x = {name: "bind",attrs: {nodeset: s.destination || (v + s.name)}};
            var p = s.kind.toLowerCase();
            if (p == "device id") {
                x.attrs.type = "string";
                x.attrs["jr:preload"] = "property";
                x.attrs["jr:preloadParams"] = "deviceid"
            } else {
                if (p == "start time") {
                    x.attrs.type = "dateTime";
                    x.attrs["jr:preload"] = "timestamp";
                    x.attrs["jr:preloadParams"] = "start"
                } else {
                    if (p == "end time") {
                        x.attrs.type = "dateTime";
                        x.attrs["jr:preload"] = "timestamp";
                        x.attrs["jr:preloadParams"] = "end"
                    }
                }
            }
            t.children.push(x);
            return
        }
        var o = {name: s.name};
        z.children.push(o);
        var m = {name: e[s.type],attrs: {ref: s.destination || (v + s.name)},children: []};
        u.children.push(m);
        var x = {name: "bind",attrs: {nodeset: s.destination || (v + s.name)}};
        t.children.push(x);
        if (s.type == "inputText") {
            x.attrs.type = "string"
        } else {
            if (s.type == "inputNumeric") {
                if (s.kind == "Integer") {
                    x.attrs.type = "int"
                } else {
                    if (s.kind == "Decimal") {
                        x.attrs.type = "decimal"
                    }
                }
            } else {
                if (s.type == "inputDate") {
                    x.attrs.type = "date"
                } else {
                    if (s.type == "inputLocation") {
                        x.attrs.type = "geopoint"
                    } else {
                        if (s.type == "inputMedia") {
                            x.attrs.type = "binary"
                        } else {
                            if (s.type == "inputBarcode") {
                                x.attrs.type = "barcode"
                            } else {
                                if (s.type == "inputSelectOne") {
                                    x.attrs.type = "select1"
                                } else {
                                    if (s.type == "inputSelectMany") {
                                        x.attrs.type = "select"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        var w;
        if ((s.label !== undefined) && !_.isEmpty(s.label)) {
            m.children.push({name: "label", val:  s.label.eng });
            a(s.label, v + s.name + ":label", r)
        }
        if ((s.hint !== undefined) && !_.isEmpty(s.hint)) {
            m.children.push({name: "hint",attrs: {ref: "jr:itext('" + v + s.name + ":hint')"}});
            a(s.hint, v + s.name + ":hint", r)
        }
        if ((s.defaultValue !== undefined) && (s.defaultValue !== "")) {
            o.children = [s.defaultValue]
        }
        if (s.readOnly === true) {
            x.attrs.readonly = "true()"
        }
        if (s.required === true) {
            x.attrs.required = "true()"
        }
        if ((s.length !== undefined) && (s.length !== false)) {
            n.push('regex(., "^.{' + s.length.min + "," + s.length.max + '}$")');
            w = "Response length must be between " + s.length.min + " and " + s.length.max
        }
        if ((s.range !== undefined) && (s.range !== false)) {
            n.push(". " + (s.range.minInclusive ? "&gt;=" : "&gt;") + " " + c(s.range.min) + " and . " + (s.range.maxInclusive ? "&lt;=" : "&lt;") + " " + c(s.range.max));
            w = "Value must be between " + s.range.min + " and " + s.range.max
        }
        if (s.type == "inputMedia") {
            m.attrs.mediatype = s.kind.toLowerCase() + "/*"
        }
        if (s.options !== undefined) {
            _.each(s.options, function(B, A) {
                var C = v + s.name + ":option" + A;
                a(B.text, C, r);
                m.children.push({name: "item",children: [{name: "label",attrs: {ref: "jr:itext('" + C + "')"}}, {name: "value",val: B.val}]})
            })
        }
        if (s.relevance !== "") {
            q.push(s.relevance)
        }
        if (s.constraint !== "") {
            n.push(s.constraint)
        }
        if (s.calculate !== undefined && s.calculate !== "") {
            x.attrs.calculate = s.calculate
        }
        if (q.length > 0) {
            x.attrs.relevant = "(" + q.join(") and (") + ")"
        }
        if (n.length > 0) {
            x.attrs.constraint = "(" + n.join(") and (") + ")"
        }
        if ((s.invalidText !== undefined) && !_.isEmpty(s.invalidText)) {
            x.attrs["jr:constraintMsg"] = "jr:itext('" + v + s.name + ":constraintMsg')";
            a(s.label, v + s.name + ":constraintMsg", r)
        } else {
            if (w != null) {
                x.attrs["jr:constraintMsg"] = w
            }
        }
    };
    var k = function(p) {
        var r = {name: "data",attrs: {id: "build_" + g.sanitizeString(g(".header h1").text()) + "_" + Math.round((new Date()).getTime() / 1000)},children: [{name: "meta",children: [{name: "instanceID"}]}]};
        var n = {name: "instance",children: [r]};
        var q = {name: "itext",children: []};
        var s = {name: "model",children: [n, q]};
        var m = {name: "h:body",children: []};
        var o = {name: "h:html",attrs: {xmlns: "http://www.w3.org/2002/xforms","xmlns:h": "http://www.w3.org/1999/xhtml","xmlns:ev": "http://www.w3.org/2001/xml-events","xmlns:xsd": "http://www.w3.org/2001/XMLSchema","xmlns:jr": "http://openrosa.org/javarosa"},children: [{name: "h:head",children: [{name: "h:title",val: p.title}, s]}, m]};

        var t = {name: "bind",attrs: {nodeset: "/data/meta/instanceID",type: "string",readonly: "true()",calculate: "concat('uuid:', uuid())"}};
        s.children.push(t);
        _.each(p.controls, function(u) {
            d(u, "/data/", r, q, s, m)
        });
        return o
    };
    var l = function(o) {
        var m = "";
        for (var n = 0; n < o; n++) {
            m += "  "
        }
        return m
    };
    var i = function(o, n) {
        if (n === undefined) {
            n = 0
        }
        var m = l(n);
        if (_.isString(o)) {
            return h(m + o) + "\n"
        }
        m += "<" + o.name;
        if (o.attrs !== undefined) {
            _.each(o.attrs, function(q, p) {
                m += " " + p + '="' + h(q) + '"'
            })
        }
        if (o.val !== undefined) {
            m += ">" + h(o.val) + "</" + o.name + ">\n"
        } else {
            if (o.children !== undefined) {
                if (o._noWhitespace !== true) {
                    m += ">\n";
                    _.each(o.children, function(p) {
                        m += i(p, n + 1)
                    });
                    m += l(n)
                } else {
                    m += ">" + _.map(o.children, function(p) {
                        return i(p, 0).slice(0, -1)
                    }).join("")
                }
                m += "</" + o.name + ">\n"
            } else {
                m += "/>\n"
            }
        }
        return m
    };
    var h = function(m) {
        if (m == null) {
            return ""
        } else {
            return m.replace(/"/g, "&quot;").replace(/&(?!(?:[a-z0-9]{1,6}|#[a-f0-9]{4});)/ig, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
        }
    };
    var c = function(m) {
        if (m == null) {
            return "''"
        } else {
            if (_.isString(m)) {
                return "'" + m + "'"
            } else {
                return m
            }
        }
    };
    odkmaker.data.serialize = function() {
        return i(k(odkmaker.data.extract()))
    }
})(jQuery);
/* data-ui.js */
var dataNS = odkmaker.namespace.load("odkmaker.data");
(function(b) {
    dataNS.currentForm = null;
    var a = function() {
        b(".openDialog .modalLoadingOverlay").fadeIn();
        b.ajax({url: "/form/" + b(".openDialog .formList li.selected").attr("rel"),dataType: "json",type: "GET",success: function(d, c) {
                dataNS.currentForm = d;
                odkmaker.data.load(d);
                b(".openDialog").jqmHide()
            },error: function(e, c, d) {
                b(".openDialog .errorMessage").empty().append("<p>Could not open the form. Please try again in a moment.</p>").slideDown()
            }})
    };
    b(function() {
        b(".menu .newLink").click(function(f) {
            f.preventDefault();
            if (confirm("Are you sure? You will lose unsaved changes to the current form.")) {
                odkmaker.application.newForm()
            }
        });
        b(".menu .saveLink").click(function(f) {
            f.preventDefault();
            if (odkmaker.auth.currentUser === null) {
                b(".signinDialog").jqmShow();
                return
            }
            if (odkmaker.data.currentForm === null) {
                b(".saveAsDialog").jqmShow();
                return
            }
            b.ajax({url: "/form/" + odkmaker.data.currentForm.id,contentType: "application/json",dataType: "json",type: "PUT",data: JSON.stringify(odkmaker.data.extract()),success: function(h, g) {
                    dataNS.currentForm = h;
                    b.toast("Form saved!")
                },error: function(i, g, h) {
                    b.toast("Your form could not be successfully saved at this time. Please try again in a moment.")
                }})
        });
        b(".header .menu .saveLocallyLink").click(function(g) {
            g.preventDefault();
            var f = b('<form action="/binary/save" method="post" target="downloadFrame" />');
            f.append(b('<input type="hidden" name="payload"/>').val(JSON.stringify(odkmaker.data.extract()))).append(b('<input type="hidden" name="filename"/>').val(b("h1").text() + ".odkbuild"));
            f.appendTo(b("body"));
            f.submit()
        });
        var c = b(".openDialog");
        c.delegate(".formList li", "click", function(f) {
            f.preventDefault();
            var g = b(this);
            g.siblings("li").removeClass("selected");
            g.addClass("selected")
        });
        c.find(".openLink").click(function(f) {
            f.preventDefault();
            a()
        });
        c.delegate(".formList li", "dblclick", function(f) {
            f.preventDefault();
            a()
        });
        c.delegate(".formList li a.deleteFormLink", "click", function(g) {
            g.preventDefault();
            if (!confirm("Are you absolutely sure you want to delete this form? This cannot be undone.")) {
                return
            }
            c.find(".modalLoadingOverlay").fadeIn();
            var f = b(this).closest("li");
            b.ajax({url: "/form/" + f.attr("rel"),dataType: "json",type: "DELETE",success: function(i, h) {
                    c.find(".modalLoadingOverlay").stop().fadeOut();
                    odkmaker.auth.currentUser.forms = _.reject(odkmaker.auth.currentUser.forms, function(j) {
                        j.id = f.attr("rel")
                    });
                    f.remove();
                    b(".openDialog .errorMessage").empty()
                },error: function() {
                    b(".openDialog .errorMessage").empty().append("<p>Something went wrong when trying to delete that form. Please try again later.")
                }})
        });
        b(".saveAsDialog .saveAsLink").click(function(f) {
            f.preventDefault();
            var g = b(".saveAsDialog #saveAs_name").val();
            if (g === "") {
                return false
            }
            b(".saveAsDialog .errorMessage").slideUp();
            b.ajax({url: "/forms",contentType: "application/json",dataType: "json",type: "POST",data: JSON.stringify(b.extend({}, odkmaker.data.extract(), {title: g})),success: function(i, h) {
                    b.toast('Your form has been saved as "' + g + '".');
                    dataNS.currentForm = i;
                    b(".saveAsDialog").jqmHide()
                },error: function(j, h, i) {
                    b(".saveAsDialog .errorMessage").empty().append("<p>Could not save the form. Please try again in a moment.</p>").slideDown()
                }})
        });
        var d = false;
        b(".loadLocallyDialog .loadFileLink").click(function(f) {
            f.preventDefault();
            e.submit()
        });
        b(".exportDialog .downloadLink").click(function(g) {
            g.preventDefault();
        });
        b(".aggregateDialog .aggregateExportButton").click(function(g) {
            g.preventDefault();
            var f = b('<form action="/aggregate/post" method="post" target="blank" />');
            f.append(b('<input type="hidden" name="payload"/>').val(dataNS.serialize())).append(b('<input type="hidden" name="aggregate_instance_name"/>').val(b(".aggregateInstanceName").val()));
            f.appendTo(b("body"));
            f.submit()
        })
    })
})(jQuery);
/* i18n.js */
var i18nNS = odkmaker.namespace.load("odkmaker.i18n");
(function(c) {
    var g = {aar: "Afar",abk: "Abkhazian",ave: "Avestan",afr: "Afrikaans",aka: "Akan",amh: "Amharic",arg: "Aragonese",ara: "Arabic",asm: "Assamese",ava: "Avaric",aym: "Aymara",aze: "Azerbaijani",bak: "Bashkir",bel: "Belarusian",bul: "Bulgarian",bih: "Bihari",bis: "Bislama",bam: "Bambara",ben: "Bengali",bod: "Tibetan",bre: "Breton",bos: "Bosnian",cat: "Catalan, Valencian",che: "Chechen",cha: "Chamorro",cos: "Corsican",cre: "Cree",ces: "Czech",chu: "Church Slavic",chv: "Chuvash",cym: "Welsh",dan: "Danish",deu: "German",div: "Divehi",dzo: "Dzongkha",ewe: "Ewe",ell: "Modern Greek",eng: "English",epo: "Esperanto",spa: "Spanish",est: "Estonian",eus: "Basque",fas: "Persian",ful: "Fulah",fin: "Finnish",fij: "Fijian",fao: "Faroese",fra: "French",fry: "Western Frisian",gle: "Irish",gla: "Gaelic",glg: "Galician",grn: "Guaraní",guj: "Gujarati",glv: "Manx",hau: "Hausa",heb: "Modern Hebrew",hin: "Hindi",hmo: "Hiri Motu",hrv: "Croatian",hat: "Haitian",hun: "Hungarian",hye: "Armenian",her: "Herero",ina: "Interlingua",ind: "Indonesian",ile: "Interlingue",ibo: "Igbo",iii: "Sichuan Yi",ipk: "Inupiaq",ido: "Ido",isl: "Icelandic",ita: "Italian",iku: "Inuktitut",jpn: "Japanese",jav: "Javanese",kat: "Georgian",kon: "Kongo",kik: "Kikuyu",kua: "Kwanyama",kaz: "Kazakh",kal: "Kalaallisut",khm: "Central Khmer",kan: "Kannada",kor: "Korean",kau: "Kanuri",kas: "Kashmiri",kur: "Kurdish",kom: "Komi",cor: "Cornish",kir: "Kirghiz",lat: "Latin",ltz: "Luxembourgish",lug: "Ganda",lim: "Limburgish",lin: "Lingala",lao: "Lao",lit: "Lithuanian",lub: "Luba-Katanga",lav: "Latvian",mlg: "Malagasy",mah: "Marshallese",mri: "Māori",mkd: "Macedonian",mal: "Malayalam",mon: "Mongolian",mar: "Marathi",msa: "Malay",mlt: "Maltese",mya: "Burmese",nau: "Nauru",nob: "Norwegian Bokmål",nde: "North Ndebele",nep: "Nepali",ndo: "Ndonga",nld: "Dutch, Flemish",nno: "Norwegian Nynorsk",nor: "Norwegian",nbl: "South Ndebele",nav: "Navajo",nya: "Chichewa",oci: "Occitan",oji: "Ojibwa",orm: "Oromo",ori: "Oriya",oss: "Ossetian",pan: "Panjabi",pli: "Pāli",pol: "Polish",pus: "Pashto",por: "Portuguese",que: "Quechua",roh: "Romansh",run: "Rundi",ron: "Romanian, Moldavian",rus: "Russian",kin: "Kinyarwanda",san: "Sanskrit",srd: "Sardinian",snd: "Sindhi",sme: "Northern Sami",sag: "Sango",sin: "Sinhala",slk: "Slovak",slv: "Slovene",smo: "Samoan",sna: "Shona",som: "Somali",sqi: "Albanian",srp: "Serbian",ssw: "Swati",sot: "Southern Sotho",sun: "Sundanese",swe: "Swedish",swa: "Swahili",tam: "Tamil",tel: "Telugu",tgk: "Tajik",tha: "Thai",tir: "Tigrinya",tuk: "Turkmen",tgl: "Tagalog",tsn: "Tswana",ton: "Tonga",tur: "Turkish",tso: "Tsonga",tat: "Tatar",twi: "Twi",tah: "Tahitian",uig: "Uighur",ukr: "Ukrainian",urd: "Urdu",uzb: "Uzbek",ven: "Venda",vie: "Vietnamese",vol: "Volapük",wln: "Walloon",wol: "Wolof",xho: "Xhosa",yid: "Yiddish",yor: "Yoruba",zha: "Zhuang",zho: "Chinese",zul: "Zulu"};
    var f = ["eng"];
    i18nNS.activeLanguages = function() {
        return f
    };
    i18nNS.setActiveLanguages = function(h) {
        f = h || ["eng"]
    };
    var e = "eng";
    i18nNS.displayLanguage = function(h) {
        if (h !== undefined) {
            e = h
        }
        return e
    };
    i18nNS.getFriendlyName = function(h) {
        return g[h]
    };
    var b = function(i, h) {
        return c('<li class="' + i + '"><a href="#remove" class="removeTranslation">remove</a>' + h + "</li>")
    };
    var d = function() {
        var h = [];
        c(".workspace .control").each(function() {
            _.each(c(this).data("odkControl-properties"), function(i) {
                if (i.type == "uiText") {
                    h.push(i)
                }
            })
        });
        return h
    };
    var a = function() {
        var j = c(".translationsDialog");
        j.find(".translationNone").show();
        var i = j.find(".translationList").empty();
        _.each(f, function(k) {
            j.find(".translationNone").hide();
            i.append(b(k, g[k]))
        });
        var h = j.find(".translationSelect").empty();
        _.each(g, function(k, l) {
            if (c.inArray(l, f) < 0) {
                h.append('<option value="' + l + '">' + k + "</option>")
            }
        })
    };
    c(function() {
        c.live(".manageTranslations", "click", function(h) {
            h.preventDefault();
            a()
        });
        c(".translationsDialog .addTranslation").click(function(i) {
            i.preventDefault();
            var j = c(".translationSelect :selected");
            var h = j.attr("value");
            f.push(h);
            c(".translationsDialog .translationList").append(b(h, g[h]));
            j.remove();
            c(".translationsDialog .translationNone").hide();
            c(".displayLanguages").append('<li class="radio"><a href="#" rel="' + h + '"><span class="icon"></span>' + g[h] + "</a></li>");
            _.each(d(), function(k) {
                k.value[h] = ""
            });
            c(".workspace .control.selected").trigger("odkControl-reloadProperties")
        });
        c.live(".translationsDialog .removeTranslation", "click", function(i) {
            i.preventDefault();
            var j = c(this);
            var h = j.closest("li").attr("class");
            if (!confirm("Are you sure you want to delete the active language " + g[h] + "? All existing translations for this language will be lost!")) {
                return
            }
            c.removeFromArray(h, f);
            e = f[0];
            c(".translationSelect").append(c('<option value="' + h + '">' + g[h] + "</option>"));
            j.closest("li").remove();
            _.each(d(), function(k) {
                delete k.value[h]
            });
            c(".workspace .control.selected").trigger("odkControl-reloadProperties")
        })
    })
})(jQuery);
/* options-editor.js */
var optionsNS = odkmaker.namespace.load("odkmaker.options");
(function(f) {
    optionsNS.presets = [];
    optionsNS.currentProperty = null;
    optionsNS.optionsUpdated = null;
    var c = f(".optionsEditorDialog");
    var b = f(".optionsEditorDialog .optionsBody");
    var a = f(".optionsEditorDialog .optionsHeaderContainer");
    var d = f(".optionsEditorDialog .presetsSelect");
    optionsNS.modalHandler = function() {
        i();
        g(optionsNS.currentProperty)
    };
    var h = function(k) {
        var j = true;
        b.children().each(function() {
            return (j = (f(this).children(":nth-child(" + k + ")").val().trim() === ""))
        });
        return j
    };
    c.find(".optionsContainer").scroll(function() {
        a.children(":first-child").css("margin-left", -1 * f(this).scrollLeft())
    });
    b.delegate("input", "focus", function() {
        var j = f(this);
        if (j.next().length === 0) {
            b.children().each(function() {
                f(this).append('<input type="text"/>')
            })
        }
    });
    b.delegate("input", "blur", function() {
        var j = f(this);
        if (j.next().is(":last-child") && h(j.prevAll().length + 1)) {
            b.children().each(function() {
                f(this).children(":last-child").remove()
            })
        }
    });
    b.delegate("input", "keydown", function(k) {
        var m = f(this);
        if (k.which == 13) {
            if (k.shiftKey) {
                m.prev().focus()
            } else {
                m.next().focus()
            }
        } else {
            if (k.which == 9) {
                k.preventDefault();
                var l;
                var j = m.prevAll().length + 1;
                if (k.shiftKey) {
                    l = m.closest("li").prev()
                } else {
                    l = m.closest("li").next()
                }
                if (l.length === 0) {
                    if (k.shiftKey) {
                        j--;
                        l = b.children(":last-child")
                    } else {
                        j++;
                        l = b.children(":first-child")
                    }
                }
                l.children(":nth-child(" + j + ")").focus()
            }
        }
    });
    c.find(".loadPreset").click(function(j) {
        j.preventDefault();
        if (d.is(":disabled")) {
            return
        }
        g(optionsNS.presets[parseInt(d.val())].options)
    });
    c.find(".deletePreset").click(function(k) {
        k.preventDefault();
        if (d.is(":disabled")) {
            return
        }
        if (confirm("Are you sure you want to delete this preset? This cannot be undone.")) {
            var j = parseInt(d.val());
            optionsNS.presets.splice(j, 1);
            d.children(":nth-child(" + (j + 1) + ")").remove();
            i()
        }
    });
    c.find(".savePreset").click(function(k) {
        k.preventDefault();
        var j = prompt("Please name this options preset.").trim();
        if (j === "") {
            return
        }
        optionsNS.presets.push({name: j,options: e()});
        i()
    });
    c.find(".applyOptions").click(function(j) {
        j.preventDefault();
        if (_.isFunction(optionsNS.optionsUpdated)) {
            optionsNS.optionsUpdated(e())
        }
        c.jqmHide()
    });
    var i = function() {
        d.empty();
        _.each(optionsNS.presets, function(j, k) {
            d.append('<option value="' + k + '">' + f.h(j.name) + "</option>")
        });
        if (_.isEmpty(optionsNS.presets)) {
            d.append('<option value="">(none created yet)</option>')
        }
        d.attr("disabled", _.isEmpty(optionsNS.presets))
    };
    var g = function(k) {
        var l = [{id: "value",name: "Underlying Value"}].concat(_.map(odkmaker.i18n.activeLanguages(), function(m) {
            return {id: m,name: odkmaker.i18n.getFriendlyName(m)}
        }));
        var j = l.length * 150;
        c.find(".optionsHeader, .optionsBody").empty();
        _.each(l, function(o) {
            c.find(".optionsHeader").width(j).append("<li>" + o.name + "</li>");
            var n;
            if (o.id == "value") {
                n = _.pluck(k, "val")
            } else {
                n = _.map(k, function(p) {
                    return p.text[o.id] || ""
                })
            }
            n.push("");
            var m = f('<li data-lang="' + o.id + '"/>');
            _.each(n, function(p) {
                m.append('<input type="text" value="' + f.h(p) + '"/>')
            });
            c.find(".optionsBody").width(j).append(m)
        })
    };
    var e = function() {
        var j = [];
        _(b.children(":first-child").children().length).times(function() {
            j.push({text: {}})
        });
        b.children().each(function() {
            var k = f(this);
            var l = k.attr("data-lang");
            k.children().each(function(m) {
                if (l == "value") {
                    j[m].val = f(this).val().trim()
                } else {
                    j[m].text[l] = f(this).val().trim()
                }
            })
        });
        return _.reject(j, function(k) {
            return (k.val === "") && _.all(k.text, function(l) {
                return l === ""
            })
        })
    }
})(jQuery);
/* modals.js */
var modalsNS = odkmaker.namespace.load("odkmaker.modals");
(function(b) {
    var a = {signinDialog: function(c) {
            c.find(":input").val("").end().find("h3").text("Sign in").end().find(".signinLink").removeClass("hide").end().find(".signupLink").addClass("hide").end().find(".toggleSignupLink").text("Don't yet have an account?").closest("p").show().end().end().find(".passwordLink").addClass("hide").end().find(".togglePasswordLink").text("Forgot your password?").closest("p").show().end().end().find(".signin_section").show().end().find(".signup_section").hide()
        },accountDialog: function(c) {
            c.find("#account_email").val(odkmaker.auth.currentUser.email)
        },openDialog: function(d) {
            var c = d.find(".formList");
            c.empty();
            d.find(".errorMessage").empty();
            d.find(".modalLoadingOverlay").fadeIn();
            odkmaker.auth.verify(function() {
                d.find(".modalLoadingOverlay").stop().fadeOut();
                _.each(odkmaker.auth.currentUser.forms, function(e) {
                    c.append('<li rel="' + e.id + '">' + b.h(e.title) + '<a href="#delete" class="deleteFormLink">delete</a></li>')
                });
                if (odkmaker.auth.currentUser.forms.length === 0) {
                    c.append('<li class="noData">You do not appear to have saved any forms just yet.</li>')
                }
            })
        },saveAsDialog: function(c) {
            c.find("#saveAs_name").val(b("h1").text())
        },loadLocallyDialog: function(c) {
            c.find(".errorMessage").hide();
            c.find("#loadFile_name").val("")
        },exportDialog: function(c) {
               var post_data = {
                   'xform': odkmaker.data.serialize(),
                   'file' : JSON.stringify(odkmaker.data.extract())
               };
        var callback = function (response) {
            var redirect_url = '/project/overview/' + response.project_id;
            DW.trackEvent('questionnaire-creation-method', 'simple-qns-success');
            window.location.replace(redirect_url);
            return true;
        };

        $.post('/xform_designer/create/', post_data).done(function(response) {
           var responseJson = response;
           if (responseJson.success) {
               return callback(responseJson);
            }
            else {
                $.unblockUI();
                if(!(responseJson.code_has_errors || responseJson.name_has_errors)) {
                    questionnaireViewModel.errorInResponse(true);
                }
                if(responseJson.code_has_errors) {
                    questionnaireViewModel.questionnaireCode.setError(responseJson.error_message['code']);
                }
                if(responseJson.name_has_errors) {
                    questionnaireViewModel.projectName.setError(responseJson.error_message['name']);
                }
            }
        });
//            if (b(".workspace .control.error:first").length > 0) {
//                c.find(".validationWarningMessage").show()
//            } else {
//                c.find(".validationWarningMessage").hide()
//            }
//            c.find(".exportCodeContainer pre").text(odkmaker.data.serialize())
        },aggregateDialog: function(c) {
            c.removeClass("exporting")
        },optionsEditorDialog: odkmaker.options.modalHandler};
    b(function() {
        b(".modal").jqm({modal: true,onShow: function(c) {
                _.each(a, function(e, d) {
                    if (c.w.hasClass(d)) {
                        e(c.w, c.t)
                    }
                });
                c.w.fadeIn("slow");
                c.o.fadeIn("slow")
            },onHide: function(c) {
                c.w.fadeOut("slow");
                c.o.fadeOut("slow")
            }}).append('<div class="modalLoadingOverlay"><div class="loadingSpinner"></div></div>');
        b.live("a[rel=modal]", "click", function(c) {
            c.preventDefault();
            var d = b(this);
            if (d.hasClass("authRequired") && (odkmaker.auth.currentUser === null)) {
                b(".signinDialog").jqmShow();
                return
            } else {
                if (d.hasClass("destructive")) {
                    if (!confirm("Are you sure? You will lose unsaved changes to the current form.")) {
                        return
                    }
                }
            }
            b(".modal." + d.attr("href").replace(/#/, "")).jqmShow()
        });
        b(".modal form").submit(function(c) {
            c.preventDefault();
            b(this).closest(".modal").find(".acceptLink").click()
        })
    })
})(jQuery);
/* property-editor.js */
(function(d) {
    var c = {required: "This property is required.",alphanumeric: "Only letters and numbers are allowed.",unique: "This property must be unique; there is another control that conflicts with it."};
    var a = function(i, g, f, h) {
        if (_.isUndefined(g.limit)) {
            return
        }
        var e = [];
        _.each(g.limit, function(j) {
            switch (j) {
                case "required":
                    if ((g.value == null) || (g.value === "")) {
                        e.push(j)
                    }
                    break;
                case "alphanumeric":
                    if (!_.isString(g.value) || g.value.match(/[^0-9a-z_]/i)) {
                        e.push(j)
                    }
                    break;
                case "unique":
                    if (h.parent().length === 0) {
                        break
                    }
                    var k = true;
                    h.siblings().each(function() {
                        k = k && (d(this).data("odkControl-properties")[f].value != g.value)
                    });
                    if (!k) {
                        e.push(j)
                    }
                    break
            }
        });
        i.children(".errorList").remove();
        if (e.length > 0) {
            g.validationErrors = e;
            i.addClass("error");
            d("<ul/>").addClass("errorList").append(_.map(e, function(j) {
                return "<li>" + c[j] + "</li>"
            }).join("")).appendTo(i)
        } else {
            delete g.validationErrors;
            i.removeClass("error")
        }
    };
    d.fn.propertyEditor = function(f, e, g) {
        return this.each(function() {
            var i = d(this);
            var h = d("#templates .editors ." + f.type).clone();
            h.attr("data-name", e);
            i.empty().append(h);
            d.fn.propertyEditor.editors[f.type](f, h, g, e);
            i.bind("odkProperty-validate", function() {
                a(i, f, e, g)
            });
            a(i, f, e, g)
        })
    };
    d.fn.propertyEditor.defaults = {};
    d.fn.propertyEditor.editors = {text: function(e, g, f) {
            g.find("h4").text(e.name);
            g.find("p").text(e.description);
            g.find(".editorTextfield").attr("id", "property_" + e.name).val(e.value || "").bind("keyup input", function(h) {
                e.value = d(this).val();
                f.trigger("odkControl-propertiesUpdated")
            })
        },uiText: function(f, h, g) {
            h.find("h4").text(f.name);
            h.find("p").text(f.description);
            var e = h.find(".translations");
            _.each(odkmaker.i18n.activeLanguages(), function(k) {
                var j = k;
                var i = d("#templates .editors .uiText-translation").clone();
                i.find("h5").text(odkmaker.i18n.getFriendlyName(j));
                i.find(".editorTextfield").val((f.value == null) ? "" : (f.value[j] || "")).bind("keyup input", function(l) {
                    f.value[j] = d(this).val();
                    g.trigger("odkControl-propertiesUpdated")
                });
                e.append(i)
            })
        },bool: function(e, g, f) {
            g.find(".editorCheckbox").attr("id", "property_" + e.name).attr("checked", e.value === true).click(function(h) {
                e.value = d(this).is(":checked");
                f.trigger("odkControl-propertiesUpdated")
            });
            g.find("label").attr("for", "property_" + e.name).text(e.name);
            g.find("p").text(e.description)
        },numericRange: function(f, h, g) {
            h.find("h4").text(f.name);
            h.find("p").text(f.description);
            var e = h.find(".editorTextfield, .inclusive");
            var i = function() {
                return {min: e.filter(".min").val(),max: e.filter(".max").val(),minInclusive: e.filter(".minInclusive").is(":checked"),maxInclusive: e.filter(".maxInclusive").is(":checked")}
            };
            if (f.value === false) {
                e.attr("disabled", true)
            } else {
                e.filter(".min").val(f.value.min).end().filter(".max").val(f.value.max).end().filter(".minInclusive").attr("checked", f.value.minInclusive).end().filter(".maxInclusive").attr("checked", f.value.maxInclusive).end()
            }
            e.bind("input change keyup", function(j) {
                f.value = i();
                g.trigger("odkControl-propertiesUpdated")
            });
            h.find(".editorEnabled").attr("checked", f.value !== false).click(function(j) {
                if (d(this).is(":checked")) {
                    e.attr("disabled", false);
                    f.value = i();
                    g.trigger("odkControl-propertiesUpdated")
                } else {
                    e.attr("disabled", true);
                    f.value = false;
                    g.trigger("odkControl-propertiesUpdated")
                }
            })
        },"enum": function(f, h, g) {
            h.find("h4").text(f.name);
            h.find("p").text(f.description);
            var e = h.find(".editorSelect");
            _.each(f.options, function(i) {
                e.append(d("<option>" + i + "</option>"))
            });
            e.val(f.value);
            e.change(function(i) {
                f.value = d(this).val();
                g.trigger("odkControl-propertiesUpdated")
            });
            f.value = e.val()
        },dateRange: function(e, g, f) {
            d.fn.propertyEditor.editors.numericRange(e, g, f);
            g.find(".editorTextfield").datepicker({dateFormat: "yy-mm-dd",onSelect: function(i, h) {
                    d(h.input).trigger("keyup")
                }})
        },optionsEditor: function(f, h, g) {
            h.find("h4").text(f.name);
            h.find("p").text(f.description);
            var e = h.find(".optionsList");
            _.each(f.value, function(k, j) {
                if (k.text === undefined || k.text === null) {
                    k.text = {}
                }
                e.append(b(f, k, j, g))
            });
            h.find(".addOption").click(function(j) {
                j.preventDefault();
                var i = {text: {}};
                f.value.push(i);
                e.append(b(f, i, e.children().length, g));
                g.trigger("odkControl-propertiesUpdated")
            });
            h.find(".optionsEditorLink").click(function(i) {
                odkmaker.options.currentProperty = f.value;
                odkmaker.options.optionsUpdated = function(k) {
                    f.value = k;
                    g.trigger("odkControl-propertiesUpdated");
                    var j = d("<li/>").propertyEditor(f, h.attr("data-name"), g);
                    h.closest("li").replaceWith(j)
                }
            })
        }};
    var b = function(h, g, e, j) {
        var i = d('<a href="#removeOption" class="removeOption">Remove Option</a>');
        i.click(function(l) {
            l.preventDefault();
            d.removeFromArray(g, h.value);
            var k = d(this).closest(".optionsList");
            d(this).closest("li").remove();
            k.children().each(function(m) {
                d(this).toggleClass("even", (m % 2) == 0).find("h4").text("Option " + (m + 1))
            });
            j.trigger("odkControl-propertiesUpdated")
        });
        var f = d("#templates .editors .optionsEditorValueField").clone();
        f.find(".editorTextfield").val(g.val || "").keyup(function(k) {
            g.val = d(this).val();
            j.trigger("odkControl-propertiesUpdated")
        });
        return d("<li></li>").toggleClass("even", (e % 2) == 0).append(d("#templates .editors .uiText").clone().propertyEditor({name: "Option " + (e + 1),type: "uiText",value: g.text}, j).prepend(i).append(f))
    }
})(jQuery);
/* workspace-draggable.js */
(function(d) {
    var f;
    var e = false;
    var c = function(g, i) {
        var h = d(".workspaceScrollArea");
        var j = h.offset();
        if (g.top < (j.top + i.scrollMargin)) {
            if (!e) {
                e = true;
                clearInterval(f);
                f = setInterval(function() {
                    h.scrollTop(h.scrollTop() - i.scrollSpeed)
                }, i.scrollSpeed)
            }
        } else {
            if (g.top > (j.top + h.outerHeight(false) - i.scrollMargin)) {
                if (!e) {
                    e = true;
                    clearInterval(f);
                    f = setInterval(function() {
                        h.scrollTop(h.scrollTop() + i.scrollSpeed)
                    }, i.scrollSpeed)
                }
            } else {
                e = false;
                clearInterval(f)
            }
        }
    };
    var b = function(h, g, i, l) {
        if (g.top > h.innerHeight()) {
            h.find(".placeholder").addClass("closing").slideUp("normal", function() {
                d(this).remove()
            });
            return false
        }
        if ((l === undefined) || (l === null)) {
            l = h
        }
        if (l.children(":not(.placeholder)").length === 0) {
            if (l.find(".placeholder").length === 0) {
                i.dragCallback(l, 0)
            }
            return true
        }
        var j = l.offset().top - h.offset().top;
        var k = false;
        l.children().each(function() {
            var n = d(this);
            if (n.is(".placeholder")) {
                j += n.outerHeight(true);
                return
            } else {
                if (n.is(".group")) {
                    var o = n.children(".workspaceInnerWrapper").children(".workspaceInner");
                    k = b(n, {top: g.top - j,left: g.left}, i, o);
                    if (k) {
                        return false
                    }
                }
            }
            var m = n.innerHeight() / 3;
            if (g.top < (j + m)) {
                if (!n.prev().is(".placeholder")) {
                    i.dragCallback(n, -1)
                }
                k = true;
                return false
            }
            j += n.outerHeight(true);
            if ((g.top > (j - m)) && (g.top < j)) {
                if (!n.next().is(".placeholder")) {
                    i.dragCallback(n, 1)
                }
                k = true;
                return false
            }
        });
        return k
    };
    var a = function(l, g, i) {
        var h = d(".workspaceScrollArea");
        var k = h.offset();
        if ((g.left < k.left) || (g.left > (k.left + h.outerWidth(false))) || (g.top < k.top) || (g.top > (k.top + h.outerHeight(false)))) {
            return
        }
        var m = d(".workspace");
        var j = k.top - h.scrollTop() + h.spacingTop() + m.spacingTop();
        g.top -= j;
        if ((!b(m, g, i)) && (m.children(":last-child").is(":not(.placeholder)"))) {
            i.dragCallback(m.children(":last-child"), 1)
        }
    };
    d.fn.workspaceDraggable = function(g) {
        var g = d.extend({}, d.fn.workspaceDraggable.defaults, g);
        return this.each(function() {
            var i = d(this);
            var h = d.meta ? d.extend({}, g, i.data()) : g;
            d(this).draggable(d.extend({}, {addClass: false,appendTo: "body",distance: 5,helper: "clone",opacity: 0.8,scroll: false,drag: function(j, k) {
                    c({left: k.position.left,top: k.position.top}, h);
                    a(i, {left: k.position.left,top: k.position.top}, h)
                },stop: function(j, k) {
                    clearInterval(f);
                    h.dropCallback(k.helper)
                }}, g.draggableOptions))
        })
    };
    d.fn.workspaceDraggable.defaults = {dragCallback: function(g, h) {
        },draggableOptions: {},dropCallback: function() {
        },insertCallback: function() {
        },scrollInterval: 10,scrollMargin: 40,scrollSpeed: 10}
})(jQuery);
/* control.js */
(function(c) {
    var a = function(j, h, e, g) {
        var f = j.children(".controlInfo");
        var d = f.children(".controlHeadline");
        f.children(".controlName").text(g.name.value);
        if (h == "group") {
            d.children(".controlLabel").text(c.emptyString(g.label.value[odkmaker.i18n.displayLanguage()], "[no group caption text yet]"))
        } else {
            if (h == "metadata") {
            } else {
                d.children(".controlLabel").text(c.emptyString(g.label.value[odkmaker.i18n.displayLanguage()], "[no caption text yet]"));
                d.children(".controlHint").text(g.hint.value[odkmaker.i18n.displayLanguage()])
            }
        }
        var i = f.children(".controlProperties");
        i.empty();
        _.each(g, function(k) {
            if ((k.summary === false) || (k.value !== true)) {
                return
            }
            i.append(c("<li>" + k.name + "</li>"))
        });
        if (j.hasClass("selected")) {
            c(".propertyList > li, .advancedProperties > li").trigger("odkProperty-validate")
        }
        j.toggleClass("error", _.any(g, function(k) {
            return _.isArray(k.validationErrors) && (k.validationErrors.length > 0)
        }))
    };
    var b = function(i, g, d, e) {
        c(".workspace .control.selected").removeClass("selected");
        i.addClass("selected");
        var h = c(".propertyList");
        h.empty();
        var f = c.tag({_: "li","class": "advanced",contents: [{_: "a","class": "toggle",href: "#advanced",contents: [{_: "div","class": "icon"}, "Advanced"]}, {_: "ul","class": "advancedProperties toggleContainer",style: {display: "none"}}]});
        var j = f.find(".advancedProperties");
        _.each(e, function(l, k) {
            c("<li/>").propertyEditor(l, k, i).appendTo((l.advanced === true) ? j : h)
        });
        h.append(f)
    };
    c.fn.odkControl = function(f, e, d) {
        if (c.fn.odkControl.controlProperties[f] === undefined) {
            return
        }
        var e = c.extend({}, c.fn.odkControl.defaults, e);
        return this.each(function() {
            var i = c(this);
            i.data("odkControl-type", f);
            var h = null;
            if ((f == "group") || (f == "branch") || (f == "metadata")) {
                h = d || c.extend(true, {}, c.fn.odkControl.controlProperties[f])
            } else {
                h = d || c.extend(true, c.extend(true, {}, c.fn.odkControl.defaultProperties), c.fn.odkControl.controlProperties[f])
            }
            if (h.name.value == "untitled") {
                h.name.value += (_.uniqueId() + 1)
            }
            i.data("odkControl-properties", h);
            i.bind("odkControl-propertiesUpdated", function(j) {
                j.stopPropagation();
                a(i, f, e, h)
            });
            i.trigger("odkControl-propertiesUpdated");
            i.bind("odkControl-reloadProperties", function(j) {
                b(i, f, e, h)
            });
            i.click(function(j) {
                j.stopPropagation();
                b(i, f, e, h)
            });
            b(i, f, e, h);
            if (f == "group") {
                c('<div class="workspaceInnerWrapper"><div class="workspaceInner"></div></div><div class="groupFooter"></div>').insertAfter(i.children(".controlInfo"))
            }
            i.find(".deleteControl").click(function(j) {
                j.preventDefault();
                i.slideUp("normal", function() {
                    if (i.is(".selected")) {
                        c(".propertyList").empty()
                    }
                    i.remove()
                })
            });
            var g = 0;
            i.workspaceDraggable({draggableOptions: {start: function(j, k) {
                        k.helper.width(i.width());
                        g = i.outerHeight(true);
                        i.after(c('<div class="placeholder hidden"></div>').css("height", g + "px")).hide().appendTo(c("body"))
                    }},dragCallback: function(k, l) {
                    c(".workspace .placeholder.hidden").addClass("closing").stop().slideUp("fast", function() {
                        c(this).remove()
                    });
                    c(".control.ui-draggable-dragging").toggleClass("last", k.is(":last-child") && (l > 0));
                    var j = c('<div class="placeholder hidden"></div>').css("height", g + "px").slideDown("fast");
                    if (l < 0) {
                        k.before(j)
                    } else {
                        if (l == 0) {
                            k.append(j)
                        } else {
                            if (l > 0) {
                                k.after(j)
                            }
                        }
                    }
                },dropCallback: function(k) {
                    var j = c(".workspace .placeholder:not(.closing)");
                    if (j.length == 1) {
                        j.replaceWith(i)
                    } else {
                        i.appendTo(".workspace")
                    }
                    i.show()
                },insertPlaceholder: false});
            _.defer(function() {
                i.find(".controlFlowArrow").triangle()
            })
        })
    };
    c.fn.odkControl.defaults = {};
    c.fn.odkControl.defaultProperties = {name: {name: "Data Name",type: "text",description: "The data name of this field in the final exported XML.",limit: ["required", "alphanumeric", "unique"],required: true,value: "untitled",summary: false},label: {name: "Caption Text",type: "uiText",description: "The name of this field as it is presented to the user.",required: true,value: {},summary: false},hint: {name: "Hint",type: "uiText",description: "Additional help for this question.",value: {},summary: false},defaultValue: {name: "Default Value",type: "text",description: "The value this field is presented with at first.",value: "",summary: false},readOnly: {name: "Read Only",type: "bool",description: "Whether this field can be edited by the end user or not.",value: false,summary: true},required: {name: "Required",type: "bool",description: "Whether this field must be filled in before continuing.",value: false,summary: true},relevance: {name: "Relevance",type: "text",description: "Specify a custom expression to evaluate to determine if this field is shown.",value: "",advanced: true,summary: false},constraint: {name: "Constraint",type: "text",description: "Specify a custom expression to validate the user input.",value: "",advanced: true,summary: false},destination: {name: "Instance Destination",type: "text",description: "Specify a custom XPath expression at which to store the result.",value: "",advanced: true,summary: false},calculate: {name: "Calculate",type: "text",description: "Specify a custom expression to store a value in this field",value: "",advanced: true,summary: false}};
    c.fn.odkControl.controlProperties = {inputText: {length: {name: "Length",type: "numericRange",description: "Valid lengths for this user input of this control.",value: false,summary: false},invalidText: {name: "Invalid Text",type: "uiText",description: "Message to display if the value fails the length check.",value: {},summary: false}},inputNumeric: {range: {name: "Range",type: "numericRange",description: "Valid range for the user input of this control.",value: false,summary: false},invalidText: {name: "Invalid Text",type: "uiText",description: "Message to display if the value fails the range check.",value: {},summary: false},kind: {name: "Kind",type: "enum",description: "Type of number accepted.",options: ["Integer", "Decimal"],value: "Integer",summary: true}},inputDate: {range: {name: "Range",type: "dateRange",description: "Valid range for the user input of this control.",value: false,summary: false},invalidText: {name: "Invalid Text",type: "uiText",description: "Message to display if the value fails the range check.",value: {},summary: false}},inputLocation: {},inputMedia: {kind: {name: "Kind",type: "enum",description: "Type of media to upload.",options: ["Image", "Audio", "Video"]}},inputBarcode: {},inputSelectOne: {options: {name: "Options",type: "optionsEditor",value: [],summary: false}},inputSelectMany: {options: {name: "Options",type: "optionsEditor",value: [],summary: false}},group: {name: {name: "Name",type: "text",description: "The data name of this group in the final exported XML.",limit: ["required", "alphanumeric", "unique"],required: true,value: "untitled",summary: false},label: {name: "Label",type: "uiText",description: "Give the group a label to give a visual hint to the user.",required: true,value: {},summary: false},loop: {name: "Looped",type: "bool",description: "Whether or not to allow this group to loop.",value: false},fieldList: {name: "Display On One Screen",type: "bool",description: "Display all the controls in this group on one screen",value: false},relevance: {name: "Relevance",type: "text",description: "Specify a custom expression to evaluate to determine if this group is shown.",value: "",advanced: true,summary: false}},branch: {logic: {name: "Rules",type: "logicEditor",description: "Specify the rules that decide how the form will branch.",value: [],summary: false}},metadata: {name: {name: "Data Name",type: "text",description: "The data name of this field in the final exported XML.",limit: ["required", "alphanumeric", "unique"],required: true,value: "untitled",summary: false},kind: {name: "Kind",type: "enum",description: "Type of metadata to add.",options: ["Device ID", "Start Time", "End Time"],value: "Device ID",summary: true}},}
})(jQuery);
/* toolbutton.js */
(function(a) {
    var b = function(c) {
        return a("#templates .control").clone().addClass(c).odkControl(c).trigger("odkControl-select")
    };
    a.fn.toolButton = function(c) {
        return this.each(function() {
            var d = a(this);
            d.click(function(e) {
                e.preventDefault();
                a(".workspace").append(b(d.attr("rel")))
            });
            d.workspaceDraggable({dragCallback: function(f, g) {
                    a(".workspace .placeholder").addClass("closing").slideUp("normal", function() {
                        a(this).remove()
                    });
                    var e = a('<div class="placeholder"></div>').text(d.text()).append('<div class="flowArrow"></div>').slideDown("normal");
                    if (g < 0) {
                        f.before(e)
                    } else {
                        if (g == 0) {
                            f.append(e)
                        } else {
                            if (g > 0) {
                                f.after(e)
                            }
                        }
                    }
                },dropCallback: function() {
                    var e = a(".workspace .placeholder:not(.closing)");
                    if (e.length > 0) {
                        e.replaceWith(b(d.attr("rel")))
                    }
                },draggableOptions: {start: function(e, f) {
                        a(f.helper).empty().append(a('<div class="typeIcon></div>"'))
                    }}})
        })
    }
})(jQuery);
/* dropdown-menu.js */
(function(a) {
    a.fn.dropdownMenu = function(b) {
        return this.each(function() {
            var c = a(this);
            c.click(function(e) {
                c.children(".submenu").slideDown("fast");
                c.addClass("open");
                var d = _.uniqueId();
                a(document).bind("click.menu_" + d, function(g) {
                    var f = a(g.target);
                    if (f.parents().index(c[0]) < 0 || f.is("a")) {
                        var h = f.closest("li");
                        if (h.hasClass("checkbox")) {
                            h.toggleClass("selected")
                        } else {
                            if (h.hasClass("radio")) {
                                h.siblings().removeClass("selected");
                                h.addClass("selected")
                            }
                        }
                        a(document).unbind("click.menu_" + d);
                        c.removeClass("open");
                        c.children(".submenu").slideUp("fast")
                    }
                })
            })
        })
    }
})(jQuery);
/* application.js */
var applicationNS = odkmaker.namespace.load("odkmaker.application");
applicationNS.newForm = function() {
    $(".workspace").empty();
    $(".header h1").text("Untitled Form");
    $(".propertiesPane .propertylist").empty().append('<li class="emptyData">First add a control, then select it to view its properties here.</li>');
    odkmaker.data.currentForm = null
};
$(function() {
    $(".header .menu li").dropdownMenu();
    $.live(".header .menu .displayLanguages a", "click", function(a) {
        a.preventDefault();
        odkmaker.i18n.displayLanguage($(this).attr("rel"));
        $(".workspace .control").trigger("odkControl-propertiesUpdated")
    });
    $(".header .menu .toggleCollapsed").click(function(a) {
        a.preventDefault();
        $(".workspace").toggleClass("collapsed");
        $(".controlFlowArrow").empty().triangle()
    });
    $("#editTitleLink").click(function(a) {
        a.preventDefault();
        var b = $(".xform_header #renameFormField");
        if (b.is(":visible")) {
            $(".xform_header h1").text(b.hide().val()).fadeIn();
            $(this).text("Rename")
        } else {
            b.val($(".xform_header h1").hide().text()).fadeIn();
            $(this).text("Done")
        }
    });
    $(".toolPalette a").toolButton();
    applicationNS.newForm();
    $.live("a.toggle", "click", function(a) {
        a.preventDefault();
        $(this).toggleClass("expanded").siblings(".toggleContainer").slideToggle("normal")
    });
    $("a[rel$='external']").click(function() {
        this.target = "_blank"
    });
    $(window).resize(function(a) {
        $(".workspace").css("min-height", ($(".workspaceScrollArea").innerHeight() - 320) + "px")
    }).resize();
    setTimeout(function() {
        $(".loadingScreen .status").text("checking who you are...")
    }, 0)
});
