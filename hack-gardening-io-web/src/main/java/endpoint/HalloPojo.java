/*
 * Copyright (C) Schweizerische Bundesbahnen SBB, 2016.
 */

package endpoint;

public class HalloPojo {

    private String info;

    HalloPojo(){
        info = "Hallo da";
    }

    public String getInfo(){
        return info;
    }
}
