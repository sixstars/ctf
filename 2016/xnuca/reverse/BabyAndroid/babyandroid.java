package com.example.babyandroid;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View$OnClickListener;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends Activity {
    public MainActivity() {
        super();
    }

    public String check(String password) {
        byte[] pwd = password.getBytes();
        int i;
        for(i = 0; i < pwd.length; ++i) {
            pwd[i] = ((byte)(pwd[i] ^ i));
        }
//x-nuca2016
        byte[] pad = new byte[]{5, 9, 14, 1, 84, 15, 15, 84, 8, 9, 6, 88, 1, 15, 89, 7, 27, 29, 68, 67};
        for(i = 0; i < pwd.length; ++i) {
            pwd[i] = ((byte)(pwd[i] ^ pad[i]));
        }
		//[5, 8, 12, 2, 80, 10, 9, 83, 0, 0, 12, 83, 13, 2, 87, 8, 11, 12, 86, 80]
        byte[] newpwd = new byte[30];
        for(i = 0; i < pwd.length; i += 2) {
            newpwd[i] = ((byte)((pwd[i] - 0x30) * 10 + (pwd[i + 1] - 0x30)));
        }
		//0,2,4 -> 
        for(i = 0; i < newpwd.length; ++i) {
            newpwd[i] = ((byte)(newpwd[i] + (((byte)(newpwd.length - i))) * 3));
        }

        StringBuilder ret_list = new StringBuilder();
        for(i = 0; i < newpwd.length; ++i) {
            ret_list.append(newpwd[i]);
        }

        return ret_list.toString();
    }

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.setContentView(2130903065);
        this.findViewById(2131296337).setOnClickListener(new View$OnClickListener() {
            public void onClick(View v) {
                View v1 = MainActivity.this.findViewById(2131296335);//x-nuca2016
                View v0 = MainActivity.this.findViewById(2131296336); //check(v0) = 'x-nuca2016'
                if(MainActivity.this.check(((EditText)v0).getText().toString()).equals(((EditText)v1)
                        .getText().toString())) {
                    Toast.makeText(MainActivity.this.getApplicationContext(), "wrong", 1).show();
                }
                else {
                    Toast.makeText(MainActivity.this.getApplicationContext(), "flag{" + ((EditText)v0)
                            .getText().toString() + "}", 1).show();
                }
            }
        });
    }

    public boolean onCreateOptionsMenu(Menu menu) {
        this.getMenuInflater().inflate(2131492864, menu);
        return 1;
    }

    public boolean onOptionsItemSelected(MenuItem item) {
        boolean v1 = item.getItemId() == 2131296351 ? true : super.onOptionsItemSelected(item);
        return v1;
    }
}

