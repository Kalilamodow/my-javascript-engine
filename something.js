function doStuff(a, b) {
    console.log({ a: a * 2, b: b.repeat(44) });
}

var a_param = 4;
var b_param = "sup";

var result = doStuff(a_param, b_param);
console.log(result);
