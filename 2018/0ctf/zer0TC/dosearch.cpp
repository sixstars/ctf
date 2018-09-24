// Too slow. Only 1/8 of key recovery here

#include<iostream>
#include<fstream>
#include<vector>
#include<map>
#include<algorithm>
#include<stdint.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

using namespace std;


/*
 * Addition in GF(2^8)
 * http://en.wikipedia.org/wiki/Finite_field_arithmetic
 */
uint8_t gadd(uint8_t a, uint8_t b) {
	return a^b;
}

/*
 * Subtraction in GF(2^8)
 * http://en.wikipedia.org/wiki/Finite_field_arithmetic
 */
uint8_t gsub(uint8_t a, uint8_t b) {
	return a^b;
}

/*
 * Multiplication in GF(2^8)
 * http://en.wikipedia.org/wiki/Finite_field_arithmetic
 * Irreducible polynomial m(x) = x8 + x4 + x3 + x + 1
 */
uint8_t gmult(uint8_t a, uint8_t b) {

	uint8_t p = 0, i = 0, hbs = 0;

	for (i = 0; i < 8; i++) {
		if (b & 1) {
			p ^= a;
		}

		hbs = a & 0x80;
		a <<= 1;
		if (hbs) a ^= 0x1b; // 0000 0001 0001 1011	
		b >>= 1;
	}

	return (uint8_t)p;
}

/*
 * Addition of 4 byte words
 * m(x) = x4+1
 */
void coef_add(uint8_t a[], uint8_t b[], uint8_t d[]) {

	d[0] = a[0]^b[0];
	d[1] = a[1]^b[1];
	d[2] = a[2]^b[2];
	d[3] = a[3]^b[3];
}

/*
 * Multiplication of 4 byte words
 * m(x) = x4+1
 */
void coef_mult(uint8_t *a, uint8_t *b, uint8_t *d) {

	d[0] = gmult(a[0],b[0])^gmult(a[3],b[1])^gmult(a[2],b[2])^gmult(a[1],b[3]);
	d[1] = gmult(a[1],b[0])^gmult(a[0],b[1])^gmult(a[3],b[2])^gmult(a[2],b[3]);
	d[2] = gmult(a[2],b[0])^gmult(a[1],b[1])^gmult(a[0],b[2])^gmult(a[3],b[3]);
	d[3] = gmult(a[3],b[0])^gmult(a[2],b[1])^gmult(a[1],b[2])^gmult(a[0],b[3]);
}

/*
 * The cipher Key.	
 */
int K;

/*
 * Number of columns (32-bit words) comprising the State. For this 
 * standard, Nb = 4.
 */
int Nb = 4;

/*
 * Number of 32-bit words comprising the Cipher Key. For this 
 * standard, Nk = 4, 6, or 8.
 */
int Nk;

/*
 * Number of rounds, which is a function of  Nk  and  Nb (which is 
 * fixed). For this standard, Nr = 10, 12, or 14.
 */
int Nr;

/*
 * S-box transformation table
 */
static uint8_t s_box[256] = { 103, 172, 53, 159, 102, 168, 133, 197, 174, 182, 41, 164, 220, 58, 118, 63, 161, 50, 89, 242, 253, 74, 250, 119, 108, 122, 120, 216, 60, 208, 178, 20, 180, 187, 117, 213, 48, 90, 218, 46, 190, 188, 111, 252, 56, 77, 169, 232, 135, 72, 44, 115, 130, 57, 96, 155, 105, 181, 83, 0, 204, 139, 9, 7, 138, 23, 145, 97, 185, 13, 254, 69, 24, 34, 158, 76, 222, 165, 2, 247, 226, 6, 183, 116, 206, 21, 225, 210, 219, 36, 129, 100, 141, 62, 198, 28, 207, 84, 184, 99, 160, 215, 52, 73, 153, 42, 191, 26, 162, 194, 235, 81, 238, 110, 43, 214, 234, 221, 70, 80, 148, 176, 251, 245, 151, 244, 132, 14, 29, 94, 137, 131, 189, 31, 231, 47, 68, 8, 11, 249, 243, 37, 203, 200, 202, 255, 236, 112, 51, 10, 98, 79, 19, 59, 228, 177, 192, 75, 85, 45, 121, 27, 147, 179, 1, 201, 123, 18, 167, 166, 239, 146, 49, 196, 163, 109, 15, 143, 144, 150, 65, 106, 25, 124, 54, 241, 16, 92, 227, 217, 104, 173, 223, 86, 113, 39, 157, 199, 126, 71, 33, 61, 38, 142, 87, 22, 237, 152, 55, 212, 248, 175, 149, 170, 246, 88, 17, 64, 209, 171, 240, 224, 154, 211, 78, 93, 205, 114, 136, 12, 40, 101, 5, 95, 233, 35, 186, 195, 230, 127, 91, 229, 193, 32, 30, 4, 140, 66, 134, 128, 125, 82, 3, 67, 107, 156};

