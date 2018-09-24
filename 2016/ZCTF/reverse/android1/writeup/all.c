#include <stdio.h>
#include <string.h>

int dword_C00D[4] = {0x2175DA3A, 0xB3DBE2DB, 0x149B411, 0xD4EAC6A5};

unsigned int sub_8AF8(int *a1, unsigned int a2, int *a3)
{
  unsigned int v3; // r3@1
  unsigned int v4; // r5@1
  unsigned int v5; // r4@3
  unsigned int v6; // r3@3
  unsigned int v7; // r6@3

  v3 = 0;
  v4 = a2 & 7;
  if ( !(a2 & 7) )
  {
    while ( v4 != a2 >> 3 )
    {
      v5 = *a1;
      v6 = a1[1];
      v7 = 0xC6EF3720;
      do
      {
        v6 -= (v5 + v7) ^ (16 * v5 + a3[2]) ^ ((v5 >> 5) + a3[3]);
        v5 -= (v6 + v7) ^ (16 * v6 + *a3) ^ ((v6 >> 5) + a3[1]);
        v7 += 0x61C88647;
      }
      while ( v7 );
      *a1 = v5;
      a1[1] = v6;
      v4 = (v4 + 1) & 0xFFFF;
      a1 += 2;
    }
    v3 = a2;
  }
  return v3;
}


char aGhgstu45imnesv[] = "GHgSTU45IMNesVlZadrXf17qBCJkxYWhijOyzbcR6tDPw023KLA8QEFuvmnop9+/";

char * sub_8B80(char *a1, char *a2, int a3)
{
  int v3; // r3@1
  char *v4; // r4@1
  int v5; // r5@1
  int v6; // r6@3
  int v7; // r0@4
  int v8; // r6@5
  char v9; // r6@8
  char *result; // r0@9

  v3 = 0;
  v4 = a2;
  v5 = 0;
  while ( v5 < a3 )
  {
    *v4 = aGhgstu45imnesv[(unsigned int)(unsigned char)*a1 >> 2];
    v6 = 16 * (unsigned char)*a1 & 0x30;
    if ( a3 <= v5 + 1 )
    {
      a2[v3 + 1] = aGhgstu45imnesv[v6];
      v7 = v3 + 3;
      a2[v3 + 2] = 61;
LABEL_7:
      a2[v7] = 61;
      v3 += 4;
      break;
    }
    v4[1] = aGhgstu45imnesv[v6 | ((unsigned int)(unsigned char)a1[1] >> 4)];
    v8 = 4 * (unsigned char)a1[1] & 0x3C;
    if ( a3 <= v5 + 2 )
    {
      v7 = v3 + 3;
      a2[v3 + 2] = aGhgstu45imnesv[v8];
      goto LABEL_7;
    }
    v3 += 4;
    v5 += 3;
    v4[2] = aGhgstu45imnesv[v8 | ((unsigned int)(unsigned char)a1[2] >> 6)];
    v9 = a1[2];
    a1 += 3;
    v4[3] = aGhgstu45imnesv[v9 & 0x3F];
    v4 += 4;
  }
  result = a2;
  a2[v3] = 0;
  return result;
}


int dword_9E0C[32] ={ 0x57, 0xC, 0xFFFFFFF3, 0xFFFFFFFB, 0xFFFFFFF2, 0xF, 0xFFFFFFDE, 0x44
,0xFFFFFFFD, 0xFFFFFFD5, 0x1B, 0xFFFFFFEA, 0xD, 0xFFFFFFF7, 0x1A, 0xB
,0xFFFFFFBD, 0x24, 0xFFFFFFE4, 0x3A, 0, 0xFFFFFFC4, 0x40, 0xFFFFFFC1
,0x39, 0xFFFFFFC7, 0x11, 2, 0xB, 0xFFFFFFFD, 0x17, 0xFFFFFFCF};

int sub_8C20(int a1, signed int a2)
{
  int v2; // r3@1

  v2 = 'W';
  if ( a2 )
  {
    v2 = 'A';
    if ( a2 <= 31 )
      v2 = (a1 + dword_9E0C[a2]) & 0xFF;
  }
  return v2;
}

int sub_8C44(char *r0_0)
{
  char *v1; // r6@1
  int i; // r4@2
  unsigned int v3; // r6@3
  char v4; // r7@7
  int result; // r0@9
  signed int v6; // [sp+0h] [bp-58h]@3
  char a1[52]; // [sp+8h] [bp-50h]@1
  int v8; // [sp+3Ch] [bp-1Ch]@1

  v1 = r0_0;
  memset(a1, 0, 50);
  if ( v1 )
  {
    i = 0;
    if ( strlen(v1) > 0x17 )
    {
      strcpy(a1, v1);
      v3 = 0;
      v6 = 65;
      while ( i < strlen(a1) && i != 32 )
      {
        v4 = a1[i];
        v3 += (unsigned char)(v4 ^ sub_8C20(v6, i));
        v6 = sub_8C20(v6, i++);
      }
      i = v3 <= 0;
    }
  }
  else
  {
    i = 0;
  }
  result = i;
  return result;
}

int main() {
    char s1[33] = "AAAAAAAAAAAAAAA"; // input s1
    char s2[33];
    printf("%s\n", s1);
    sub_8AF8(s1, 16, dword_C00D);
    sub_8AF8(s1 + 16, 16, dword_C00D);
    int i;
    for (i = 0; i < 32; ++i) {
        printf("%02x", (unsigned char)s1[i]);
    }
    printf("\n");
    memset(s2, 0, sizeof(s2));
    sub_8B80(s1, s2, strlen(s1));
    printf("%s\n", s2);

    printf("%d\n", sub_8C44(s2));
    return 0;
}
