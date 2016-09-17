/*
 * Copyright (C) Schweizerische Bundesbahnen SBB, 2016.
 */

package services;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import hack.gardening.io.web.model.json.Plant;
import hack.gardening.io.web.model.json.Plantsschema;

public class JasonService {

    public List<Plant> unmarshalJsonObject(Path pathToSource) throws FileNotFoundException {
        if (!Files.exists(pathToSource)) {
            throw new FileNotFoundException("Pfad gibt es nicht");
        }

        try {
            try(Reader reader = new BufferedReader(new InputStreamReader(new FileInputStream(pathToSource.toString())))){
                Gson gson = new GsonBuilder().create();
                Plantsschema plantsschema = gson.fromJson(reader, Plantsschema.class);
                List<Plant> plantList = plantsschema.getPlants();
                return plantList;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        //--- Here we will maybe never land. ---
        return null;
    }
}