/*
 * Inverse S-box transformation table
 */
static uint8_t inv_s_box[256] = {59, 164, 78, 252, 245, 232, 81, 63, 137, 62, 149, 138, 229, 69, 127, 176, 186, 216, 167, 152, 31, 85, 205, 65, 72, 182, 107, 161, 95, 128, 244, 133, 243, 200, 73, 235, 89, 141, 202, 195, 230, 10, 105, 114, 50, 159, 39, 135, 36, 172, 17, 148, 102, 2, 184, 208, 44, 53, 13, 153, 28, 201, 93, 15, 217, 180, 247, 253, 136, 71, 118, 199, 49, 103, 21, 157, 75, 45, 224, 151, 119, 111, 251, 58, 97, 158, 193, 204, 215, 18, 37, 240, 187, 225, 129, 233, 54, 67, 150, 99, 91, 231, 4, 0, 190, 56, 181, 254, 24, 175, 113, 42, 147, 194, 227, 51, 83, 34, 14, 23, 26, 160, 25, 166, 183, 250, 198, 239, 249, 90, 52, 131, 126, 6, 248, 48, 228, 130, 64, 61, 246, 92, 203, 177, 178, 66, 171, 162, 120, 212, 179, 124, 207, 104, 222, 55, 255, 196, 74, 3, 100, 16, 108, 174, 11, 77, 169, 168, 5, 46, 213, 219, 1, 191, 8, 211, 121, 155, 30, 163, 32, 57, 9, 82, 98, 68, 236, 33, 41, 132, 40, 106, 156, 242, 109, 237, 173, 7, 94, 197, 143, 165, 144, 142, 60, 226, 84, 96, 29, 218, 87, 223, 209, 35, 115, 101, 27, 189, 38, 88, 12, 117, 76, 192, 221, 86, 80, 188, 154, 241, 238, 134, 47, 234, 116, 110, 146, 206, 112, 170, 220, 185, 19, 140, 125, 123, 214, 79, 210, 139, 22, 122, 43, 20, 70, 145};


static uint8_t ptable[64] = {
    16, 19, 23, 9, 22, 20, 21, 17, 
    40, 43, 44, 47, 41, 45, 57, 42, 
    36, 32, 38, 33, 55, 37, 34, 35, 
    50, 53, 48, 52, 39, 54, 49, 51, 
    10, 11, 14, 8, 13, 15, 18, 12, 
    0, 7, 2, 3, 4, 1, 5, 31, 
    63, 46, 58, 62, 61, 59, 56, 60, 
    6, 29, 25, 24, 30, 27, 28, 26
}; 

static uint8_t inv_ptable[64] = { 40, 45, 42, 43, 44, 46, 56, 41, 35, 3, 32, 33, 39, 36, 34, 37, 0, 7, 38, 1, 5, 6, 4, 2, 59, 58, 63, 61, 62, 57, 60, 47, 17, 19, 22, 23, 16, 21, 18, 28, 8, 12, 15, 9, 10, 13, 49, 11, 26, 30, 24, 31, 27, 25, 29, 20, 54, 14, 50, 53, 55, 52, 51, 48};
/*
 * Generates the round constant Rcon[i]
 */
uint8_t R[] = {0x02, 0x00, 0x00, 0x00};
 
uint8_t * Rcon(uint8_t i) {
	
	if (i == 1) {
		R[0] = 0x01; // x^(1-1) = x^0 = 1
	} else if (i > 1) {
		R[0] = 0x02;
		i--;
		while (i-1 > 0) {
			R[0] = gmult(R[0], 0x02);
			i--;
		}
	}
	
	return R;
}

