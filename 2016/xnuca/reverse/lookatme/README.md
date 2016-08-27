这道题一部分代码在java，一部分代码在native，java部分用jadx-gui，native部分用IDA，把逻辑弄清楚就很容易了。

在处理输入字符串的过程中，程序读取了一个文件`/data/data/oct.rd6.iie.crackme/files/cache`并从中读取了几个字节，用来进行后续计算

代码如下：
```javascript
// simulate
let str = 'd513beba042b7944';
str = Array.prototype.slice.apply(Buffer(str, 'utf8'));

function swap_char(i, j) {
    let t = str[i];
    str[i] = str[j];
    str[j] = t;
}

function onHighMemory(g, m, n) {
    let result = (g[2]*12*g[2]) + (g[3]*13*g[3]) + (g[2]*14*g[3]) + g[1]*15*g[0] + 16;
    if (g[0] ^ n === g[1] && result === m) return true;
    return false;
}

function sub_1088(str, a2) {
    let v4 = Buffer(4);
    for (let i = 0; i < 4; i++) {
        v4[i] = (str[4 * i + 3] + a2) % 128;
    }
    return v4[0] === 58 && v4[1] == 109 && v4[2] === 105 && v4[3] === 104;
}

swap_char(0,8);
swap_char(1,3);
swap_char(7,2);
swap_char(11,3);
swap_char(14,9);
swap_char(4,10);
for (let i = 0; i < str.length; i++) str[i] ^= 0x76/*read from file 'cache'*/;

let r = false;
if (str[0] == 70 && str[4] == 68 && str[8] == 18 && str[12] === 65) r = true;
if (!r) throw Error();

let v18 = [0x03, 0x57, 0x50, 0x0E];
let v19 = [
    0x16156,
    0x1ac29,
    0x185a9,
    0x3c48d
];
for (let p = 0; p < 4; p++) {
    let g = str.slice(p*4, p*4 + 4);
    let m = v19[p];
    let n = v18[p];
    if (!onHighMemory(g, m, n)) throw Error();
}
if (!sub_1088(str, 0xA6/*read from file 'cache'*/)) throw Error();

// str = [ 70, 69, 23, 20, 68, 19, 20, 71, 18, 66, 20, 67, 65, 79, 66, 66 ];

// reverse
str = [ 70, -1, -1, 58, 68, -1, -1, 109, 18, -1, -1, 105, 65, -1, -1, 104 ];
for (let i = 3; i < 16; i += 4) str[i] = (str[i] - 0xA6 + 256*2) % 128;
for (let i = 0; i < 4; i++) str[i*4+1] = str[i*4] ^ v18[i];
for (let i = 0; i < 4; i++) {
    let a = 12;
    let b = 14 * str[i*4+3];
    let c = str[i*4+3] * str[i*4+3] * 13 + str[i*4+1] * str[i*4] * 15 + 16 - v19[i];
    str[i*4+2] = (-b + Math.sqrt(b*b-4*a*c)) / (2*a);
}
for (let i = 0; i < str.length; i++) str[i] ^= 0x76;
swap_char(4,10);
swap_char(14,9);
swap_char(11,3);
swap_char(7,2);
swap_char(1,3);
swap_char(0,8);
console.log(Buffer(str).toString('utf8'));
```
