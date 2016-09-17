/*
 * Copyright (C) Schweizerische Bundesbahnen SBB, 2016.
 */

package endpoint;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;


@RestController
public class InfoResource {

    @RequestMapping("/info")
    @ResponseBody
    public HalloPojo getInfo() {
        return new HalloPojo();
    }

}