/*
 * Transformation in the Cipher and Inverse Cipher in which a Round 
 * Key is added to the State using an XOR operation. The length of a 
 * Round Key equals the size of the State (i.e., for Nb = 4, the Round 
 * Key length equals 128 bits/16 bytes).
 */
void add_round_key(uint8_t *state, uint8_t *w, uint8_t r) {
	
	uint8_t c;
	
	for (c = 0; c < 8; c++) {
        state[c] = state[c]^w[8*r+c];
	}
}

/*
 * Transformation in the Cipher that takes all of the columns of the 
 * State and mixes their data (independently of one another) to 
 * produce new columns.
 */
void mix_columns(uint8_t *state) {

	uint8_t a[] = {0x02, 0x01, 0x01, 0x03}; // a(x) = {02} + {01}x + {01}x2 + {03}x3
	uint8_t i, j, col[4], res[4];

	for (j = 0; j < Nb; j++) {
		for (i = 0; i < 4; i++) {
			col[i] = state[Nb*i+j];
		}

		coef_mult(a, col, res);

		for (i = 0; i < 4; i++) {
			state[Nb*i+j] = res[i];
		}
	}
}

/*
 * Transformation in the Inverse Cipher that is the inverse of 
 * MixColumns().
 */
void inv_mix_columns(uint8_t *state) {

	uint8_t a[] = {0x0e, 0x09, 0x0d, 0x0b}; // a(x) = {0e} + {09}x + {0d}x2 + {0b}x3
	uint8_t i, j, col[4], res[4];

	for (j = 0; j < Nb; j++) {
		for (i = 0; i < 4; i++) {
			col[i] = state[Nb*i+j];
		}

		coef_mult(a, col, res);

		for (i = 0; i < 4; i++) {
			state[Nb*i+j] = res[i];
		}
	}
}

/*
 * Transformation in the Cipher that processes the State by cyclically 
 * shifting the last three rows of the State by different offsets. 
 */
void shift_rows(uint8_t *state) {

	uint8_t i, k, s, tmp;

	for (i = 1; i < 4; i++) {
		// shift(1,4)=1; shift(2,4)=2; shift(3,4)=3
		// shift(r, 4) = r;
		s = 0;
		while (s < i) {
			tmp = state[Nb*i+0];
			
			for (k = 1; k < Nb; k++) {
				state[Nb*i+k-1] = state[Nb*i+k];
			}

			state[Nb*i+Nb-1] = tmp;
			s++;
		}
	}
}

/*
 * Transformation in the Inverse Cipher that is the inverse of 
 * ShiftRows().
 */
void inv_shift_rows(uint8_t *state) {

	uint8_t i, k, s, tmp;

	for (i = 1; i < 4; i++) {
		s = 0;
		while (s < i) {
			tmp = state[Nb*i+Nb-1];
			
			for (k = Nb-1; k > 0; k--) {
				state[Nb*i+k] = state[Nb*i+k-1];
			}

			state[Nb*i+0] = tmp;
			s++;
		}
	}
}

/*
 * Transformation in the Cipher that processes the State using a non­
 * linear byte substitution table (S-box) that operates on each of the 
 * State bytes independently. 
 */
void sub_bytes(uint8_t *state) {
	uint8_t i, j;

	for (i = 0; i < 8; i++) {
		state[i] = s_box[state[i]];
	}
}
void inv_sub_bytes(uint8_t *state) {
	uint8_t i, j;

	for (i = 0; i < 8; i++) {
		state[i] = inv_s_box[state[i]];
	}
}

static uint8_t pow2[8] = {1, 2, 4, 8, 16, 32, 64, 128};

void permutation(uint8_t *state) {
	uint8_t state2[8];
	uint8_t i, j, x, y;
    memset(state2, 0, sizeof(state2));
    for (i=0; i<64; i++) {
        x = ptable[i]/8;
        y = ptable[i]%8;
        if ((state[x]&pow2[7-y])>0)
            state2[i/8]+=pow2[7-i%8];

    }

	for (i = 0; i < 8; i++) {
		state[i] = state2[i];
	}

}

uint8_t p_next[8] = {5, 4, 0, 7, 2, 1, 3, 6};
uint8_t p_prev[8] = {2, 5, 4, 6, 1, 0, 7, 3};

