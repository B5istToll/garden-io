/*
 * Copyright (C) Schweizerische Bundesbahnen SBB, 2016.
 */


import javax.ws.rs.Path;
import javax.ws.rs.core.Response;


@Path("/info")
public class GardeningResource {


    public Response getInfo(){
        String output = "Jersey say : ";

        return Response.status(200).entity(output).build();
    }
}