uint8_t permuone(uint8_t byte, uint8_t pos, uint8_t extra) {
	uint8_t byte2 = 0;
	uint8_t i, x, y;
    uint8_t p2 = p_next[pos];
    for (i=p2*8; i<(p2+1)*8; i++) {
        x = ptable[i]/8;
        y = ptable[i]%8;
        if (x==pos) {
            if ((byte&pow2[7-y])>0)
                byte2+=pow2[7-i%8];
        } else {
            if (extra)
                byte2+=pow2[7-i%8];
        }
    }

    return byte2;
}

uint8_t inv_permuone(uint8_t byte, uint8_t pos, uint8_t extra) {
	uint8_t byte2 = 0;
	uint8_t i, x, y;
    uint8_t p2 = p_prev[pos];
    for (i=p2*8; i<(p2+1)*8; i++) {
        x = inv_ptable[i]/8;
        y = inv_ptable[i]%8;
        if (x==pos) {
            if ((byte&pow2[7-y])>0)
                byte2+=pow2[7-i%8];
        } else {
            if (extra)
                byte2+=pow2[7-i%8];
        }
    }

    return byte2;
}

/*
 * Transformation in the Inverse Cipher that is the inverse of 
 * SubBytes().
 */

/*
 * Function used in the Key Expansion routine that takes a four-byte 
 * input word and applies an S-box to each of the four bytes to 
 * produce an output word.
 */
void sub_word(uint8_t *w) {

	uint8_t i;

	for (i = 0; i < 4; i++) {
		w[i] = s_box[16*((w[i] & 0xf0) >> 4) + (w[i] & 0x0f)];
	}
}

/*
 * Function used in the Key Expansion routine that takes a four-byte 
 * word and performs a cyclic permutation. 
 */
void rot_word(uint8_t *w) {

	uint8_t tmp;
	uint8_t i;

	tmp = w[0];

	for (i = 0; i < 3; i++) {
		w[i] = w[i+1];
	}

	w[3] = tmp;
}

uint8_t rcon[16] = {0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a};
static int rounds=5;

/*
 * Key Expansion
 */
void key_expansion(uint8_t *key, uint8_t *w) {

	uint8_t tmp[4], tmp2[4];
	uint8_t i, j, k;
	int cur=8;

	for (i = 0; i < 8; i++) {
        w[i] = key[i];
	}
	for (i = 0; i < 4; i++) {
        tmp[i] = key[4+i];
	}

	for (i = 1; i <= rounds; i++) {
        tmp2[0] = tmp[1];
        tmp2[1] = tmp[2];
        tmp2[2] = tmp[3];
        tmp2[3] = tmp[0];
        for (j=0;j<4;j++)
            tmp[j]=s_box[tmp2[j]];
        tmp[0] ^= rcon[i];
        for (j=0; j<2; j++) {
            for (k=0; k<4; k++)
                tmp[k] ^= w[cur-8+k];
            for (k=0; k<4; k++)
                w[cur+k] = tmp[k];
            cur += 4;
        }

	}
}

void cipher(uint8_t *in, uint8_t *out, uint8_t *w) {

	uint8_t state[16];
	uint8_t r, i, j;

	for (i = 0; i < 8; i++) {
        state[i] = in[i];
	}

	for (r = 0; r < rounds; r++) {
		add_round_key(state, w, r);
		sub_bytes(state);
		if (r != rounds-1)
			permutation(state);
	}

	add_round_key(state, w, rounds);

	for (i = 0; i < 8; i++) {
        out[i] = state[i];
	}
}

void inv_cipher(uint8_t *in, uint8_t *out, uint8_t *w) {

	uint8_t state[4*Nb];
	uint8_t r, i, j;

	for (i = 0; i < 4; i++) {
		for (j = 0; j < Nb; j++) {
			state[Nb*i+j] = in[i+4*j];
		}
	}

	add_round_key(state, w, Nr);

	for (r = Nr-1; r >= 1; r--) {
		inv_shift_rows(state);
		inv_sub_bytes(state);
		add_round_key(state, w, r);
		inv_mix_columns(state);
	}

	inv_shift_rows(state);
	inv_sub_bytes(state);
	add_round_key(state, w, 0);

	for (i = 0; i < 4; i++) {
		for (j = 0; j < Nb; j++) {
			out[i+4*j] = state[Nb*i+j];
		}
	}
}

int notmain() {

	uint8_t i;

	uint8_t key[] = {
		0x00, 0x01, 0x02, 0x03,
		0x04, 0x05, 0x06, 0x07};

	uint8_t in[] = {
		0x00, 0x11, 0x22, 0x33,
		0xcc, 0xdd, 0xee, 0xff};
	
	uint8_t out[16]; // 128
	
	uint8_t *w; // expanded key

	w = malloc(8*10*rounds);

	key_expansion(key, w);
	for (i = 8; i < 10; i++) {
		printf("%x %x %x %x ", w[4*i+0], w[4*i+1], w[4*i+2], w[4*i+3]);
	}

	cipher(in /* in */, out /* out */, w /* expanded key */);

	printf("out:\n");
	
	for (i = 0; i < 2; i++) {
		printf("%x %x %x %x ", out[4*i+0], out[4*i+1], out[4*i+2], out[4*i+3]);
	}

	printf("\n");

/*
	inv_cipher(out, in, w);

	printf("msg:\n");
	for (i = 0; i < 4; i++) {
		printf("%x %x %x %x ", in[4*i+0], in[4*i+1], in[4*i+2], in[4*i+3]);
	}

	printf("\n");
*/
	exit(0);

}

static uint8_t prob[256] = {0, 198, 61, 251, 183, 113, 138, 76, 215, 17, 234, 44, 96, 166, 93, 155, 247, 49, 202, 12, 64, 134, 125, 187, 32, 230, 29, 219, 151, 81, 170, 108, 130, 68, 191, 121, 53, 243, 8, 206, 85, 147, 104, 174, 226, 36, 223, 25, 117, 179, 72, 142, 194, 4, 255, 57, 162, 100, 159, 89, 21, 211, 40, 238, 27, 221, 38, 224, 172, 106, 145, 87, 204, 10, 241, 55, 123, 189, 70, 128, 236, 42, 209, 23, 91, 157, 102, 160, 59, 253, 6, 192, 140, 74, 177, 119, 153, 95, 164, 98, 46, 232, 19, 213, 78, 136, 115, 181, 249, 63, 196, 2, 110, 168, 83, 149, 217, 31, 228, 34, 185, 127, 132, 66, 14, 200, 51, 245, 56, 254, 5, 195, 143, 73, 178, 116, 239, 41, 210, 20, 88, 158, 101, 163, 207, 9, 242, 52, 120, 190, 69, 131, 24, 222, 37, 227, 175, 105, 146, 84, 186, 124, 135, 65, 13, 203, 48, 246, 109, 171, 80, 150, 218, 28, 231, 33, 77, 139, 112, 182, 250, 60, 199, 1, 154, 92, 167, 97, 45, 235, 16, 214, 35, 229, 30, 216, 148, 82, 169, 111, 244, 50, 201, 15, 67, 133, 126, 184, 212, 18, 233, 47, 99, 165, 94, 152, 3, 197, 62, 248, 180, 114, 137, 79, 161, 103, 156, 90, 22, 208, 43, 237, 118, 176, 75, 141, 193, 7, 252, 58, 86, 144, 107, 173, 225, 39, 220, 26, 129, 71, 188, 122, 54, 240, 11, 205};

uint8_t bufp[100];
uint8_t bufc[100];
//uint8_t stat[8][4][256][256][256];
vector<int> stat[8][256];

int main() {
    int i,ext,k,k0,k1,k2,k0e,k1e,k2e,j,r;
    uint8_t p[8];
    uint8_t c[8];
    vector<int> intersect;
    /*
    uint8_t bb=permuone(0x72,6,1);
    printf("%02x ", bb);
    bb=inv_permuone(bb,p_next[6],0);
    printf("%02x ", bb);
    return 0;

    stat[0][0].push_back(2333);
    stat[0][0].push_back(2333);
    for (vector<int>::iterator it = stat[0][0].begin(); it!=stat[0][0].end(); ++it)
        cout<<' '<<*it;
    return 0;
    */
    //notmain();
    ifstream fin("data",ios::binary);
    for (i=0;i<8;i++) {
        fin.read(p,8);
        for (k=0;k<8;k++)
            bufp[i*8+k]=p[k];
        fin.read(c,8);
        for (k=0;k<8;k++)
            bufc[i*8+k]=c[k];
    }

    uint8_t pos;
    uint8_t byte;

    for (i=0; i<8; i++)
    for (k0=0; k0<256; k0++)
    for (k1=0; k1<128; k1++) {
        k1e=k1/2*4+k1%2; // one trivial bits
    for (k2=0; k2<128; k2++) {
        k2e=k2/2*4+k2%2;
    for (ext=0; ext<4; ext++) {
        pos = 5;
        byte = bufp[i*8+pos];
        byte ^= k0;
        byte = s_box[byte];
        byte = permuone(byte, pos, ext/2);
        pos = p_next[pos];
        byte ^= k1e;
        byte = s_box[byte];
        byte = permuone(byte, pos, ext%2);
        pos = p_next[pos];
        byte ^= k2e;
        byte = s_box[byte];
        stat[i][byte].push_back(k0*65536+k1*256+k2);
    }
    }
    }

    int cur[8];
    int size[8];
    vector<int> cands[8];
    int minv,maxv;
    for (k0=0; k0<128; k0++) {
        k0e=k0/8*16+k0%8;
    for (k1=0; k1<128; k1++) {
        k1e=k1/16*32+k1%16;
    for (k2=0; k2<256; k2++) {
        for (i=0; i<8; i++) {
        cands[i].clear();
        for (ext=0; ext<4; ext++) {
            pos = 0;
            byte = bufc[i*8+pos];
            byte ^= k2;
            byte = inv_s_box[byte];
            byte ^= k1e;
            byte = inv_permuone(byte, pos, ext%2);
            pos = p_prev[pos];
            byte = inv_s_box[byte];
            byte ^= k0e;
            byte = inv_permuone(byte, pos, ext/2);
            pos = p_prev[pos];
            cands[i].insert(cands[i].end(), stat[i][byte].begin(), stat[i][byte].end());
        }
        sort(cands[i].begin(), cands[i].end());
        cands[i].erase(unique( cands[i].begin(), cands[i].end() ), cands[i].end());
        }
        memset(cur, 0, sizeof(cur));
        intersect.clear();
        for (i=0; i<8; i++)
            size[i] = cands[i].size();
        /*
        for (i=0; i<8; i++) 
            printf("%d ", size[i]);
        printf("\n");
        for (i=0; i<8; i++) {
            for (j=0;j<size[i]/1000;j++)
                printf("%d ", cands[i][j]);
            printf("\n");
        }
        exit(0);
        */
        while (true) {
            uint8_t fin=0;
            for (i=0; i<8; i++)
                if (cur[i]>=size[i])
                    fin=1;
            if (fin)
                break;

            minv = cands[0][cur[0]];
            maxv = minv;
            for (i=1; i<8; i++) {
                int tmp = cands[i][cur[i]];
                if (tmp<minv)
                    minv = tmp;
                if (tmp>maxv)
                    maxv = tmp;
            }
            if (minv == maxv) {
                intersect.push_back(minv);
                for (i=0; i<8; i++)
                    cur[i]++;
            } else {
                for (i=0; i<8; i++)
                    if (cands[i][cur[i]]!=maxv)
                        cur[i]++;
            }
        }
        for (i=0; i<intersect.size(); i++) {
            int tmp = intersect[i];
            int tmp2 = tmp/256%256;
            tmp2 = tmp2/2*4+tmp2%2;
            int tmp3 = tmp%256;
            tmp3 = tmp3/2*4+tmp3%2;
            cout<<tmp/65536<<' '<<tmp2<<' '<<tmp3<<' '<<k0e<<' '<<k1e<<' '<<k2<<endl;
        }
        /*
        ss.clear();
        set_intersection(stat[0][idx[0]].begin(),stat[0][idx[0]].end(),stat[1][idx[1]].begin(),stat[1][idx[1]].end(), inserter(ss,ss.begin()));
        for (i=2;i<8;i++) {
            intersect.clear();
            set_intersection(ss.begin(),ss.end(),stat[i][idx[i]].begin(),stat[i][idx[i]].end(),
                             inserter(intersect,intersect.begin()));
            ss = intersect;
        }
        for (set<int>::iterator it = ss.begin(); it!=ss.end(); ++it) {
            int tmp = *it;
            cout<<tmp/65536<<' '<<tmp/256%256<<' '<<tmp%256<<' '<<k0<<' '<<k1<<' '<<k2<<endl;
        }
        */
    }
    }
    }
    
    return 0;
}
